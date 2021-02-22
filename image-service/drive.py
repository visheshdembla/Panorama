from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class DriveAccessor:

    drive = None
    def __init__(self):
        self.drive = None
        self.authUser()
    
    
    def authUser(self):
        """Returns object of drive
        """
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("userCredentials.txt")

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()

        elif gauth.access_token_expired:
            gauth.Refresh()
        
        else:
            gauth.Authorize()
        
        gauth.SaveCredentialsFile("userCredentials.txt")

        self.drive = GoogleDrive(gauth)


    def createFile(self, userFolderId, filename, filecontent):
        file = self.drive.CreateFile({'title': filename, 'parents': [{'id': userFolderId}]})
        file.SetContentString(filecontent)
        file.Upload()
        return file['id']
    

    def createFolder(self, foldername):
        folder = self.drive.CreateFile({'title': foldername, "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        return folder['id']


    def downloadFile(self, fileId):
        """Return the file in string format along with the file name
        """
        file = self.drive.CreateFile({ 'id': fileId})
        return [file['title'], file.GetContentString()]

    def listFolderFiles(self, folderId):
        file_list = self.drive.ListFile({'q': "'" + folderId + "' in parents and trashed=false"}).GetList()
        imageIds = []
        for file1 in file_list:
            imageIds.append(file1['id'])
        return imageIds

if __name__ == "__main__":
    driveClient = DriveAccessor()
    folderId = driveClient.createFolder("Vishesh")
    print("Folder Id " + folderId)
    fileId = driveClient.createFile(folderId, "hello.txt",  "Hello World")
    print(driveClient.downloadFile(fileId))