import requests
from app import app
from models import db, Vehiculo

def get_vehiculos_from_swapi():
    vehiculos = []
    url = "https://www.swapi.tech/api/vehicles"

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error al obtener vehículos:", response.status_code)
            break

        data = response.json()
        for item in data["results"]:
            detalle_url = item["url"]
            swapi_id = int(detalle_url.rstrip('/').split('/')[-1])
            detalle_response = requests.get(detalle_url)
            if detalle_response.status_code == 200:
                detalles = detalle_response.json()
                props = detalles["result"]["properties"]
                vehiculos.append({
                    "nombre": props["name"],
                    "modelo": props.get("model"),
                    "fabricante": props.get("manufacturer"),
                    "costo": props.get("cost_in_credits"),
                    "swapi_id": swapi_id
                })

        url = data.get("next")

    return vehiculos

if __name__ == "__main__":
    with app.app_context():
        vehiculos = get_vehiculos_from_swapi()
        print(f"Se obtuvieron {len(vehiculos)} vehículos.")

        for v in vehiculos:
            vehiculo = Vehiculo(
                nombre=v["nombre"],
                modelo=v["modelo"],
                fabricante=v["fabricante"],
                costo=v["costo"],
                swapi_id=v["swapi_id"]
            )
            db.session.add(vehiculo)
            print(f"Insertado: {vehiculo.nombre}")

        db.session.commit()
        print("Todos los vehículos han sido guardados correctamente.")
