import json
from django.core.management.base import BaseCommand
from users.models import Vehiculo
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Carga datos iniciales de vehículos desde vehiculos.json"

    def handle(self, *args, **kwargs):
        try:
            # Ruta del archivo JSON
            json_path = os.path.join(settings.BASE_DIR, "vehiculos.json")

            self.stdout.write(f"📂 Leyendo archivo: {json_path}")

            # Leer archivo en UTF-8
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Crear vehículos
            for item in data:
                fields = item["fields"]

                Vehiculo.objects.update_or_create(
                    id=item["pk"],
                    defaults={
                        "name": fields["name"],
                        "category": fields["category"],
                        "year": fields["year"],
                        "engine": fields["engine"],
                        "power": fields["power"],
                        "transmission": fields["transmission"],
                        "fuel": fields["fuel"],
                        "price": fields["price"],
                        "availability": fields["availability"],
                        "specs": fields["specs"],
                        "image": fields["image"],
                    }
                )

            self.stdout.write(self.style.SUCCESS("✔ Vehículos cargados correctamente"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error cargando datos: {e}"))
