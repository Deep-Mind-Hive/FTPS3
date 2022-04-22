### **Project Description**

#FTPS3
Spark does not have a connector to connect to FTP as it is not HDFS. So to move a file from FTP to S3,
we need to download the file from FTP to local system and then upload it to S3. There is no library in 
market through which we can migrate a file from FTP to S3 directly. FTPS3 library helps you to mitigate
it.

The `FTPtoS3` class has needs to be invoked by passing the ftp and s3 client connection objects.
After creating the object we can use `uploadS3` method to upload the file to S3.

## Installation
Installation is recommended via pip for Python 3.
```python
pip install FTPtoS3
```
The package can then be imported using:
```python
import FTPS3
```

## Usage
Access the modules using the following statements.
```python
from FTPS3.FTPtoS3 import *
```

Example
```python
ftp_client = ftplib.FTP()
ftp_client.connect("<hostname>", <port>)
ftp_client.login("<username>", "<passowrd>")
s3_client = boto3.client(
    service_name='s3',
    region_name='<region>')
obj = FTPtoS3(ftp_client, s3_client)
obj.uploadS3("<ftp_path where file is present>",
             "<s3_path to be uploaded>",
             "<file_name in FTP>", "<s3 bucket name>")
```


## Dependencies
FTPS3 has the following dependencies:
* [ftplib](https://docs.python.org/3/library/ftplib.html)
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

## License 
MIT License  
© 2022 FTPS3








