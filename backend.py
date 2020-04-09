from flask import Flask, render_template, request
import os
import base64
import re
from io import BytesIO
import cv2
from PIL import Image
import sys
sys.path.insert(1, 'model')
from predict import main

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'static/img'

@app.route("/", methods=['GET', 'POST']) #main page
def home():
    return render_template('index.html')

@app.route("/detect", methods=['GET', 'POST']) #detection
def detection():
    
    if request.method == "POST":

            img_name = "filename.png"

            image_b64 = request.values['image']
            image_b64 = re.sub('^data:image/.+;base64,', '', image_b64)   
            image_data = BytesIO(base64.b64decode(image_b64))
            image = Image.open(image_data)

            image.show()
            image = image.save(os.path.join(app.config['IMAGE_UPLOADS'], img_name))

            main(image_data)

    return render_template('index.html')
    
if __name__ == "__main__":
        app.run()