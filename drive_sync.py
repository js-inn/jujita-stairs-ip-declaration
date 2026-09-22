import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Replace with your actual Drive folder ID

def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_ledger_file(file_path, file_name):
    service = authenticate_drive()
    
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]
    }
    
    media = MediaFileUpload(file_path, resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f"Ledger successfully archived. File ID: {file.get('id')}")

if __name__ == '__main__':
    # Example: Uploading a local audit file
    # Make sure you have a test file or your sqlite db ready
    if os.path.exists('ledger_records.db'):
        upload_ledger_file('ledger_records.db', 'audit_ledger_snapshot.db')
    else:
        print("ledger_records.db not found. Create a sample file to test!")

