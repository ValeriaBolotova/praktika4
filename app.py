from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils.encryption import vigenere_encrypt, vigenere_decrypt, shift_encrypt, shift_decrypt, get_alphabet, break_shift_cipher
from datetime import datetime
from models import db, User, Session
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///encryption_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

methods = [
    {"id": 1, "name": "vigenere", "caption": "Vigenere Cipher", "params": {"key": "str"},
     "description": "Шифрование методом Виженера"},
    {"id": 2, "name": "shift", "caption": "Shift Cipher", "params": {"shift": "int"},
     "description": "Шифрование методом сдвига"}
]

def is_unique_login(login):
    return User.query.filter_by(login=login).first() is None

def is_unique_secret(secret):
    return User.query.filter_by(secret=secret).first() is None

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not is_unique_login(data['login']) or not is_unique_secret(data['secret']):
        return jsonify({"error": "Login or Secret must be unique"}), 400
    user = User(login=data["login"], secret=data["secret"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "login": user.login}), 201

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"login": user.login, "id": user.id} for user in users]), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/methods', methods=['GET'])
def list_methods():
    return jsonify(methods), 200

@app.route('/sessions', methods=['POST'])
def create_session():
    data = request.json
    user_id = data.get("user_id")
    method_id = data.get("method_id")
    text = data.get("text")
    params = data.get("params")
    operation = data.get("operation", "encrypt")
    language = data.get("language", "en")

    method = next((m for m in methods if m["id"] == method_id), None)
    if not method:
        return jsonify({"error": "Unknown method"}), 400

    try:
        alphabet = get_alphabet(language)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    start_time = datetime.now()

    if method["name"] == "vigenere":
        key = params.get("key")
        if operation == "encrypt":
            result_text = vigenere_encrypt(text, key, alphabet)
        else:
            result_text = vigenere_decrypt(text, key, alphabet)
    elif method["name"] == "shift":
        shift = params.get("shift")
        if operation == "encrypt":
            result_text = shift_encrypt(text, shift, alphabet)
        else:
            result_text = shift_decrypt(text, shift, alphabet)
    else:
        return jsonify({"error": "Unknown method"}), 400

    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()

    session = Session(
        user_id=user_id,
        method_id=method_id,
        data_in=text,
        params=json.dumps(params),
        data_out=result_text,
        status="completed",
        created_at=start_time,
        time_out=elapsed_time
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        "id": session.id,
        "user_id": session.user_id,
        "method_id": session.method_id,
        "data_in": session.data_in,
        "params": session.params,
        "data_out": session.data_out,
        "status": session.status,
        "created_at": session.created_at.isoformat(),
        "time_out": session.time_out
    }), 201

@app.route('/sessions', methods=['GET'])
def list_sessions():
    sessions = Session.query.all()
    return jsonify([{
        "id": session.id,
        "user_id": session.user_id,
        "method_id": session.method_id,
        "data_in": session.data_in,
        "params": session.params,
        "data_out": session.data_out,
        "status": session.status,
        "created_at": session.created_at.isoformat(),
        "time_out": session.time_out
    } for session in sessions]), 200

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    data = request.json
    secret = data.get("secret")

    session = Session.query.get(session_id)
    if session:
        user = User.query.get(session.user_id)
        if user and user.secret == secret:
            db.session.delete(session)
            db.session.commit()
            return jsonify({"status": "deleted"}), 200
        else:
            return jsonify({"error": "Invalid secret"}), 403
    else:
        return jsonify({"error": "Session not found"}), 404

@app.route('/break', methods=['POST'])
def break_cipher():
    data = request.json
    method_id = data.get("method_id")
    text = data.get("text")
    language = data.get("language", "en")

    method = next((m for m in methods if m["id"] == method_id), None)
    if not method:
        return jsonify({"error": "Unknown method"}), 400

    try:
        alphabet = get_alphabet(language)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if method["name"] == "shift":
        possible_texts = break_shift_cipher(text, alphabet)
        return jsonify({"possible_texts": possible_texts}), 200
    else:
        return jsonify({"error": "Breaking this cipher is not supported"}), 400


if __name__ == '__main__':
    app.run(debug=True)
