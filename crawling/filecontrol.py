import os
import base64
import re

from PIL import Image
from io import BytesIO


class Controller:
    def save_image(self, path, data):
        image = Image.open(BytesIO(data.content))
        image.save(path)

        return 0

    def makedirectory(self, keyword):
        if not os.path.exists(keyword):
            os.makedirs(keyword)

    def save_data_url(self, path, url):
        head, data = url.split(',', 1)
        file_format = head.split(';')[0].split('/')[1]

        data = base64.b64decode(data)
        with open(path + "." + file_format, 'wb') as f:
            f.write(data)

