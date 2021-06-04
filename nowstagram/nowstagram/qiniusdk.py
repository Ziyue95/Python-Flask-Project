# -*- coding: utf-8 -*-

from nowstagram import app
from qiniu import Auth, put_stream, put_data
import os

access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
#Initializa cloud server
q = Auth(access_key, secret_key)

bucket_name = app.config['QINIU_BUCKET_NAME']

def qiniu_upload_file(source_file, save_file_name):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)
    # fileno() method returns the file descriptor of the stream, as a number.
    #ret, info = put_stream(token, save_file_name, source_file.stream,
    #                      "qiniu", os.fstat(source_file.stream.fileno()).st_size)
    ret, info = put_data(token, save_file_name, source_file.stream)

    print(type(info.status_code), info)
    #if info.status_code == 200:
    #    return domain_prefix + save_file_name
    return None