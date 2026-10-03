from pymongo import MongoClient
from config import mongo_uri, mongo_db, mongo_colection

try:
    client = MongoClient(mongo_uri)

    # Comprobar conexión
    client.admin.command("ping")

    # Seleccionar base de datos
    db = client[mongo_db]

    # Seleccionar colección
    estudiantes = db[mongo_colection]

    # Datos de los alumnos
    alumnos_data = [
        {
            "nombre": "Jose",
            "edad": 28,
            "carrera": "Sistemas"
        },
        {
            "nombre": "Raul",
            "edad": 21,
            "carrera": "Sistemas"
        },
        {
            "nombre": "Saul",
            "edad": 24,
            "carrera": "Desarrollo de Software Multiplataforma"
        }
    ]

    # Insertar alumnos
    resultado = estudiantes.insert_many(alumnos_data)

    print("Alumnos agregados")
    print("IDs:", resultado.inserted_ids)

except Exception as error:
    print("Error:")
    print(error)

finally:
    try:
        client.close()
    except:
        pass