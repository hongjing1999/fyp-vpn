from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload



def uploadFile(file: str):

    username = file.split("@")[0]
    creds = None
    if os.path.exists('key.json'):
        creds = Credentials.from_service_account_file("key.json")

    try:
        service = build('drive', 'v3', credentials=creds)
        directoryId = ""
        userDirectory = service.files().list(
            q="mimeType = 'application/vnd.google-apps.folder' and '14bW_E-YB2IM5jCg3aYC5PqyeaEuJfWWC' in parents and trashed = false and name = '" + username + "'",
            spaces='drive',
            fields='nextPageToken, files(id, name)', ).execute()

        if (len(userDirectory.get('files', [])) < 1):
            file_metadata = {'name': username, 'parents': ["14bW_E-YB2IM5jCg3aYC5PqyeaEuJfWWC"], 'mimeType': 'application/vnd.google-apps.folder'}
            directory = service.files().create(body=file_metadata,
                                          fields='id').execute()
            directoryId = directory.get("id")
        else:
            directoryId = userDirectory.get('files', [])[0].get("id")

        file_metadata = {'name': file, 'parents': [directoryId]}
        media = MediaFileUpload('/root/algo/configs/178.128.102.222/wireguard/'+file, mimetype='text/plain')
        new_file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
    except HttpError as error:
        print(f'An error occurred: {error}')

