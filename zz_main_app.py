from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime
import os
import music_tag
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zzsqlite3.db'
db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_song = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.now)


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_podcast = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.now)
    host = db.Column(db.String(100), nullable=False)


class Audiobook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_audiobook = db.Column(db.String(100), nullable=False)
    author_title = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.now)


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():
    file = request.files['file']
    file.save(secure_filename(file.filename))
    cwd = os.getcwd()

    files = os.listdir(cwd)

    try:
        f = music_tag.load_file(files[0])
    except Exception as e:
        return 'File not supported', os.remove(files[0])
    statement = 'Action is Successful: 200 OK'

    if str(f['#codec']) == 'mp3':
        if str(request.form['option']) == 'song':
            new_file = Song(name_of_song=str(
                f['tracktitle']), duration=int(f['#length']))
            db.session.add(new_file)
            db.session.commit()
            return render_template('index.html', statement=statement), os.remove(files[0])

        elif str(request.form['option']) == 'podcast':
            new_file = Podcast(name_of_podcast=str(f['tracktitle']), duration=int(
                f['#length']), host=str(f['album']))
            db.session.add(new_file)
            db.session.commit()
            return render_template('index.html', statement=statement), os.remove(files[0])

        elif str(request.form['option']) == 'audiobook':
            new_file = Audiobook(title_audiobook=str(f['tracktitle']), author_title=str(
                f['composer']), narrator=str(f['artist']), duration=int(f['#length']))
            db.session.add(new_file)
            db.session.commit()
            return render_template('index.html', statement=statement), os.remove(files[0])
    else:
        return 'The request is invalid: 400 bad request', os.remove(files[0])

    return 'Internal Server Error', os.remove(files[0])


@app.route('/delete')
def delete():
    return render_template('delete.html')


@app.route('/delete/audioFileType/audioFileID', methods=['POST', 'GET'])
def deleted():
    table = request.form.get('select')
    id = request.form.get('id')
    sqliteConnection = sqlite3.connect('zzsqlite3.db')
    cursor = sqliteConnection.cursor()
    sql_delete_query = "DELETE from "+(table)+" where id ="+(id)
    cursor.execute(sql_delete_query)
    sqliteConnection.commit()
    cursor.close()
    statement = 'Sucessfully Deleted'
    return render_template('delete.html', statement=statement)


@app.route('/get')
def det():
    return render_template('get.html')


@app.route('/get/audioFileType/audioFileID', methods=['POST', 'GET'])
def get():
    table = request.form.get('select')
    id = request.form.get('id')
    sqliteConnection = sqlite3.connect('zzsqlite3.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * from "+table)
    row = cursor.fetchall()
    statement = str(row[int(id)])

    return render_template('get.html', statement=statement)


if __name__ == '__main__':
    app.run(debug=True)
