import shutil
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()


def download_folder():
    """used to make backup"""
    drive = GoogleDrive(gauth)
    fileID = ''
    fileList = drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()
    for file in fileList:
        if (file['title'] == "files"):
            fileID = file['id']
            break
    str = "\'" + fileID + "\'" + " in parents and trashed=false"  # 'files' folder path

    file_list = drive.ListFile({'q': str}).GetList()
    for file in file_list:  # file -> users ids
        fileID = file['id']
        str1 = "\'" + fileID + "\'" + " in parents and trashed=false"  # user_id

        fileID2 = ''
        file_list_2 = drive.ListFile({'q': str1}).GetList()
        for file_2 in file_list_2:
            fileID2 = file_2['id']
            str2 = "\'" + fileID2 + "\'" + " in parents and trashed=false"  # notification folder

            if fileID2 != '':
                file_list_3 = drive.ListFile({'q': str2}).GetList()
                for file_3 in file_list_3:
                    my_dir = f"files/{file['title']}/{file_2['title']}"
                    if not os.path.exists(my_dir):
                        os.makedirs(my_dir)
                    file_3.GetContentFile(f"{my_dir}/{file_3['title']}")  # downloads

            else:
                return ''


def make_archive():
    if os.path.exists('my_archive.zip'):
        os.remove('my_archive.zip')
    shutil.make_archive('my_archive', 'zip', 'files')


def make_backup():
    download_folder()
    make_archive()

    drive = GoogleDrive(gauth)
    fileID = ''
    fileList = drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()
    for file in fileList:
        if file['title'] == "backup":
            fileID = file['id']
            break

    my_file = drive.CreateFile({'title': f'my_archive', 'parents': [{'id': fileID}]})  # создаем файл на диске
    my_file.SetContentFile(f'my_archive.zip')
    my_file.Upload()


if __name__ == '__main__':
    make_backup()

