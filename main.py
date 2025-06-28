from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import uuid
from pytube import YouTube

app = Flask(__name__)
DOWNLOAD_FOLDER = "down"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route('/download', methods=['GET'])
def download_spotify():
    url = request.args.get('url')
    if not url:
        return jsonify({'status': 'error: no url param'}), 400

    session_id = str(uuid.uuid4())

    try:
        # Baixa o vídeo usando yt-dlp
        result = subprocess.run(
            ['yt-dlp', '-f', 'mp4', '-o', f'{DOWNLOAD_FOLDER}/{session_id}.%(ext)s', url],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        return jsonify({
            'status': 'ok',
            'file_url': f'/file/{session_id}.mp4'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/file/<filename>')
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    print(file_path)
    if not os.path.exists(file_path):
        return jsonify({'status': 'error: no file'}), 404
    return send_from_directory(DOWNLOAD_FOLDER, filename)

@app.route('/')
def index():
    return jsonify({'status': 'bad use: API SPDL online. Use /download?url=...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)