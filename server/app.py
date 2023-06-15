from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

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
        msgs = [msg.to_dict() for msg 
                in Message.query.order_by("created_at").all()]
        return make_response(msgs, 200)
    else: 
        data = request.get_json()
        new_msg = Message(
            body=data.get("body"),
            username=data.get("username")
        )
        db.session.add(new_msg)
        db.session.commit()
        return make_response(new_msg.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = db.session.get(Message, id)
    
    if msg and request.method == 'PATCH':
        for attr in request.get_json(): 
            setattr(msg, attr, request.get_json().get(attr))
        db.session.add(msg)
        db.session.commit()
        return make_response(msg.to_dict(), 200)
    
    elif msg and request.method == 'DELETE': 
        db.session.delete(msg)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }
        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555)
