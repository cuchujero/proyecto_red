#SAxJI93958X909x5674!kf
#JCoweiw93xRIWQxxxte536

from prediccion import analisis
from red import entrenamiento_red
from servicio import comprobacion_apikey, registro_auditoria, controlar_peticion
import time
from datetime import datetime
from bson import ObjectId
from cachetools import TTLCache
from flask import Flask, jsonify, request

user_cache = TTLCache(maxsize=100, ttl=300)
resultado_cache = TTLCache(maxsize=100, ttl=300)

app = Flask(__name__)

@app.route('/entramiento_red', methods=['GET'])
def entramiento_red_route():
    try:
        return entrenamiento_red()
    except Exception as e:
        # Maneja cualquier error y devuelve un mensaje de error
        return jsonify({"error": str(e)}), 500


@app.route('/comprobar_riesgo', methods=['GET'])
def comprobar_riesgo_route():
    try:

        start_time = time.time()

        # Comprobacion api key
        provided_api_key = request.headers.get('Authorization')

        usuario = user_cache.get(provided_api_key)

        if usuario is None:
            usuario = comprobacion_apikey(provided_api_key)
            user_cache[provided_api_key] = usuario

        if usuario=="no encontrado":
            return jsonify({"error": "API key no válida"}), 401

        # Analisis de riesgo cardiaco
        parametro_colesterol = float(request.args.get('nivel_colesterol'))
        parametro_presion = float(request.args.get('presion_arterial'))
        parametro_azucar = float(request.args.get('azucar'))
        parametro_edad = int(request.args.get('edad'))
        parametro_sobrepeso = int(request.args.get('sobrepeso'))
        parametro_tabaquismo = int(request.args.get('tabaquismo'))

        resultado_cache_key = (
            parametro_colesterol,
            parametro_presion,
            parametro_azucar,
            parametro_edad,
            parametro_sobrepeso,
            parametro_tabaquismo,
        )

        resultado = resultado_cache.get(resultado_cache_key)


        if resultado is None:
            resultado = analisis(parametro_colesterol, parametro_presion, parametro_azucar, parametro_edad, parametro_sobrepeso, parametro_tabaquismo)
            resultado_cache[resultado_cache_key] = resultado
 
        # Calculo de tiempo
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Tiempo actual
        current_datetime = datetime.now()

        control = controlar_peticion(current_datetime, provided_api_key, usuario['user_type'])

        if control==1:
            return jsonify({"error": "Su tipo de usuario ha excedido la cantidad de peticiones"}), 401
         
        registro_auditoria({"_id": ObjectId(),"process_time": elapsed_time, "date": current_datetime, "api_key": provided_api_key, "user_id": usuario['_id']})

        # Devuelve el resultado como respuesta JSON
        if resultado==1:
            return jsonify({"Resultado": "Existe riesgo cardiaco"}), 200
        else:
           return jsonify({"Resultado": "No existe riesgo cardiaco"}), 200
       
    except Exception as e:
        # Maneja cualquier error y devuelve un mensaje de error
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

