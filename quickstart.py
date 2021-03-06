# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:13:09 2019

@author: Luming
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
def autoupload():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    try:
        name = '1.csv'  # It's the file which you'll upload
        file = drive.CreateFile()  # Create GoogleDriveFile instance
        file.SetContentFile(name)
        file.Upload()
    except :
        print("Unexpected error:", sys.exc_info()[0])