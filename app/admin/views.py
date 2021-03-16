from flask import render_template, request, jsonify, json, flash, redirect, session, make_response
from werkzeug.security import generate_password_hash
from app.models import User  # 导入模型
import re  # 导入正则模块
from app import db  # 导入 db
from . import admin_blue  # 导入蓝图对象
from app.utils.common import login_required, change_filename, qiniu_upload
from app.utils.captcha.captcha import captcha  # 导入captcha扩展
from app import redis_store, constants  # 导入redis实例
import os
from werkzeug.utils import secure_filename


# 后台首页路由
@admin_blue.route('/admin')
@login_required
def index():
    return render_template('admin/index/index.html')


# 后台注册
@admin_blue.route('/admin/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if not data['username']:
            return jsonify(status=0, msg='请填写用户名')
        if not data['password']:
            return jsonify(status=0, msg='请填写密码')

        if data['check_password'] != data['password']:
            return jsonify(status=0, msg='两次密码输入不一致')

        if not re.match(r'1[3456789]\d{9}$', data['mobile']):
            return jsonify(status=0, msg='手机号格式错误')

        # 根据手机号进行查询，确认用户是否注册
        user_mobile = User.query.filter_by(mobile=data['mobile']).first()
        if user_mobile:
            return jsonify(status=0, msg='手机号码已被注册')

        # 构造模型类对象，准备存储数据到 user 表中
        user = User()
        user.mobile = data['mobile']
        user.username = data['username']
        user.password = generate_password_hash(data['password'])
        # 把用户数据提交到数据库中
        db.session.add(user)
        db.session.commit()

        return jsonify(status=1, msg='注册成功')
    return render_template('admin/user/register.html')


# 后台登录
@admin_blue.route('/admin/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        captcha = request.form['captcha']  # 接收前端提交过来的验证码
        image_code_id = request.form['image_code_id']  # 接收前端提交过来的 image_code_id

        real_image_code = str(redis_store.get('ImageCode_' + image_code_id))  # 把image_code_id转成字符串，然后存入redis

        # print(real_image_code.lower())
        # print(captcha.lower())

        # 验证码验证
        if real_image_code.lower() != captcha.lower():
            flash('图片验证码不一致')
            return redirect(request.referrer)

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('用户名或密码输入错误')
            return redirect(request.referrer)

        session['user'] = user
        return redirect('/admin')
    return render_template('admin/user/login.html')


# 后台退出
@admin_blue.route('/admin/logout')
def logout():
    # 退出本质就是清除session
    session.pop("user")
    return redirect('/admin/user/login')  # 退出后跳转到登录


# 生成验证码
@admin_blue.route('/admin/image_code')
def generate_image_code():
    image_code_id = request.args.get('image_code_id')  # 获取参数
    if not image_code_id:  # 判断参数是否存在
        return jsonify(status=0, msg='参数缺失')
    name, text, image = captcha.generate_captcha()  # 调用扩展来生成图片验证码
    redis_store.setex('ImageCode_' + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)  # 保存图片验证码到redis
    response = make_response(image)  # 使用响应对象返回图片本身
    response.headers['Content-Type'] = 'image/jpg'  # 设置响应的数据类型
    return response  # 返回响应


# 使用插件上传图片到本地
@admin_blue.route('/admin/photos', methods=['POST'])
@login_required
def photos():
    if request.method == 'POST':
        # 定义上传目录，如果目录不存在，则自动创建
        file_dir = os.path.join(os.getcwd(), constants.UPLOAD_FOLDER)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        image = request.files['image']  # 获取前端提交过来的图片
        filename = secure_filename(change_filename(image.filename))  # 修改图片上传的图片名称
        file_path = os.path.join(constants.UPLOAD_FOLDER, filename)  # 获取上传后的绝对路径
        image.save(file_path)  # 保存到本地
        # 返回本地图片地址给前端
        return jsonify({'image_url': os.path.join('/static/upload', filename)})


# 使用插件上传图片到七牛
@admin_blue.route('/admin/upload_qiniu', methods=['POST'])
@login_required
def upload_qiniu():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            file_data = file.read()
            filename = qiniu_upload(file_data)  # 上传到七牛
            image_url = constants.QINIU_DOMIN_PREFIX + filename
            return jsonify(image_url=image_url)


# 富文本编辑器上传图片到七牛
@admin_blue.route('/admin/submit-image', methods=['GET', 'POST'])
def submit_image():
    '''富文本图片上传方法'''
    file = request.files['file']
    try:
        img = file.read()
        # print(img)
    except Exception:
        return jsonify(status=0, msg="图片读取失败")

    key = qiniu_upload(img)

    img_url = constants.QINIU_DOMIN_PREFIX + key
    return '{"error":false,"path":"' + img_url + '"}'


# 多图上传
@admin_blue.route('/admin/webUploader', methods=['POST'])
@login_required
def webUploader():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_data = file.read()
            filename = qiniu_upload(file_data)  # 上传到七牛
            image_url = constants.QINIU_DOMIN_PREFIX + filename
            return jsonify({'image_url': image_url})
