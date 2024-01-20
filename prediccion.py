import numpy as np
import tensorflow as tf
from joblib import load

def analisis(parametro_colesterol, parametro_presion, parametro_azucar, parametro_edad, parametro_sobrepeso, parametro_tabaquismo):
    model = tf.keras.models.load_model("./model/model.keras")
    params = np.array([parametro_colesterol, parametro_presion, parametro_azucar, parametro_edad, parametro_sobrepeso, parametro_tabaquismo])
    params = params.reshape(1, -1)
    scaler = load("./scaler/scaler.joblib")
    scaled_params = scaler.transform(params)
    result = model.predict(scaled_params)
    return int(result[0][0])
