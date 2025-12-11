import json
import os
from django.conf import settings
from users.models import Vehiculo

def load_initial_data():
    json_path = os.path.join(settings.BASE_DIR, "vehiculos.json")

    if not os.path.exists(json_path):
        print("⚠️ vehiculos.json no encontrado.")
        return

    if Vehiculo.objects.exists():
        print("⚠️ Ya existen vehículos en la base de datos. No se cargarán de nuevo.")
        return

    print("📌 Cargando vehículos iniciales...")

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            fields = item["fields"]
            Vehiculo.objects.create(**fields)

    print("✅ Vehículos cargados correctamente.")
