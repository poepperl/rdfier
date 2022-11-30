import os
import s3fs

class S3Connector:

    def __init__(self):
        self.AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

        self.s3 = s3fs.S3FileSystem(anon=False)  
        
    def get_storage_options(self):
        storage_options = {
            "key": self.AWS_ACCESS_KEY_ID,
            "secret": self.AWS_SECRET_ACCESS_KEY,
            "token": self.AWS_SESSION_TOKEN,
        }
        return storage_options

    def glob(self, path, pattern):
        return self.s3.glob(path+pattern)

    def get_fiels(self, path):
        return self.s3.ls(path)
