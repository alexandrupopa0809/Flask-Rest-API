import json

from flask import Flask, request, jsonify, Response
from datetime import date
import mysql.connector
import arrow

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'meteo'
}


@app.route('/api/countries', methods=['GET'])
def get_all_countries():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tari')
    data = cursor.fetchall()
    payload = []
    for result in data:
        content = {}
        content = {'id': result[0], 'nume': result[1], 'lat': result[2],
                   'lon': result[3]}
        payload.append(content)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(payload), 200


@app.route('/api/countries', methods=['POST'])
def add_country():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    data = request.get_json()
    if data and 'nume_tara' in data and 'lat' in data and 'lon' in data:
        name = data['nume_tara']
        lon = data['lon']
        lat = data['lat']
        try:
            cursor.execute('INSERT INTO tari(nume_tara, lat, lon) VALUES (%s, %s, %s)',
                           (name, lat, lon))
            connection.commit()
            id_tara = cursor.lastrowid
            cursor.close()
            connection.close()
            return json.dumps({"id": id_tara}), 201
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/countries/<id>', methods=['PUT'])
def update_country(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    data = request.get_json()

    cursor.execute('SELECT * FROM tari')
    countries = cursor.fetchall()
    for country in countries:
        if int(country[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    if data and 'id' in data and 'nume_tara' in data and 'lat' in data and 'lon' in data:
        request_id = data['id']
        name = data['nume_tara']
        lon = data['lon']
        lat = data['lat']
        if int(request_id) != int(id):
            return Response(status='400')
        try:
            cursor = connection.cursor()
            cursor.execute('UPDATE tari SET nume_tara = %s, lat = %s, lon = %s WHERE id = %s',
                           (name, lat, lon, id))
            connection.commit()
            cursor.close()
            connection.close()
            return Response(status='200')
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/countries/<id>', methods=['DELETE'])
def delete_country(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM tari')
    countries = cursor.fetchall()
    for country in countries:
        if int(country[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('DELETE FROM tari WHERE id = %s', (int(id),))
    connection.commit()
    cursor.close()
    connection.close()
    return Response(status='200')


def country_exists(connection, id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tari')
    countries = cursor.fetchall()
    for country in countries:
        if int(country[0]) == int(id):
            cursor.close()
            return True
    cursor.close()
    return False


@app.route('/api/cities', methods=['POST'])
def add_city():
    connection = mysql.connector.connect(**config)
    data = request.get_json()

    if data and 'id_tara' in data and 'nume_oras' in data and 'lat' in data and 'lon' in data:
        id_tara = data['id_tara']
        if not country_exists(connection, id_tara):
            return Response(status='400')
        name = data['nume_oras']
        lon = data['lon']
        lat = data['lat']
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO orase(id_tara, nume_oras, lat, lon) VALUES (%s, %s, %s, %s)',
                           (id_tara, name, lat, lon))
            connection.commit()
            id_oras = cursor.lastrowid
            cursor.close()
            connection.close()
            return json.dumps({"id": id_oras}), 201
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/cities', methods=['GET'])
def get_all_cities():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM orase')
    data = cursor.fetchall()
    payload = []
    for result in data:
        content = {}
        content = {'id': result[0], 'idTara': result[1], 'nume': result[2], 'lat': result[3],
                   'lon': result[4]}
        payload.append(content)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(payload), 200


@app.route('/api/cities/country/<idTara>', methods=['GET'])
def get_city_by_country(idTara):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM orase""")
    data = cursor.fetchall()
    payload = []
    for result in data:
        content = {}
        content = {'id': result[0], 'idTara': result[1], 'nume': result[2], 'lat': result[3],
                   'lon': result[4]}
        if result[1] == int(idTara):
            payload.append(content)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(payload), 200


@app.route('/api/cities/<id>', methods=['PUT'])
def update_city(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    data = request.get_json()

    cursor.execute('SELECT * from orase')
    cities = cursor.fetchall()
    for city in cities:
        if int(city[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    if data and 'id' in data and 'id_tara' in data and 'nume_oras' in data and 'lat' in data and 'lon' in data:
        request_id = data['id']
        if int(request_id) != int(id):
            return Response(status='400')
        id_tara = data['id_tara']
        if not country_exists(connection, id_tara):
            return Response(status='400')
        name = data['nume_oras']
        lon = data['lon']
        lat = data['lat']
        try:
            cursor = connection.cursor()
            cursor.execute('UPDATE orase SET id_tara = %s, nume_oras = %s, lat = %s, lon = %s WHERE id = %s',
                           (id_tara, name, lat, lon, id))
            connection.commit()
            cursor.close()
            connection.close()
            return Response(status='200')
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM orase')
    cities = cursor.fetchall()
    for city in cities:
        if int(city[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('DELETE FROM orase WHERE id = %s', (int(id),))
    connection.commit()
    cursor.close()
    connection.close()
    return Response(status='200')


def city_exists(connection, id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM orase')
    cities = cursor.fetchall()
    for city in cities:
        if int(city[0]) == int(id):
            cursor.close()
            return True
    cursor.close()
    return False


@app.route('/api/temperatures', methods=['POST'])
def add_temperature():
    connection = mysql.connector.connect(**config)
    data = request.get_json()

    if data and 'id_oras' in data and 'valoare' in data:
        id_oras = data['id_oras']
        if not city_exists(connection, id_oras):
            return Response(status='400')
        valoare = data['valoare']
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO temperaturi(valoare, timestamp, id_oras) VALUES (%s, %s, %s)',
                           (valoare, str(arrow.now().format('YYYY-MM-DD')), id_oras,))
            connection.commit()
            id_temp = cursor.lastrowid
            cursor.close()
            connection.close()
            return json.dumps({"id": id_temp}), 201
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/temperatures/<id>', methods=['PUT'])
def update_temperature(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    data = request.get_json()

    cursor.execute('SELECT * from temperaturi')
    temps = cursor.fetchall()
    for temp in temps:
        if int(temp[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    if data and 'id' in data and 'id_oras' in data and 'valoare' in data:
        request_id = data['id']
        if int(request_id) != int(id):
            return Response(status='400')
        id_oras = data['id_oras']
        if not city_exists(connection, id_oras):
            return Response(status='400')
        valoare = data['valoare']
        try:
            cursor = connection.cursor()
            cursor.execute('UPDATE temperaturi SET id_oras = %s, valoare = %s WHERE id = %s',
                           (id_oras, valoare, id))
            connection.commit()
            cursor.close()
            connection.close()
            return Response(status='200')
        except mysql.connector.IntegrityError:
            return Response(status='409')
    return Response(status='400')


@app.route('/api/temperatures/<id>', methods=['DELETE'])
def delete_temperature(id):
    id_exist = False

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM temperaturi')
    temps = cursor.fetchall()
    for temp in temps:
        if int(temp[0]) == int(id):
            id_exist = True
    if not id_exist:
        return Response(status='404')
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('DELETE FROM temperaturi WHERE id = %s', (int(id),))
    connection.commit()
    cursor.close()
    connection.close()
    return Response(status='200')


@app.route('/api/temperatures', methods=['GET'])
def get_all_temperatures():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM temperaturi')
    data = cursor.fetchall()
    payload = []
    for result in data:
        content = {}
        content = {'id': result[0], 'valoare': result[1], 'timestamp': result[2], 'id_oras': result[3]}
        payload.append(content)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(payload), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
