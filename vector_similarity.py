import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
from scipy.spatial import distance
import sys, os

print(sys.argv)

model_url = "https://tfhub.dev/tensorflow/efficientnet/lite0/feature-vector/2"
IMAGE_SHAPE = (224, 224)

# Wrap the TensorFlow Hub KerasLayer in a Lambda layer
layer = tf.keras.layers.Lambda(lambda x: hub.KerasLayer(model_url)(x))

model = tf.keras.Sequential([layer])

def extract(file):
    file = Image.open(file).resize(IMAGE_SHAPE)
    file = file.convert('RGB')  # Convert image to RGB
    file = np.array(file) / 255.0
    embedding = model.predict(file[np.newaxis, ...])
    flattened_feature = embedding.flatten()
    return flattened_feature

def dc(img1, img2, metric="cosine"):
    return distance.cdist([img1], [img2], metric)[0]

cwd = 'c:\\Users\\julia\\Desktop\\Yhack-AI-Artist-Coach\\'
print(os.path.join(cwd, "output.png"))
img1 = extract(os.path.join(cwd, "output.png"))
path2 = os.path.join(cwd, "ui_images/")
interger = int(sys.argv[1])
path2 += "0" if interger < 10 else ""
path2 += str(interger) + ".png"
img2 = extract(path2)

rating = dc(img1, img2)
try:
    rating = rating[0]
    with open("output.txt", "w") as f:
        f.write(str(rating))
except:
    print("FAIL")

rating = f"{100 - float(rating) * 100:.2f}"
print(rating)
