import numpy as np
import tensorflow as tf
from PIL import Image
import pillow_heif
from os.path import exists
import gdown

from src.repository import img_classes


model_filename = "src\static\img_model\museum_model_62.hdf5"

if not exists(model_filename):
    url = 'https://drive.google.com/file/d/1hGyUfsZ7M9Ki8WbgTNTJ8HiZxMPpDPA8/view?usp=share_link'
    output = model_filename
    gdown.download(url, output, quiet=False, fuzzy=True)

model = tf.keras.models.load_model(model_filename, compile=False)

ALLOWED_EXTENSIONS = {'jpg', 'heic'}


def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def heic_pic(picture_path):
    heif_file = pillow_heif.read_heif(picture_path, convert_hdr_to_8bit=False, bgr_mode=False)
    image_pil = heif_file.to_pillow()
    image_pil = image_pil.resize((256, 256))
    image_matrix = np.array(image_pil)
    input_image = np.reshape(image_matrix, (-1, 256, 256, 3))
    return input_image


def jpg_pic(picture_path):
    image_png = Image.open(picture_path)
    image_png = image_png.resize((256, 256))
    image_png = np.array(image_png)
    input_image = np.reshape(image_png, (-1, 256, 256, 3))
    return input_image


def predict_image(image):
    image = str(fr'{image}')
    if image.split('.')[-1].lower() == 'heic':
        input_img = heic_pic(image)
    elif image.split('.')[-1].lower() == 'jpg':
        input_img = jpg_pic(image)
    predict_img = model.predict(input_img)
    print(predict_img)
    pred_class = img_classes.classes[np.argmax(predict_img)]
    print(pred_class)
    return pred_class


if __name__ == '__main__':
    print(predict_image("D:/Дима/museum_project/src/static/upload/IMG_2096.HEIC"))
