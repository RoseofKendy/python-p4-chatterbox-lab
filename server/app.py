from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Optional: makes JSON easier to read

# Initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# GET /messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or 'body' not in data or 'username' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({}), 204

# Run the server
if __name__ == '__main__':
    app.run(port=5555, debug=True)
