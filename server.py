import os
import time
from flask import Flask, request, redirect, url_for
import base64
from werkzeug import secure_filename
from werkzeug.serving import run_simple

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
        file.close()  
    return

if __name__ == '__main__':
    run_simple('10.20.199.201',8000,app)