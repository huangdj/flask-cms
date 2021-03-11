from flask import Flask
from flask_script import Manager  # 导入扩展，可以使用管理器启动项目
from config import config  # 导入配置信息
from flask_sqlalchemy import SQLAlchemy  # 导入数据库扩展
from flask_migrate import MigrateCommand, Migrate  # 导入迁移包

app = Flask(__name__)
manage = Manager(app)  # 实例化管理器
db = SQLAlchemy(app)  # 注册数据库实例

Migrate(app, db)  # 注入框架实例和数据实例
manage.add_command('db', MigrateCommand)  # 添加迁移命令
app.config.from_object(config['development'])  # 使用配置


@app.route('/')
def index():
    return 'Hello Clwy!'


if __name__ == '__main__':
    manage.run()
