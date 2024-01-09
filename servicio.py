import pymongo

def conexion(nombre_coleccion):
    # Direccion a la base de datos
    uri = "mongodb+srv://cuchujero:1AQdaVJSjWlEP9Xs@cluster0.5nzhn.mongodb.net/?retryWrites=true&w=majority"
    # Conexión a la base de datos
    client = pymongo.MongoClient(uri)  

    '''
    # ping de conexion
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    '''

    # Seleccionar o crear una base de datos
    database = client["network"]

    # Seleccionar o crear una colección
    collection = database[nombre_coleccion]

    return [collection, client]


def comprobacion_apikey(apikeyValue):

    [collection, client] = conexion("user")

    # Realizar la búsqueda
    usuario_encontrado = collection.find_one({'api_key': apikeyValue})

    client.close()

    # Verificar si se encontró el usuario
    if usuario_encontrado:
        return usuario_encontrado
    else:
       return "no encontrado"


def registro_auditoria(registro):

    [collection, client] = conexion("log")

    insert_result = collection.insert_one(registro)
    
    print(f"ID del documento insertado: {insert_result.inserted_id}")

    client.close()

    return insert_result

   
def controlar_peticion(current_datetime, apiKey, tipo_usuario):

    [collection, client] = conexion("log")

    if tipo_usuario=='PREMIUM':
        request_limit = 50
    else:
        request_limit = 5

    document_count = collection.count_documents({"api_key": apiKey})
    
    if (document_count<request_limit):
        return 0
    else:
        documents = collection.find({"api_key": apiKey}).sort([("_id", -1)]).limit(request_limit)

        document_date = documents[request_limit-1].get("date")

        time_difference = (current_datetime - document_date).total_seconds() / 60

        client.close()

        if abs(time_difference) < 1:
            return 1
        else:
            return 0
