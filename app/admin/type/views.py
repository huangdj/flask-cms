from flask import render_template, request, flash, redirect
from . import type_blue  # 导入蓝图对象
from app.utils.common import login_required  # 引入装饰器
from app.models import Type
from app import db


# 首页
@type_blue.route('/admin/type')
@login_required
def index():
    types = Type.query.order_by(-Type.id).all()
    return render_template('admin/type/index.html', types=types)


# 新增
@type_blue.route('/admin/type/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        if not name:
            flash('请输入类型名称')
            return redirect(request.referrer)

        type = Type(name=name, image=image)
        db.session.add(type)
        db.session.commit()
        flash('新增成功')
        return redirect('/admin/type')

    return render_template('admin/type/add.html')


# 编辑
@type_blue.route('/admin/type/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        type = Type.query.filter_by(id=id).first()
        type.name = request.form['name']
        type.image = request.form['image']
        db.session.commit()
        flash('编辑成功')
        return redirect('/admin/type')

    type = Type.query.filter(Type.id == id).first()
    return render_template('admin/type/edit.html', type=type)
