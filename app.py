from __future__ import unicode_literals
from flask import Flask, render_template, request, send_from_directory
import youtube_dl
import os, re, time

app = Flask(__name__)

def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f) and (os.stat(f).st_mtime < time.time() - 3600):
            os.remove(os.path.join(directory, f))

    #purge('.', '[a-zA-Z0-9]*.mp4')


@app.route("/")
def index():
    purge('.', '[a-zA-Z0-9]*.mp4')
    purge('.', '[a-zA-Z0-9]*.mp3')

    return render_template('index.html')

@app.route("/convert_mp3", methods=['POST'])
def mp3():
    video_url = str(request.form['mp3_url'])

    ydl_opts = {
    'forcefilename': True,
    'restrictfilenames': True,
    'format': 'bestaudio/best',
    'outtmpl': 'download_mp3/%(id)s.%(ext)s',
    'postprocessors':
        [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)

    return info_dict['display_id'] + '.mp3'

@app.route("/download_mp3/<path>", methods=['GET'])
def download_mp3(path):
    #path = path.replace('/', '').replace('?', '')
    temp = path.split('.')
    if len(temp) > 2 or temp[1] != 'mp3':
        return 'invalid file'
    return send_from_directory('download_mp3', path)

@app.route("/convert_mp4", methods=['POST'])
def mp4():
    video_url = str(request.form['mp4_url'])

    ydl_opts = {
    'forcefilename': True,
    'restrictfilenames': True,
    'format': 'best',
    'outtmpl': 'download_mp4/%(id)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)

    return info_dict['display_id'] + '.mp4'


@app.route("/download_mp4/<path>", methods=['GET'])
def download_mp4(path):
    #path = path.replace('/', '').replace('?', '')
    temp = path.split('.')
    if len(temp) > 2 or temp[1] != 'mp4':
        return 'invalid file'
    return send_from_directory('download_mp4', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False,port=80)
