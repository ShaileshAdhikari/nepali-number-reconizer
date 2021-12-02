from io import BytesIO
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import numpy as np
import tensorflow as tf
from PIL import Image,ImageOps
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator


app = Flask(__name__)

IMAGE_SIZE = (25,25)
MODEL_PATH = os.path.abspath("..") +'/backend/best-model.h5'

@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html")
    if request.method == 'POST':
        filename = request.form['save_fname']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']

        # Decoding base64 string to bytes object
        img_bytes = base64.b64decode(canvas_image[22:])
        img = Image.open(BytesIO(img_bytes))
        r, g, b, a = img.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        file = "static/images/"+filename
        # Saving Image to desired directory
        rgb_image.save(file)

        conn =  psycopg2.connect(host="127.0.0.1",port=5432,database="nepali_digit",
                                 user = "postgres",password="postgres")
        cur = conn.cursor()
        cur.execute("INSERT INTO files (name, canvas_image) VALUES (%s, %s)", [file, canvas_image])
        conn.commit()
        conn.close()

        return redirect(url_for('identify'))
        
        
@app.route('/identify', methods=['GET', 'POST'])
def identify():
    conn = psycopg2.connect(host="127.0.0.1",port=5432,database="nepali_digit",
                            user = "postgres",password="postgres")
    cur = conn.cursor()
    cur.execute("SELECT id, name, canvas_image from files")
    file = cur.fetchall()

    pred, response = predict(file[-1][1])

    cur.execute("""UPDATE files SET predicted = (%s) WHERE id = (%s);""",(int(pred[0]),int(file[-1][0])))
    conn.commit()
    conn.close()

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin','*')

    return response

def predict(directory):
    img = load_img(directory, target_size=IMAGE_SIZE, color_mode='grayscale')
    img = ImageOps.invert(img)
    img_arr = np.expand_dims(img_to_array(img), axis=0)
    datagen = ImageDataGenerator(rescale=1. / 255)
    dada = datagen.flow(img_arr, batch_size=1, shuffle=False)

    new_shape = (1,) + IMAGE_SIZE + (1,)
    final_image = tf.convert_to_tensor(dada[0].reshape(new_shape))
    model = tf.keras.models.load_model(MODEL_PATH)
    conf = model.predict(final_image)
    pred = conf.argmax(axis=1)

    print("Predicted {} with {}% confidence.".format(pred,conf[0][pred]*100))
    response= {
        'classVal':int(pred[0]),
        'class_prob':conf.tolist()
    }
    return pred, response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug= False)
