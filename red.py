# Importaciones

import pandas as pd # Tomar los datos
import numpy as np  # Gestionar los arreglos con los datos
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split # Para separar datos de entrenamiento con de testeo
from sklearn.metrics import precision_recall_curve, average_precision_score
import tensorflow as keras # Para Crear/entrenar/evaluar el modelo
from keras.models import Sequential
from keras.layers import Dense 
from keras.optimizers import Adam # Optimizador
import matplotlib.pyplot as plt # Para graficar

# Entramiento de red

def entrenamiento_red():
    
    # Leer datos
    data = pd.read_csv("./datos/datos_de_pacientes_5000.csv",index_col=0)

    print("-----------------------")
    print("--------Datos----------")
    print("-----------------------")
    print(data)

    # Escalar variables
    scaler = MinMaxScaler()

    # Separar datos de resultados y de analisis
    X = data.drop(['riesgo_cardiaco'], axis=1)
    y = np.array(data['riesgo_cardiaco'])

    # Dividir en datos de entrenamiento y testeo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_train = pd.DataFrame(scaled_X_train, columns=X_train.columns)

    scaled_X_test = scaler.fit_transform(X_test)
    scaled_X_test = pd.DataFrame(scaled_X_test, columns=X_test.columns)

    # Creo el modelo
    model = Sequential()

    # Entradas (colesterol, presion, glucosa, edad, sobrepeso, tabaquismo)
    model.add(Dense(50, input_shape=(6,), activation='relu', kernel_initializer='uniform'))
    model.add(Dense(25, activation='relu', kernel_initializer='random_normal'))
    model.add(Dense(35, activation='relu', kernel_initializer='random_normal'))
    model.add(Dense(1, activation='sigmoid')) 

    # Compilo la red
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01))
    model.summary()

    # Entreno red
    historicalModel = model.fit(scaled_X_train, y_train, validation_split=0.2, epochs=200, batch_size=32, verbose=2) 

    # Obtengo el modelo predictivo
    y_pred = model.predict(scaled_X_test)

    # Guardo modelo
    model.save("model.keras")

    # Visualización de la pérdida
    plt.plot(historicalModel.history['loss'], label='Training Loss')
    plt.plot(historicalModel.history['val_loss'], label='Validation loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Visualización de precisión
    precision, recall, _ = precision_recall_curve(y_test, y_pred)
    avg_precision = average_precision_score(y_test, y_pred)

    plt.plot(recall, precision, color='blue', lw=2, label='Precision-Recall curve (AP = {:.2f})'.format(avg_precision))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc='lower right')
    plt.show()

    return 'network train successfully executed'