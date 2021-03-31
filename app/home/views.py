from flask import render_template
from . import home_blue  # 导入蓝图对象
from app.models import Project, Type, Gallery


@home_blue.route('/')
def index():
    # 所有项目
    projects = Project.query.order_by(-Project.id).limit(10).all()
    # 所有类型
    types = Type.query.limit(4).all()
    return render_template('home/index/index.html', projects=projects, types=types)


# 项目详情页
@home_blue.route('/show/<int:id>')
def show_project(id):
    # 查出当前要查看的数据，包括相册
    project = Project.query.filter(Project.id == id).first()
    galleries = Gallery.query.filter(Gallery.project_id == id).all()

    other_projects = Project.query.filter(Project.id != id).all()
    return render_template('home/project/show.html', project=project, galleries=galleries,
                           other_projects=other_projects)


# 类型对应的项目
@home_blue.route('/type/<int:id>')
def show_type(id):
    if id == 3:
        projects = Project.query.filter(Project.type_id == 3).all()
    elif id == 4:
        projects = Project.query.filter(Project.type_id == 4).all()
    elif id == 5:
        projects = Project.query.filter(Project.type_id == 5).all()
    else:
        projects = Project.query.filter(Project.type_id == 5).all()
    return render_template('home/project/type.html', projects=projects)
