import requests
from app import app
from models import db, Planeta

def get_planetas_from_swapi():
    planetas = []
    url = "https://www.swapi.tech/api/planets"

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print("❌ Error al obtener planetas:", response.status_code)
            break

        data = response.json()
        for item in data["results"]:
            detalle_url = item["url"]
            swapi_id = int(detalle_url.rstrip('/').split('/')[-1])
            detalle_response = requests.get(detalle_url)
            if detalle_response.status_code == 200:
                detalles = detalle_response.json()
                props = detalles["result"]["properties"]
                
                planetas.append({
                    "nombre": props["name"],
                    "clima": props["climate"],
                    "terreno": props["terrain"],
                    "poblacion": int(props["population"]) if props["population"].isdigit() else None,
                    "diametro": int(props["diameter"]) if props["diameter"].isdigit() else None,
                    "swapi_id": swapi_id
                })

        url = data.get("next")

    return planetas

if __name__ == "__main__":
    with app.app_context():
        planetas = get_planetas_from_swapi()
        print(f"🌍 Se obtuvieron {len(planetas)} planetas.")

        for p in planetas:
            planeta = Planeta(
                nombre=p["nombre"],
                clima=p["clima"],
                terreno=p["terreno"],
                poblacion=p["poblacion"],
                diametro=p["diametro"],
                swapi_id=p["swapi_id"]
            )
            db.session.add(planeta)
            print(f"✅ Insertado: {planeta.nombre}")

        db.session.commit()
        print("🎉 Todos los planetas han sido guardados correctamente.")

