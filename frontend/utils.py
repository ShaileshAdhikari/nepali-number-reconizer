import os
import numpy as np
import tensorflow as tf
from PIL import ImageOps
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator


IMAGE_SIZE = (25,25)
MODEL_PATH = os.path.abspath("..") +'/backend/best-model.h5'
IMAGE_DETAILS=[
    {
        "id":0,
        "image_path":"../static/numbers/0.png",
        "image_name":"Zero"
    },
    {
        "id": 1,
        "image_path": "../static/numbers/1.png",
        "image_name": "One"
    },
    {
        "id": 2,
        "image_path": "../static/numbers/2.png",
        "image_name": "Two"
    },
    {
        "id": 3,
        "image_path": "../static/numbers/3.png",
        "image_name": "Three"
    },
    {
        "id": 4,
        "image_path": "../static/numbers/4.png",
        "image_name": "Four"
    },
    {
        "id": 5,
        "image_path": "../static/numbers/5.png",
        "image_name": "Five"
    }
]

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
        'path':directory,
        'classVal':int(pred[0]),
        'class_prob':conf.tolist()
    }
    return pred, response