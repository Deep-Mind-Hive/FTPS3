import ftplib
import boto3
import sys


class FTPtoS3():
    def __init__(self,
                 ftp_client, s3_client):
        """
        :param ftp_client: FTP Connection Object
        :param s3_client: S3 Connection Object
        """
        self.single_upload = b''
        self.ftp_client = ftp_client
        self.s3_client = s3_client
        self.part = b''
        self.uploaded_file = 0
        self.total_items = list()
        self.item = 0
        self.upload_id = None

    def uploadS3(self, path, s3_path, file_name, s3_bucket):
        """
        :param path: FTP path where file is stored
        :param s3_path:  S3 path where the file should be stored
        :param file_name: Name of the file in FTP
        :param s3_bucket: Name of the bucket in S3
        """
        # Check for the valid path
        try:
            self.ftp_client.cwd(path)
        except ftplib.error_perm:
            raise Exception("Path does not exist")

        # Check for the valid file name
        try:
            size = self.ftp_client.size(file_name)
        except ftplib.error_perm:
            raise Exception("File does not exist")

        def single_part_upload(content):
            # FTP method to store the data for a small file
            self.single_upload += content

        def multipart_upload(data):
            # FTP method to store the data for a large file
            for _ in [1]:
                self.part += data
                read_size = sys.getsizeof(self.part)
                if read_size < 10000000:
                    # If data read is less than 10MB then increment the read data
                    # till it reaches 10MB
                    continue
                self.uploaded_file += sys.getsizeof(self.part)
                # Upload read part of the data to S3
                transferred_part = self.s3_client.upload_part(
                    Bucket=s3_bucket,
                    Key=s3_path,
                    PartNumber=self.item + 1,
                    UploadId=self.upload_id,
                    Body=self.part)
                item_metadata = {
                    'PartNumber': self.item + 1,
                    'ETag': transferred_part['ETag']}
                self.total_items.append(item_metadata)
                self.item += 1
                print(self.item)
                self.part = b''

        if size > 10242880:
            try:
                # Multipart upload initilization
                initiate_multipart_upload = self.s3_client.create_multipart_upload(Bucket=s3_bucket,
                                                                              Key=s3_path)
                self.upload_id = initiate_multipart_upload['UploadId']

                # Keeping a limit to read at max 15MB of data
                self.ftp_client.retrbinary(f"RETR {file_name}", multipart_upload, blocksize=15000000)
                self.uploaded_file += sys.getsizeof(self.part)
                # Upload the remaining of read part for last iteration
                transferred_part = self.s3_client.upload_part(
                    Bucket=s3_bucket,
                    Key=s3_path,
                    PartNumber=self.item + 1,
                    UploadId=self.upload_id,
                    Body=self.part)
                item_metadata = {
                    'PartNumber': self.item + 1,
                    'ETag': transferred_part['ETag']}
                self.total_items.append(item_metadata)
                self.item += 1
                multipart_metadata = {
                    'Parts': self.total_items
                }
                # Completing the multipart
                var = self.s3_client.complete_multipart_upload(
                    Bucket=s3_bucket,
                    Key=s3_path+file_name,
                    UploadId=self.upload_id,
                    MultipartUpload=multipart_metadata
                )
                return var
            except ftplib.ConnectionResetError:
                raise Exception("An existing connection was forcibly closed by the remote host")
            except Exception:
                raise Exception("Multipart Upload Failed")
        else:
            self.ftp_client.retrbinary(f"RETR {file_name}", single_part_upload, blocksize=10242880)
            # For small file use put_object method
            try:
                var = self.s3_client.put_object(Body=self.single_upload, Bucket=s3_bucket,
                                     Key=s3_path + file_name)
                return var
            except Exception:
                raise Exception("Unable to upload object")




