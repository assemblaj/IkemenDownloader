import zipfile
from configs import ZIP_FILE_PATH
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

def unzip_file():
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(".")
        return zip_ref.namelist()[0]

def move_file(file_name, new_path):
    if new_path != dir_path :
       if not new_path.endswith('/'): 
           new_path = new_path + '/'
       counter = 1
       new_name = file_name 
       while os.path.exists(new_path + new_name):
           file_name_parts = file_name.split(".zip")
           new_name = file_name_parts[0] + f"({counter}).zip"
           counter = counter + 1
       os.rename(file_name, new_path + new_name)


