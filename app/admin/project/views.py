from flask import render_template, request, flash, redirect, json, jsonify
from . import project_blue
from app.utils.common import login_required
from app.models import Project, Gallery
from app import db
import re


# 项目列表
@project_blue.route('/admin/project/')
@login_required
def index():
    # 按关键词搜索
    keyword = request.args.get('keyword')
    if keyword:
        where = Project.name.like("%" + keyword + "%")
        projects = Project.query.filter(where).order_by(-Project.id).all()
        return render_template('admin/project/index.html', projects=projects)
    else:
        projects = Project.query.order_by(-Project.id).all()
    return render_template('admin/project/index.html', projects=projects)


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
