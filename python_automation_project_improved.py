#improvements from version 1:
#1.using magic library for better file detection
#2.using datetime library to add dates to when the file has been moved and create subfolders based on timestamps
#3.using tkinter library for GUI to make the experience easier to navigate



import os # import the os module to interact with the operating system
import shutil # import shutil module to move files between directories
import magic #import magic for MIME type detection   MIME: originally used for indenitnifying emails, now used for file identifyfgin as well
import datetime #import datetime for timestamp
from tkinter import filedialog, Tk #importing Tkinter for the GUI(graphical user interface)

#function to organize files in the specified directory(hints of original base code)
def organize_files(directory):
     # define file categories and their corresponding extensions
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"]
    }

     #iterate through all the files in the specified directory

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        #checks of the current path is a file and not a folder
        if os.path.isfile(file_path):
            moved = False


            #detecting mime type for the clissification of tte file
            mime_type = magic.from_file(file_path, mime = True)


            #determining which folder the file goes into based on mime type
            for folder, extensions in file_types.items():
                if any (filename.lower().endswith(ext) for ext in extensions) or mime_type.startswith(folder.lower()):

                    #creates subfolder based on timestamps as well

                    #getting the files last timestamp
                    timestamp = os.path.getatime(file_path)
                    #timsetamp in format year-month
                    date_folder = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m")
                    destination_folder = os.path.join(directory, folder, date_folder)


                    #create folder based on timsetamps
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    
                    #code that moves the file to the designated folder
                    destination = os.path.join(destination_folder, filename)
                    shutil.move(file_path, destination)
                    print("Moved: {filename} to {destination_folder}")
                    moved = True
                    break


            #if the file isn't moved to any categories, move it into others folder
            if not moved:

                #getting the timsetamp for the uncategorized file
                timestamp = os.path.getmtime(file_path)
                #time format same as before, year-month
                data_folder = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m")
                other_folder = os.path.join(directory, "Others", data_folder)

                #creates others folder if missing
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)

                #moving the file to the others folder
                destination = os.path.join(other_folder, filename)
                shutil.move(file_path, destination)
                print("Moved: {filename} to {other_folder}")

#entry point for the script
if __name__ == "__main__":
    #setting up the GUI for the directory selection in the application
    root = Tk()
    #hiding the root window      root window: main window of GUI application. has widgets, files, etc. whatever you want
    root.withdraw()
    print("Please select the directory to organize.")
    directory = filedialog.askdirectory(title="Select Directory to Organize")


     # check if the directory exists and is valid
    if directory and os.path.exists(directory) and os.path.isdir(directory):
        print("Organizing files in: {directory}")
        # call the organize_files function
        organize_files(directory)
    else:
        print("Error: not a valid directory")

