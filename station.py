from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder='template')

@app.route('/stations/', methods=['GET', 'POST'])
def showSubwaystation():
    items = []
    if request.method == 'POST':
        db = sqlite3.connect('subway_station.db')
        cursor = db.cursor()
        items = cursor.execute('SELECT distinct 역명 from 편의시설 where 역명 like (?)', ('%' + request.form['name'] + '%',)).fetchall()
        db.close()
    return render_template('search_station.html', stations = items)

@app.route('/stations/<string:station_name>/', methods=['GET', 'POST'])
def showInformation(station_name):
    items = []
    columns = []
    if request.method == 'POST':
        db = sqlite3.connect('subway_station.db')
        cursor = db.cursor()
        if 'save' in request.form:
            # 즐겨찾기 테이블에 추가
            favorite_item = request.form['favorite_item']  # 저장할 데이터 가져오기
            cursor.execute('INSERT OR IGNORE INTO 즐겨찾기 (역명) VALUES (?)',(favorite_item,))

        else:
            category = request.form['category']
            items = cursor.execute(f'SELECT * FROM {category} WHERE 역명 LIKE (?)', (station_name + '%',)).fetchall()
            cursor.execute(f'PRAGMA table_info({category})')
            columns = [row[1] for row in cursor.fetchall()]
        db.commit()
        db.close()

    return render_template('information_station.html', station_name = station_name, informations = items, columns = columns)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port = 5000)