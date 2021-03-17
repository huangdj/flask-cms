from flask import render_template, request, flash, redirect, json, jsonify
from . import project_blue
from app.utils.common import login_required
from app.models import Project, Gallery
from app import db
import re


# 项目列表
@project_blue.route('/admin/project/')  # 注意这里路由的后面一定要打 / ，否则点击下一页的时候找不到url地址
@login_required
def index():
    page = int(request.args.get('page', 1))  # 当前页数
    per_page = int(request.args.get('per_page', 10))  # 每页显示的数据条数
    keyword = request.args.get('keyword')
    if keyword:
        where = Project.name.like("%" + keyword + "%")
        paginate = Project.query.filter(where).order_by(-Project.id).paginate(page, per_page, error_out=False)
        projects = paginate.items
        return render_template('admin/project/index.html', projects=projects)
    else:
        paginate = Project.query.order_by(-Project.id).paginate(page, per_page)
        projects = paginate.items
    return render_template('admin/project/index.html', projects=projects, paginate=paginate, error_out=True)


# 新增项目
@project_blue.route('/admin/project/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        area_id = request.form['area_id']
        image = request.form['image']
        scale = request.form['scale']
        unit = request.form['unit']
        service = request.form['service']
        description = request.form['description']
        imgs = re.findall('(https.*?)\"', str(request.form.getlist('imgs')))  # 获取前端上传的多张图片
        if not name:
            flash('请输入项目名称')
            return redirect(request.referrer)

        # 往 project 表中插值
        project = Project(name=name, image=image, type_id=type_id, area_id=area_id, scale=scale, unit=unit,
                          service=service, description=description)
        db.session.add(project)
        db.session.commit()
        p = project.to_dict()

        # 循环往 gallery 表中插值
        for img in imgs:
            gallery = Gallery(imgs=img, project_id=p['id'])
            db.session.add(gallery)
            db.session.commit()

        flash('新增成功')
        return redirect('/admin/project')

    return render_template('admin/project/create.html')


# 编辑
@project_blue.route('/admin/project/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        project = Project.query.filter_by(id=id).first()

        project.name = request.form['name']
        project.type_id = request.form['type_id']
        project.area_id = request.form['area_id']
        project.image = request.form['image']
        project.scale = request.form['scale']
        project.unit = request.form['unit']
        project.service = request.form['service']
        project.description = request.form['description']

        db.session.commit()

        p = project.to_dict()

        imgs = re.findall('(https.*?)\"', str(request.form.getlist('imgs')))  # 获取前端上传的多张图片
        # 循环往 gallery 表中插值
        for img in imgs:
            gallery = Gallery(imgs=img, project_id=p['id'])
            db.session.add(gallery)
            db.session.commit()

        flash('编辑成功')
        return redirect('/admin/project')

    project = Project.query.filter(Project.id == id).first()
    galleries = project.gallery
    return render_template('admin/project/edit.html', project=project, galleries=galleries)


# 删除相册
@project_blue.route('/admin/project/del_gallery', methods=['DELETE'])
def del_gallery():
    data = json.loads(request.get_data())
    obj = Gallery.query.filter_by(id=data['id']).first()
    db.session.delete(obj)
    db.session.commit()
    return jsonify(status=1, msg='删除成功')


# 删除项目，同时删除关联的相册
@project_blue.route('/admin/project/delete/<int:id>')
def delete(id):
    obj = Project.query.filter(Project.id == id).first()
    db.session.delete(obj)
    db.session.commit()
    flash('删除成功')
    return redirect('/admin/project')


# 批量删除
@project_blue.route('/admin/project/destroy_checked', methods=['DELETE'])
def delete_checked():
    data = request.values.get('checked_ids').split(',')
    # print(data)
    # print(type(data))

    for value in data:
        obj = Project.query.filter(Project.id == value).first()
        db.session.delete(obj)
        db.session.commit()

    return jsonify(status=1, msg='删除成功')
