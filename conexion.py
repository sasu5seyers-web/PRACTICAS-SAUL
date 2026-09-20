from pymongo import MongoClient

# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Seleccionar la base de datos
db = client["escuela"]

print("Conexión exitosa con MongoDB")
