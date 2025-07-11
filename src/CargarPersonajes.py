import requests
from app import app
from models import db, Personaje
from sqlalchemy import text

def get_personajes_from_swapi():
    personajes = []
    url = "https://www.swapi.tech/api/people"

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error al obtener personajes:", response.status_code)
            break

        data = response.json()
        for item in data["results"]:
            detalle_url = item["url"]
            swapi_id = int(detalle_url.rstrip('/').split('/')[-1])
            detalle_response = requests.get(detalle_url)    
            if detalle_response.status_code == 200:
                detalles = detalle_response.json()
                props = detalles["result"]["properties"]
                personajes.append({
                    "nombre": props["name"],
                    "genero": props["gender"],
                    "año_nacimiento": props["birth_year"],
                    "altura": int(props["height"]) if props["height"].isdigit() else None,
                    "peso": int(props["mass"]) if props["mass"].isdigit() else None,
                    "color_piel": props["skin_color"],
                    "swapi_id": swapi_id
                })

        url = data["next"]

    return personajes

if __name__ == "__main__":
    with app.app_context():
        db.session.execute(text("DELETE FROM personaje_fav;"))
        db.session.execute(text("DELETE FROM personaje;"))
        db.session.execute(text("ALTER SEQUENCE personaje_id_seq RESTART WITH 1;"))
        db.session.commit()

        personajes = get_personajes_from_swapi()
        print(f"Se obtuvieron {len(personajes)} personajes.")

        for p in personajes:
            personaje = Personaje(
                nombre=p["nombre"],
                genero=p["genero"],
                ano_nacimiento=p["año_nacimiento"],
                altura=p["altura"],
                peso=p["peso"],
                color_piel=p["color_piel"],
                swapi_id=p["swapi_id"]
            )
            db.session.add(personaje)
            print(f"Insertado: {personaje.nombre}")

        db.session.commit()
        print("✅ Todos los personajes han sido guardados correctamente.")