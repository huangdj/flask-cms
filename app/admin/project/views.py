from flask import render_template, request, flash, redirect
from . import project_blue
from app.utils.common import login_required
from app.models import Project, Gallery
from app import db


# 项目列表
@project_blue.route('/admin/project')
@login_required
def index():
    return render_template('admin/project/index.html')


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
        imgs = request.form.getlist('imgs')  # 获取前端上传的多张图片
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
