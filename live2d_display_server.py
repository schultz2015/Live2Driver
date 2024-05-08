import json
import threading
import os
import flask
import base64
from flask import Flask, send_from_directory, request
import numpy as np
import tensorflow.compat.v1 as tf

from utils import getJson,getAddress
from emodetect import open
from GUI.panel import start_in_thread2


# flags = tf.app.flags
# flags.DEFINE_string('MODE', 'demo',
#                     'Set program to run in different mode, include train, valid and demo.')
# flags.DEFINE_string('checkpoint_dir', './ckpt',
#                     'Path to model file.')
# flags.DEFINE_string('train_data', './data/fer2013/fer2013.csv',
#                     'Path to training data.')
# flags.DEFINE_string('valid_data', './valid_sets/',
#                     'Path to training data.')
# flags.DEFINE_boolean('show_box', False,
#                     'If true, the results will show detection box')
# FLAGS = flags.FLAGS

app = Flask(__name__, static_folder='./dist')




@app.route('/')
def index():
    return flask.render_template("index.html")
    # return app.send_static_file('index.html')
    return app.send_static_file('main.js')
    return app.send_static_file('custom.css')
    return app.send_static_file('live2dcubismcore.js')
    # return app.send_static_file('vite.svg')


@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory('./dist/assets', path)


# @app.route('/api/get_mouth_y')
# def api_get_one_account():
#     with open("tmp.txt", "r") as f:
#         return json.dumps({
#             "y": f.read()
#         })


@app.route('/api/data', methods=['POST','GET'])
def get_data():
    data = request.get_data()
    string = data.decode("utf-8")
    image_data=string[6:].replace("%2B", "+").replace("%2F", "/").replace("%3D", "=").encode('utf-8')
    image_data=base64.b64decode(image_data)
    np_array = np.frombuffer(image_data, np.uint8)
    # 使用OpenCV的imdecode函数将numpy数组转换为OpenCV的图像格式
    # image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    # frame = image.tobytes()
    # yield (b'--frame\r\n'
    #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    re= open(np_array)
    print("return",re)
    return re

@app.route('/api/address', methods=['POST','GET'])
def address():
    data=getAddress()
    return data


@app.route('/api/model', methods=['POST','GET'])
def model():
    address=request.get_json()
    data=getJson(address)
    return data

# @app.route('/video_feed0')
# def video_feed0():
#     return Response(gen_frames0(),mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(port=4800, debug=True, host="0.0.0.0", use_reloader=False)

if __name__ == '__main__':
    main()



