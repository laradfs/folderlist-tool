# folderlist-tool
A Windows command line tool (created from a Windows Powershell script) for generating basic metadata on a file directory for use in archival description.

Folderlist.exe is a Windows executable program that can be run on a directory in a Windows environment and produce either of the following: 
1) A simple folder list of the top two levels of folders, including their size and number of files.  The list can then be copied and pasted from the screen into a scope/content or arrangement note in an archival finding aid.    
[use the -list option]
2) A text file with a folder list (top two levels) marked up as EAD components. The list can then be copied and pasted into an EAD finding aid, so the folders will be components of the collection. If EAD output is requested, the top level folders are &lt;c01&gt; elements, and subfolders are &lt;c02&gt; elements
[use the -ead option, plus a file name for the output]
 
Both outputs include the top two levels of folders in the hierarchy, with any "loose" files in each level summarized as "additional files."  

INSTRUCTIONS FOR USE:
 
Download the .exe file and put it somewhere (e.g. on your desktop for now).  
To run, open a command prompt and navigate to the folder whose contents you want to list (e.g. an archival collection folder), using the cd command and entering the path.
At the command prompt, enter the path to folderlist.exe. 
After the path, type the desired output format:
-list (or -l) for a simple list* 
-ead  (or -e) followed by a  path and filename for the file you want to create (e.g. -ead c:\Users\username\Documents\collectionname.txt) to generate EAD components in a text file. NOTE: if you do not provide a path and filename, a file called FolderListOutput.txt will be written to the parent directory.  If you provide a filename and no path, the file will be written into the same directory that you just analyzed.
Copy the output from the screen (if you chose -list) or the text file (if you chose -ead) and paste it into the appropriate spot in the finding aid file.

NOTE: If you execute the program without any parameter (without -ead or -list) it will default to the -ead option and the output will be saved in the directory that is the parent of the directory the program is being run on.  
 
*If you wish to save the output of the -list option to a text file, you can append “>" followed by a path and filename

A short video demonstration is available at https://mediaspace.umn.edu/media/t/1_qfcpa2w3#

