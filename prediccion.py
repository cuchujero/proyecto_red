import numpy as np
import tensorflow as tf

def analisis(parametro_colesterol, parametro_presion, parametro_azucar, parametro_edad, parametro_sobrepeso, parametro_tabaquismo):
    model = tf.keras.models.load_model("./model/model.keras")
    param = np.array([parametro_colesterol, parametro_presion, parametro_azucar, parametro_edad, parametro_sobrepeso, parametro_tabaquismo])
    result = model.predict(np.expand_dims(param, axis=0))
    return int(result[0][0])
