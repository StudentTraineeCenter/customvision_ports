from flask import Flask, render_template, request
import os
import base64
import re
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
import sys
sys.path.insert(1, 'python')
from predict import main
from helpfuncs import draw_boxes #extra functions used


app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'static/img/user_img'

@app.route("/")
def home():
    
    for file in os.listdir(app.config['IMAGE_UPLOADS']): #deleting images loaded from user before

        file_path = os.path.join(app.config['IMAGE_UPLOADS'], file)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:

            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    return render_template('index.html')


@app.route("/camera", methods=['GET', 'POST']) #main page
def camera():
    return render_template('camera.html')


@app.route("/detect", methods=['GET', 'POST']) #detection
def detection():
    
    if request.method == 'POST':

            image_b64 = request.values['image']
            img_test = image_b64
            image_b64 = re.sub('^data:image/.+;base64,', '', image_b64) #cutting the metadata
            image_data = BytesIO(base64.b64decode(image_b64)) 
            
            image = Image.open(image_data)
            image.show()
            predictions = main(image_data)
            image = draw_boxes(image_data, predictions)

            if image == None: return render_template('choice.html')

            image = image.convert("RGB")
            #buffered = BytesIO()
            #image.save(buffered, format="JPEG") 
            #image_url = base64.b64encode(buffered.getvalue())
            #image_url = str("^data:image/.+;base64,", encoding='utf-8') + image_url
            #image_url = "^data:image/.+;base64," + image_url
            image = image.save(os.path.join(app.config['IMAGE_UPLOADS'], '{}.jpg'.format(predictions[0]['probability'])))

            return render_template('choice.html', user_image=os.path.join(app.config['IMAGE_UPLOADS'], '{}.jpg'.format(predictions[0]['probability']))
            ,port1=predictions[0]['tagName'], port2=predictions[1]['tagName'])
    

if __name__ == "__main__":
        app.run()