import os
import time
from flask import Flask, request, redirect, url_for
import base64
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose

import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, User-Agent")
    response.headers.add("Access-Control-Allow-Methods", "GET, PUT, DELETE, OPTIONS")
    return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        code = request.get_data()
        img=base64.b64decode(code.decode().split(',')[1])
        file=open('images/'+time.strftime("%Y%m%d%H%M%S")+'.jpg','wb')  
        file.write(img)  
        

        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb
        # create pose estimator

        image_size = image.shape
        pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)
        # load model

        pose_estimator.initialise()
        # estimation

        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
        # close model

        pose_estimator.close()
        # Show 2D and 3D poses
        
        file.close() 
        return (image, pose_2d, visibility, pose_3d)

if __name__ == '__main__':
    run_simple('*',8000,app)