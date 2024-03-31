import base64
import time
import uuid
import jwt
import os

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

port = int(os.environ.get('PORT', 5000))

db_config = {
  'host': os.environ.get('DB_HOST', 'mysql-service'),
  'user': os.environ.get('DB_USER', 'root'),
  'password': os.environ.get('DB_PASSWORD', ''),
  'database': os.environ.get('DB_DATABASE', 'traveltours'),
}

db = None
cursor = None

while db is None:
  try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    print("Database connection successful!")
  except mysql.connector.Error as err:
    print("Error connecting to the database: {}".format(err))
    print("Retrying database connection in 5 seconds...")
    time.sleep(5)

active_sessions = {}
secret_key = 'your_secret_key'

@app.route('/api/user/login', methods=['POST'])
def user_login():
  data = request.get_json()

  username = data.get('username')
  password = data.get('password')

  try:
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and user['password'] == password:
      is_admin = user['isadmin'] == 1
      payload = {'username': username, 'isadmin': is_admin}
      token = jwt.encode(payload, secret_key, algorithm='HS256')
      session_id = str(uuid.uuid4())

      response_data = {
        'success': True,
        'session_id': session_id,
        'token': token,
        'message': 'Login successful',
        'username': username,
        'isadmin': is_admin
      }
      return jsonify(response_data)
    else:
      return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
  except Exception as e:
    return jsonify({'success': False, 'error': 'An error occurred while processing your request'}), 500

@app.route('/api/user/logout', methods=['POST'])
def logout():
  data = request.get_json()
  username = data.get('username')
  try:
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
      return jsonify({'success': True, 'message': 'Logout successful'})
    else:
      return jsonify({'success': False, 'error': 'User not found'}), 404

  except Exception as e:
    return jsonify({'success': False, 'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=port)
