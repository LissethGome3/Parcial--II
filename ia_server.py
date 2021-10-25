import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import csv 

from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer

archivo = pd.read_csv("dataset.csv", sep=";")
sb.scatterplot(archivo["celsius"], archivo["fahrenheit"])

celsius = archivo["celsius"]
fahrenheit = archivo["fahrenheit"]

modelo = tf.keras.Sequential()
modelo.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

modelo.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

entrenamiento = modelo.fit(celsius, fahrenheit, epochs=350)

class servidor_basico(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Peticion echa con GET")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hola mundo desde Pyhon'.encode())

    def do_POST(self):
        print('POST')
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)
        data = float(data)

        predict = modelo.predict([data])
        print('La predicción es:', predict)
        predict = str(predict)
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(predict.encode())

print('Iniciando el servidor')
server = HTTPServer(('localhost', 3007), servidor_basico)
server.serve_forever()