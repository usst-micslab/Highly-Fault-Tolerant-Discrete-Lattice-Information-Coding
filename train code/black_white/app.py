from flask import Flask, request, jsonify
from flask_cors import CORS
from encoder import encoded
from decoder import decoded
import cv2
import numpy as np
from PIL import Image
import requests

app = Flask(__name__)

def download_file(url, local_filename):
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 获取响应内容（即 Blob 数据）
        blob_data = response.content

        # 将 Blob 数据写入文件
        with open('local_filename', 'wb') as file:
            file.write(blob_data)

        print(f'图像已成功保存到本地文件 {local_filename}')
    else:
        print('请求失败:', response.status_code)

CORS(app, resources={r'/*': {'origins': '*'}})
@app.route('/')
def index():
    # 传递给模板的数据
    message = "Hello, Flask!"
    print(message)

    # 渲染 HTML 模板，并传递数据给模板
    return message

@app.route('/encoder', methods=['POST'])
def encoder_watermarking():
    data = request.get_json()
    secret = data['watermarking']
    print(secret)
    im = encoded(secret)
    image_array = np.array(im)
    image_list = image_array.tolist()

    return jsonify(image_list)

@app.route('/decoder', methods=['POST'])
def decoder_watermarking():
    file = request.files['file']

    # 保存文件到本地

    local_filename = 'images/222_hidden.png'
    file.save(local_filename)


    code = decoded(local_filename)
    print(code)

    return jsonify(code)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
