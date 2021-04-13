# import the necessary packages
from pyzbar.pyzbar import decode
import argparse
import cv2
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)


def scan_qr(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # find the qrcodes in the image and decode each of the barcodes
    qrcodes = decode(image)

    # loop over the detected qrcodes
    for qrcode in qrcodes:

        # extract the bounding box location of the qrcode and draw the
        # bounding box surrounding the qrcode on the image
        (x, y, w, h) = qrcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the qrcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        qrcodeData = qrcode.data.decode("utf-8")
        qrcodeType = qrcode.type

        your_list = pd.DataFrame(
            {'type': [qrcodeType],
             'url': [qrcodeData]
             })
        your_list = your_list[your_list.type == 'QRCODE']

        return(your_list)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def imgpost():
    # read image file string data
    filestr = request.files['file'].read()
    # convert string data to numpy array
    npimg = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    output = scan_qr(img)
    if output is None:
        return jsonify({"Error": "Broken QRCode or No QRCode Detected"})

    return jsonify(output.to_json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
