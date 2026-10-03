from pymongo import MongoClient
from config import mongo_uri, mongo_db, mongo_colection

# Conectar con MongoDB Atlas
client = MongoClient(mongo_uri)

# Seleccionar la base de datos
db = client[mongo_db]

# Seleccionar la colección
alumnos = db[mongo_colection]

print("Conexión exitosa a MongoDB Atlas")
print("Base de Datos:", mongo_db)
print("Colección:", mongo_colection)

# Alumno que se va a guardar
alumno = {
    "nombre": "Saul",
    "edad": 24,
    "carrera": "Desarrollo de Software Multiplataforma"
}

# Guardar alumno
resultado = alumnos.insert_one(alumno)

print("Id guardado:", resultado.inserted_id)