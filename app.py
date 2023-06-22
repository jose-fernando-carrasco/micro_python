from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/scan-qr', methods=['POST'])
def scan_qr():
    # Verifica si se ha enviado una imagen en la solicitud
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ninguna imagen'}), 400

    # Lee la imagen desde la solicitud
    image = request.files['image'].read()

    # Convierte la imagen en un arreglo NumPy
    nparr = np.fromstring(image, np.uint8)

    # Decodifica los códigos QR en la imagen
    decoded_objects = decode(cv2.imdecode(nparr, cv2.IMREAD_COLOR))

    # Extrae la información de los códigos QR decodificados
    results = []
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        result = {'data': data, 'type': obj.type}
        results.append(result)

    # Devuelve los resultados en formato JSON
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
