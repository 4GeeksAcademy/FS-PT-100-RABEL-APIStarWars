from flask import request, jsonify
from models import db, Personaje, Planeta,Vehiculo, Usuario, PersonajeFav, PlanetaFav, VehiculoFav
from app import app


@app.route('/users', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    personajes = [fav.personaje.serialize() for fav in usuario.favoritos_personajes]
    planetas = [fav.planeta.serialize() for fav in usuario.favoritos_planetas]
    vehiculos = [fav.vehiculo.serialize() for fav in usuario.favoritos_vehiculos]


    return jsonify({
    "personajes": personajes,
    "planetas": planetas,
    "vehiculos": vehiculos
}), 200


@app.route('/people', methods=['GET'])
def get_people():
    personajes = Personaje.query.all()
    results = list(map(lambda personaje: personaje.serialize(), personajes))
    return jsonify(results), 200


@app.route('/people/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200


@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    personaje = Personaje.query.get(person_id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    favorito = PersonajeFav(usuario_id=user_id, personaje_id=person_id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify({"msg": "Personaje añadido a favoritos"}), 200


@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    fav = PersonajeFav.query.filter_by(usuario_id=usuario.id, personaje_id=person_id).first()

    if not fav:
        return jsonify({"msg": " Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": " Favorito eliminado correctamente"}), 200




@app.route('/planets', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    resultados = [planeta.serialize() for planeta in planetas]
    return jsonify(resultados), 200


@app.route('/planets/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planeta.query.get(planeta_id)
    if planeta is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    fav = PlanetaFav(usuario_id=usuario.id, planeta_id=planet_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"msg": f" Planeta {planeta.nombre} agregado a favoritos"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    fav = PlanetaFav.query.filter_by(usuario_id=usuario.id, planeta_id=planet_id).first()

    if not fav:
        return jsonify({"msg": " Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": " Favorito eliminado correctamente"}), 200



@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehiculos = Vehiculo.query.all()
    return jsonify([v.serialize() for v in vehiculos]), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    vehiculo = Vehiculo.query.get(vehicle_id)
    if not vehiculo:
        return jsonify({"msg": "Vehículo no encontrado"}), 404

    favorito = VehiculoFav(usuario_id=user_id, vehiculo_id=vehicle_id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify({"msg": f" Vehículo {vehiculo.nombre} agregado a favoritos"}), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"msg": "Falta el parámetro user_id"}), 400

    favorito = VehiculoFav.query.filter_by(usuario_id=user_id, vehiculo_id=vehicle_id).first()
    if not favorito:
        return jsonify({"msg": " Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg": " Vehículo eliminado de favoritos"}), 200

