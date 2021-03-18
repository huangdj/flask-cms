from flask import render_template, request, flash, redirect
from . import train_blue  # 导入蓝图对象
from app.utils.common import login_required  # 引入装饰器
from app.models import Train
from app import db
from datetime import datetime


# 首页
@train_blue.route('/admin/train')
@login_required
def index():
    trains = Train.query.order_by(-Train.id).all()
    trains_count = len(trains)  # 统计数量
    return render_template('admin/train/index.html', trains=trains, trains_count=trains_count)


# 新增
@train_blue.route('/admin/train/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        test_id = request.form['test_id']
        image = request.form['image']
        create_time = request.form['create_time'] if request.form['create_time'] else datetime.now()
        content = request.form['content']

        if not title:
            flash('请输入标题')
            return redirect(request.referrer)

        if not content:
            flash('请输入内容')
            return redirect(request.referrer)

        train = Train(title=title, test_id=test_id, image=image, create_time=create_time, content=content)
        db.session.add(train)
        db.session.commit()
        flash('新增成功')
        return redirect('/admin/train')
    return render_template('admin/train/create.html')


# 编辑
@train_blue.route('/admin/train/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        train = Train.query.filter_by(id=id).first()
        train.title = request.form['title']
        train.test_id = request.form['test_id']
        train.image = request.form['image']
        train.create_time = request.form['create_time'] if request.form['create_time'] else datetime.now()
        train.content = request.form['content']
        db.session.commit()
        flash('编辑成功')
        return redirect('/admin/train')

    train = Train.query.filter(Train.id == id).first()
    return render_template('admin/train/edit.html', train=train)
