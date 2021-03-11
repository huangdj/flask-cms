from flask_script import Manager  # 导入扩展，可以使用管理器启动项目
from flask_migrate import MigrateCommand, Migrate  # 导入迁移包
from app import create_app, db  # 导入db函数

app = create_app('development')  # 调用函数，获取实例
manage = Manager(app)  # 实例化管理器

Migrate(app, db)  # 注入框架实例和数据实例
manage.add_command('db', MigrateCommand)  # 添加迁移命令


@app.route('/')
def index():
    return 'Hello Clwy!'


if __name__ == '__main__':
    manage.run()
