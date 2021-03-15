from flask import session, redirect
import functools
from datetime import datetime
from qiniu import Auth, put_data
from app import constants


# 自定义装饰器，封装用户的登录信息，登录验证装饰器
def login_required(func):
    # 让被装饰的函数名的属性不会被改变，
    @functools.wraps(func)
    def inner(*args, **kwargs):
        user = session.get('user')
        if not user:
            return redirect('/admin/user/login')
        return func(*args, **kwargs)

    return inner


# 读取上传后加密的文件名
def change_filename(filename):
    dt = datetime.now()
    time = dt.strftime('%Y%m%d%H%M%S')
    filename = time + filename
    return filename


# 七牛上传方法
def qiniu_upload(file_path):
    access_key = constants.ACCESS_KET
    secret_key = constants.SECRET_KEY
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = constants.BUCKET_NAME
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    ret, info = put_data(token, None, file_path)

    if info.status_code == 200:
        # 表示上传成功， 返回文件名
        # 我们上传成功之后, 需要在别的页面显示图像, 因此需要返回图像名
        return ret.get("key")
    else:
        # 表示上传失败
        raise Exception("上传失败")
