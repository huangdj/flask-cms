from flask import jsonify, request, json
from . import api_blue
from app.models import Chat, Type  # 引入模型
from app import db


# 多条数据转换成 json
def class_to_dict(obj):
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            a = o.__dict__
            if "_sa_instance_state" in a:
                del a['_sa_instance_state']
            dict.update(a)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        a = obj.__dict__
        if "_sa_instance_state" in a:
            del a['_sa_instance_state']
        dict.update(a)


# 所有留言
@api_blue.route('/api')
def index():
    chats = Chat.query.order_by(Chat.create_time).all()
    data = {
        'chats': class_to_dict(chats),
    }
    return jsonify(data)


# 所有类型
@api_blue.route('/api/type')
def type():
    types = Type.query.all()
    data = {
        'types': class_to_dict(types),
    }
    return jsonify(data)


# 发布留言
@api_blue.route('/api/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        chat = Chat()
        chat.title = data['title']
        chat.type_id = data['type_id']
        chat.content = data['content']
        chat.is_show = data['is_show']

        db.session.add(chat)
        db.session.commit()
        info = {
            'chat': chat.to_json()
        }
        return jsonify(info)


# 编辑留言
@api_blue.route('/api/edit/<int:id>')
def edit(id):
    chat = Chat.query.filter(Chat.id == id).first()
    info = {
        'chat': chat.to_json()
    }
    return jsonify(info)


# 保存留言
@api_blue.route('/api/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        chat = Chat.query.filter(Chat.id == data['id']).first()

        chat.title = data['title']
        chat.type_id = data['type_id']
        chat.content = data['content']
        chat.is_show = data['is_show']

        db.session.commit()
        info = {
            'chat': chat.to_json()
        }
        return jsonify(info)


# 删除
@api_blue.route('/api/delete/<int:id>', methods=['DELETE'])
def delete(id):
    obj = Chat.query.filter(Chat.id == id).first()
    db.session.delete(obj)
    db.session.commit()
