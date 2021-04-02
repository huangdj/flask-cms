from datetime import datetime
from werkzeug.security import check_password_hash
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """管理员"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Type(BaseModel, db.Model):
    """类型表"""
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), nullable=False)  # 类型名称
    image = db.Column(db.String(255), nullable=False)  # 缩略图


class Area(BaseModel, db.Model):
    """区域表"""
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), nullable=False)  # 类型名称


class Project(BaseModel, db.Model):
    """项目表"""
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)  # 所属类型
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)  # 所属区域
    name = db.Column(db.String(255), unique=True, nullable=False)  # 名称
    image = db.Column(db.String(255), nullable=False)  # 缩略图
    scale = db.Column(db.String(255), nullable=False)  # 规模
    unit = db.Column(db.String(255), nullable=False)  # 单位
    service = db.Column(db.String(255), nullable=False)  # 服务
    description = db.Column(db.Text(), nullable=False)  # 描述
    # 创建关系属性  relationship("关联的类名", backref="对方表查询关联数据时的属性名")
    type = db.relationship("Type", backref="project")
    area = db.relationship("Area", backref="project")
    gallery = db.relationship("Gallery", backref="project", cascade="delete, delete-orphan", single_parent=True,
                              lazy='dynamic')  # 删除项目的时候，对应关联的相册也一并删除，注意底下的 ondelete='cascade' 也要定义

    def to_dict(self):
        resp_dict = {
            "id": self.id,
        }
        return resp_dict


class Gallery(BaseModel, db.Model):
    """项目相册表"""
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='cascade'))  # 所属项目
    imgs = db.Column(db.String(255), nullable=False)  # 相册地址


class Train(BaseModel, db.Model):
    """培训服务表"""
    __tablename__ = "train"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), nullable=False)  # 标题
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)  # 培训类型
    image = db.Column(db.String(255), nullable=False)  # 缩略图
    content = db.Column(db.Text(), nullable=False)  # 内容
    test = db.relationship("Test", backref="train")  # 关联服务类型模型


class Test(BaseModel, db.Model):
    """服务类型表"""
    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), nullable=False)  # 类型名称


class Chat(BaseModel, db.Model):
    """留言表"""
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)  # 所属类型
    title = db.Column(db.String(255), nullable=False)  # 标题
    content = db.Column(db.Text(), nullable=False)  # 内容
    is_show = db.Column(db.Integer, default=1, nullable=False)  # 是否显示

    def to_json(self):
        return {
            "id": self.id,
            "type_id": self.type_id,
            "title": self.title,
            "content": self.content,
            "is_show": self.is_show,
            "create_time": self.create_time.strftime("%Y-%m-%d")
        }
