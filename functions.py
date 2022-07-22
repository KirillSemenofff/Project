import os
import zipfile
import shutil
from subprocess import call

def unix(folder_name):
    try:
        shutil.copyfile(r'\ffmpeg.bat', 
            rf'\{folder_name}\ffmpegcopy.bat')
        os.chdir(rf'C:\Users\79057\Desktop\betterunix\videos\{folder_name}')
        call(rf'\{folder_name}\zxccopy.bat')
        os.chdir(rf'C:\Users\79057\Desktop\betterunix\videos')
    except Exception as e:
        print(e)

def send_zipfile(message, folder_name,botan):
    try:
        with zipfile.ZipFile(rf'\{folder_name}\tgvideos.zip', 'w') as fantasy_zip:
            for folder, subfolders, files in os.walk(rf'C:\Users\79057\Desktop\betterunix\videos\{folder_name}'):
                for file in files:
                    if file.endswith('_1.mp4'):
                        fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 
                        rf'\{folder_name}'), compress_type = zipfile.ZIP_DEFLATED)
        filezip = open(rf'\{folder_name}\tgvideos.zip','rb')
        botan.send_document(message.chat.id, filezip)
    except Exception as e:
        print(e)