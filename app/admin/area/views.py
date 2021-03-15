from flask import render_template, request, flash, redirect
from . import area_blue  # 导入蓝图对象
from app.utils.common import login_required  # 引入装饰器
from app.models import Area
from app import db


# 首页
@area_blue.route('/admin/area')
@login_required
def index():
    areas = Area.query.order_by(-Area.id).all()
    return render_template('admin/area/index.html', areas=areas)


# 新增
@area_blue.route('/admin/area/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('请输入区域名称')
            return redirect(request.referrer)

        area = Area(name=name)
        db.session.add(area)
        db.session.commit()
        flash('新增成功')
        return redirect('/admin/area')

    return render_template('admin/area/add.html')


# 编辑
@area_blue.route('/admin/area/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        area = Area.query.filter_by(id=id).first()
        area.name = request.form['name']
        db.session.commit()
        flash('编辑成功')
        return redirect('/admin/area')

    area = Area.query.filter(Area.id == id).first()
    return render_template('admin/area/edit.html', area=area)


# 删除
@area_blue.route('/admin/area/delete/<int:id>')
def delete(id):
    obj = Area.query.filter(Area.id == id).first()
    db.session.delete(obj)
    db.session.commit()
    flash('删除成功')
    return redirect('/admin/area')
