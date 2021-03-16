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
    name = db.Column(db.String(255), unique=True, nullable=False)  # 类型名称
    image = db.Column(db.String(255), unique=True, nullable=False)  # 缩略图


class Area(BaseModel, db.Model):
    """区域表"""
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), unique=True, nullable=False)  # 类型名称


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
    gallery = db.relationship("Gallery", backref="project")
    type = db.relationship("Type", backref="project")
    area = db.relationship("Area", backref="project")

    def to_dict(self):
        resp_dict = {
            "id": self.id,
        }
        return resp_dict


class Gallery(BaseModel, db.Model):
    """项目相册表"""
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # 所属项目
    imgs = db.Column(db.String(255), unique=True, nullable=False)  # 相册地址
