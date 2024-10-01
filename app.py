from flask import Flask, render_template, request, jsonify, send_from_directory , make_response
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# JSONファイルの保存先
SAVE_DIR = 'data'
IMAGE_DIR = os.path.join(SAVE_DIR, 'images')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
JSON_FILE = os.path.join(SAVE_DIR, 'prompts.json')

# データの初期化
data = []
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_prompt():
    title = request.form['title']
    prompt = request.form['prompt']

    # タイトルの重複チェック
    if any(item['title'] == title for item in data):
        return jsonify({'status': 'Error', 'message': 'Title already exists'})

    # ファイルがアップロードされた場合、保存する
    file = request.files.get('image')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(IMAGE_DIR, filename)
        file.save(file_path)
        # URLパスを保存
        image_path = f"/images/{filename}"
    else:
        image_path = request.form['image_path']

    new_data = {'title': title, 'prompt': prompt, 'image_path': image_path}
    data.append(new_data)
    save_data()
    return jsonify({'status': 'OK'})

@app.route('/copy/<int:index>', methods=['GET'])
def copy_prompt(index):
    prompt_data = data[index]
    return jsonify(prompt_data)

@app.route('/images/<filename>')
def uploaded_file(filename):
    # Serve the image with headers to disable caching
    response = make_response(send_from_directory(IMAGE_DIR, filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

def save_data():
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/get_prompts')
def get_prompts():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
