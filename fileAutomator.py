from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ! FILL IN BELOW
# ? folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"
source_dir = "/Users/ahmedjuvale/Downloads"
# dest_dir_sfx = ""
# dest_dir_music = ""
dest_dir_video = "/Users/ahmedjuvale/Movies"
dest_dir_image = "/Users/ahmedjuvale/Downloads/Wallpapers"
dest_dir_documents = "/Users/ahmedjuvale/Downloads/Fall 2023"
dest_dir_340 = "/Users/ahmedjuvale/Downloads/Fall 2023/CSE 340"
dest_dir_412 = "/Users/ahmedjuvale/Downloads/Fall 2023/CSE 412"
dest_dir_463 = "/Users/ahmedjuvale/Downloads/Fall 2023/CSE 463"
dest_dir_OnePiece= "/Users/ahmedjuvale/Downloads/One Piece"


# ? supported image types
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
# audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]




def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):

    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
    
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.checkClass(entry, name)
    
    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if "One Pace" in name or "One Piece" in name:
                if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                    onePieceChanged = True
                    move_file(dest_dir_OnePiece, entry, name)
                    logging.info(f"Moved video file: {name}")
                    return
            elif (name.endswith(video_extension) or name.endswith(video_extension.upper())):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")
                return

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")
                return
    

    def checkClass(self, entry, name):
         for documents_extension in document_extensions:
            if "CSE340" in name:
                    if (name.endswith(documents_extension) or name.endswith(documents_extension.upper())) or name.endswith(".zip"):
                        move_file(dest_dir_340, entry, name)
                        logging.info(f"Moved document file: {name}")
                        return
            elif "CSE412" in name:
                    if (name.endswith(documents_extension) or name.endswith(documents_extension.upper())) or (name.endswith(".zip") or name.endswith(".mp4")):
                        move_file(dest_dir_412, entry, name)
                        logging.info(f"Moved document file: {name}")
                        return
            elif "CSE463" in name:
                    if (name.endswith(documents_extension) or name.endswith(documents_extension.upper())) or (name.endswith(".zip") or name.endswith(".mp4")):
                        move_file(dest_dir_463, entry, name)
                        logging.info(f"Moved document file: {name}")
                        return
            

    # def check_340_files(self, entry, name): 
       

    # def check_412_files(self, entry, name):
            
    
    # def check_463_files(self, entry, name):
           
            
            


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



# Unittest via the MagicMock whilst using the MoverHandler class
import unittest
from unittest.mock import MagicMock
from fileAutomator import MoverHandler, move_file  

class TestMoverHandler(unittest.TestCase):
    def setUp(self):
        self.handler = MoverHandler()
        self.mock_entry = MagicMock()
        self.mock_entry.name = 'some_file_name'

    def test_checkClass_CSE340(self):
        # Mocking move_file function
        with unittest.mock.patch('fileAutomator.move_file') as mock_move:
            self.handler.checkClass(self.mock_entry, 'CSE340_test_document.pdf')
            mock_move.assert_called_once_with(dest_dir_340, self.mock_entry, 'CSE340_test_document.pdf')

    def test_check_video_files(self):
        # Mocking move_file function
        with unittest.mock.patch('fileAutomator.move_file') as mock_move:
            self.handler.check_video_files(self.mock_entry, 'test_video.mp4')
            mock_move.assert_called_once_with(dest_dir_video, self.mock_entry, 'test_video.mp4')

    def test_check_image_files(self):
        # Mocking move_file function
        with unittest.mock.patch('fileAutomator.move_file') as mock_move:
            self.handler.check_image_files(self.mock_entry, 'test_image.jpg')
            mock_move.assert_called_once_with(dest_dir_image, self.mock_entry, 'test_image.jpg')

# More test methods can be added here

if __name__ == '__main__':
    unittest.main()
