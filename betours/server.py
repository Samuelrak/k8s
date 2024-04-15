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

port = int(os.environ.get('PORT', 5001))

db_config = {
  'host': os.environ.get('DB_HOST', 'mysql-headless'),
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

@app.route('/api/tours', methods=['GET'])
def display_tours():
  cursor.execute('SELECT id, name, location, continent, start_date, end_date, people, price, photo FROM tours')
  tours = cursor.fetchall()

  for tour in tours:
    if 'photo' in tour and tour['photo'] is not None:
      tour['photo'] = base64.b64encode(tour['photo']).decode('utf-8')

  return jsonify(tours)

@app.route('/api/tours/<int:tour_id>', methods=['GET'])
def view_tour(tour_id):
  cursor.execute('SELECT id, name, location, continent, start_date, end_date, people, price, photo FROM tours WHERE id = %s', (tour_id,))
  tour = cursor.fetchone()

  if tour:
    if 'photo' in tour and tour['photo'] is not None:
      tour['photo'] = base64.b64encode(tour['photo']).decode('utf-8')

    return jsonify(tour), 200
  else:
    return jsonify({'error': 'Tour not found'}), 404

@app.route('/api/tours', methods=['POST'])
def add_tour():
  try:
    name = request.form['name']
    location = request.form['location']
    continent = request.form['continent']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    people = int(request.form['people'])
    price = float(request.form['price'])
    photo = request.files['photo']

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    photo_content = photo.read()

    cursor.execute('''
                  INSERT INTO tours (name, location, continent, start_date, end_date, people, price, photo)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
              ''', (name, location, continent, start_date, end_date, people, price, photo_content))

    db.commit()

    response_data = {
      'status': 'success'
    }
    return jsonify(response_data), 200

  except Exception as e:
    error_message = str(e)
    response_data = {
      'status': 'error',
      'message': error_message
    }
    return jsonify(response_data), 500

@app.route('/api/tours/<int:tour_id>', methods=['DELETE'])
def delete_tour(tour_id):
  try:
    cursor.execute('DELETE FROM tours WHERE id = %s', (tour_id,))
    db.commit()

    response_data = {
      'status': 'success'
    }
    return jsonify(response_data), 200

  except Exception as e:
    error_message = str(e)
    response_data = {
      'status': 'error',
      'message': error_message
    }
    return jsonify(response_data), 500

@app.route('/api/tours/<int:tour_id>', methods=['PUT'])
def update_tour(tour_id):
  try:
    name = request.form['name']
    location = request.form['location']
    continent = request.form['continent']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    people = int(request.form['people'])
    price = float(request.form['price'])
    photo = request.files['photo'] if 'photo' in request.files else None

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")


    if photo:
      photo_content = photo.read()
      cursor.execute('''
                  UPDATE tours
                  SET name = %s, location = %s, continent = %s,
                      start_date = %s, end_date = %s, people = %s,
                      price = %s, photo = %s
                  WHERE id = %s
              ''', (name, location, continent, start_date, end_date, people, price, photo_content, tour_id))
    else:
      cursor.execute('''
                  UPDATE tours
                  SET name = %s, location = %s, continent = %s,
                      start_date = %s, end_date = %s, people = %s,
                      price = %s
                  WHERE id = %s
              ''', (name, location, continent, start_date, end_date, people, price, tour_id))

    db.commit()

    response_data = {
      'status': 'success'
    }

    return jsonify(response_data), 200

  except Exception as e:
    error_message = str(e)
    response_data = {
      'status': 'error',
      'message': error_message
    }

    return jsonify(response_data), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=port)
