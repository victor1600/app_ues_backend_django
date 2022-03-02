import os

if 'data' not in os.listdir():
    os.system(f'wget https://victor95-files.s3.amazonaws.com/data.zip')
    os.system(f'unzip data.zip')
    print('finished downloading data folder')
else:
    print('data folder exists')