# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate
# from models import db, Message
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/messages')
# def messages():
#     if request.method == 'GET':
#         messages = Message.query.order_by(Message.created_at.asc()).all()
#         messages_list = [message.to_dict() for message in messages]
#         return jsonify(messages_list), 200

#     if request.method == 'POST':
#         data = request.get_json()
#         new_message = Message(
#             body=data.get('body'),
#             username=data.get('username'),
#             created_at=datetime.utcnow()
#         )
#         db.session.add(new_message)
#         db.session.commit()
#         return jsonify(new_message.to_dict()), 201

# @app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
# def messages_by_id(id):
#     message = Message.query.get_or_404(id)

#     if request.method == 'GET':
#         return jsonify(message.to_dict()), 200

#     if request.method == 'PATCH':
#         data = request.get_json()
#         message.body = data.get('body', message.body)
#         db.session.commit()
#         return jsonify(message.to_dict()), 200

#     if request.method == 'DELETE':
#         db.session.delete(message)
#         db.session.commit()
#     return make_response ('', 204)

# if __name__ == '__main__':
#     app.run(port=5555)

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list = [message.to_dict() for message in messages]
        return jsonify(messages_list), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid input"}), 400)

        new_message = Message(
            body=data.get('body'),
            username=data.get('username'),
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    session = Session(db.engine)  # Create a new session
    message = session.get(Message, id)  # Use the new get method

    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if request.method == 'GET':
        return jsonify(message.to_dict()), 200

    if request.method == 'PATCH':
        data = request.get_json()
        message.body = data.get('body', message.body)
        session.commit()
        return jsonify(message.to_dict()), 200

    if request.method == 'DELETE':
        session.delete(message)
        session.commit()
        return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5555)
