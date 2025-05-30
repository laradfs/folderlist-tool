#29 May 2025 - includes EAD mark-up and saving output to file at given path. Correctly nests <c0x>.
import os

def format_size(bytes_size):
    """
    Convert a size in bytes into a human-readable format using appropriate units.
    Example: 2048 -> '2.00 KB'
    """
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def get_immediate_file_stats(path):
    """
    Return the number and total size of files directly within a given directory.
    Does not include files in subdirectories.
    """
    try:
        # List only files in the directory (not subdirectories)
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except Exception:
        return 0, 0  # If we can't access the directory, return zeros

    # Calculate total size of all accessible files
    total_size = sum(
        os.path.getsize(os.path.join(path, f))
        for f in files if os.path.exists(os.path.join(path, f))
    )
    return len(files), total_size

def get_total_dir_size(path):
    """
    Calculate the total size of all files within the directory, including all subdirectories.
    Used for displaying full size when listing a directory.
    """
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
            except Exception:
                continue  # Skip any inaccessible files
    return total

def list_directory_contents(path, max_depth, current_depth=1):
    """
    Recursively list the contents of a directory up to a given depth.
    Follows a custom format with dashes based on depth.
    """
    if current_depth > max_depth:
        return  # Stop recursion if we've reached the max depth

    try:
        entries = os.listdir(path)  # List entries in the current directory
    except PermissionError:
        print(f"{'-' * (current_depth - 1)}[Permission Denied]")
        return

    # Separate subdirectories from files
    subdirs = sorted([e for e in entries if os.path.isdir(os.path.join(path, e))])
    file_count, file_size = get_immediate_file_stats(path)

    # Loop through each subdirectory and print its summary
    for subdir in subdirs:
        subdir_path = os.path.join(path, subdir)
        sub_file_count, _ = get_immediate_file_stats(subdir_path)

        # Calculate proper indentation: no dash at level 1, otherwise depth-1 dashes
        
        # Print the subdirectory summary
        if output_mode == "list":
            indent = '' if current_depth == 1 else '- ' * (current_depth - 1)
            folderlist.write(f"{indent}{subdir}, {sub_file_count} files, {format_size(get_total_dir_size(subdir_path))}\n")
        else:
            indent = '' if current_depth == 1 else '\t' * (current_depth - 1)
            folderlist.write(f"{indent}<c0{current_depth} level=\"file\">\n")
            folderlist.write(f"{indent}\t<did>\n")
            folderlist.write(f"{indent}\t\t<unittitle>{subdir}</unittitle>\n")
            folderlist.write(f"{indent}\t\t<physdesc>\n")
            folderlist.write(f"{indent}\t\t\t<extent altrender=\"materialtype spaceoccupied\">{format_size(get_total_dir_size(subdir_path))}</extent>\n")
            folderlist.write(f"{indent}\t\t\t<extent altrender=\"carrier\">{sub_file_count} files</extent>\n")
            folderlist.write(f"{indent}\t\t</physdesc>\n")
            folderlist.write(f"{indent}\t</did>\n")
                      
        # Recursively list the subdirectory's contents
        list_directory_contents(subdir_path, max_depth, current_depth + 1)
        if output_mode != "list":
            folderlist.write(f"{indent}</c0{current_depth}>\n")

    # After listing all subdirectories, print additional files in this directory (if any) and if there are no 
    if file_count > 0 and len(subdirs)>0:
        if output_mode == "list":
            folderlist.write(f"{indent}Additional files, {file_count} files, {format_size(file_size)}\n")
        else:
            folderlist.write(f"{indent}<c0{current_depth} level=\"file\">\n")
            folderlist.write(f"{indent}\t<did>\n")
            folderlist.write(f"{indent}\t\t<unittitle>Additional files</unittitle>\n")
            folderlist.write(f"{indent}\t\t<physdesc>\n")
            folderlist.write(f"{indent}\t\t\t<extent altrender=\"materialtype spaceoccupied\">{format_size(file_size)}</extent>\n")
            folderlist.write(f"{indent}\t\t\t<extent altrender=\"carrier\">{file_count} files</extent>\n")
            folderlist.write(f"{indent}\t\t</physdesc>\n")
            folderlist.write(f"{indent}\t</did>\n")
            folderlist.write(f"{indent}</c0{current_depth}>\n")

if __name__ == "__main__":
    # Prompt user for a directory path
    user_input = input("Enter the full path of a Windows directory: ").strip('"')
    output_mode = input("EAD or list?")
    # Validate the path
    if not os.path.isdir(user_input):
        print("The path provided is not a valid directory.")
    else:
        try:
            # Prompt user for maximum depth of traversal
            max_depth = int(input("Enter maximum depth to list subdirectories (1 for top level only): "))
            folderlistname = input("Enter file name and path for output:")
            folderlist = open(folderlistname, "w")
            list_directory_contents(user_input, max_depth)
            folderlist.close()
        except ValueError:
            print("Invalid input. Please enter an integer for maximum depth.")

