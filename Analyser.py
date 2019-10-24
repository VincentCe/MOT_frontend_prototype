from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout, Flatten, Dense
from PIL import Image
from flask_cors import CORS, cross_origin
import tensorflow as tf
import numpy as np
import requests
import os
from PIL import Image

model = None


def load_model():
  # load the pre-trained Keras model (here we are using a model
  # pre-trained on ImageNet and provided by Keras, but you can
  # substitute in your own networks just as easily)
  global model
  # build the network
  base_model = tf.keras.applications.resnet50.ResNet50(
      include_top=False, weights=None, input_shape=(224, 224, 3))

  # build a classifier model to put on top of the convolutional model
  top_model = Sequential()
  top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
  top_model.add(Dense(1000, activation='relu'))
  top_model.add(Dropout(0.5))
  top_model.add(Dense(1000, activation='relu'))
  top_model.add(Dropout(0.5))
  top_model.add(Dense(4, activation='softmax'))

  model = Model(inputs=base_model.input, outputs=top_model(base_model.output))
  model.load_weights(r'C:\Users\DD\Desktop\MOT\server\ResNet_trainAll_May.h5')
  # model = tf.keras.models.load_model('./keras_model.h5')
  model._make_predict_function()

def prepare_image(image):
  # if the image mode is not RGB, convert it
  if image.mode != "RGB":
    image = image.convert("RGB")

  # resize the input image and preprocess it
  image = image.resize((224, 224))
  image = img_to_array(image) / 255
  image = np.expand_dims(image, axis=0)
  # return the processed image
  return image

load_model()

dirpath = 'snapshot'
for root, dirnames, fnames in os.walk(dirpath):
    for fname in fnames:
        path = os.path.join('.', root, fname)

        image = Image.open(path)  
        
        Reversed_image = prepare_image(image)
        preds = model.predict(Reversed_image)
        print(preds)


    
    




        




        