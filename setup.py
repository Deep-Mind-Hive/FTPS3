from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='FTPtoS3',
    version='0.1.1',
    description='Package for transferring huge files from FTP to S3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Deep-Mind-Hive/FTPS3',
    author='Harsh Vardhan and Sai Madhav',
    author_email='deephivemind@gmail.com,kambhampati.sm@gmail.com',
    classifiers=["License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10"],
    keywords='FTPS3,ftptos3,data migrate from FTP to S3',
    packages=['FTPS3'],
    python_requires='>=3.5, <4',
    install_requires=['ftplib','boto3'],
)