from flask import session, redirect
import functools
from datetime import datetime


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
