from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120))
    apellido: Mapped[str] = mapped_column(String(120))
    fecha_suscripcion: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    favoritos_personajes = relationship("PersonajeFav", back_populates="usuario", cascade="all, delete")
    favoritos_planetas = relationship("PlanetaFav", back_populates="usuario", cascade="all, delete")
    favoritos_vehiculos = relationship('VehiculoFav', backref='usuario_fav_vehiculo', lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_suscripcion": self.fecha_suscripcion.isoformat() if self.fecha_suscripcion else None
        }


class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    genero: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ano_nacimiento: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    altura: Mapped[Optional[int]] = mapped_column(nullable=True)
    peso: Mapped[Optional[int]] = mapped_column(nullable=True)
    color_piel: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    swapi_id: Mapped[int] = mapped_column(nullable=True)


    favoritos = relationship("PersonajeFav", back_populates="personaje", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "ano_nacimiento": self.ano_nacimiento,
            "altura": self.altura,
            "peso": self.peso,
            "color_piel": self.color_piel,
            "swapi_id": self.swapi_id
        }


class Planeta(db.Model):
    __tablename__ = "planeta"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    clima: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    terreno: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    poblacion: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    diametro: Mapped[Optional[int]] = mapped_column(nullable=True)
    swapi_id: Mapped[int] = mapped_column(nullable=True)


    favoritos = relationship("PlanetaFav", back_populates="planeta", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
            "diametro": self.diametro,
            "swapi_id": self.swapi_id
        }


class PersonajeFav(db.Model):
    __tablename__ = "personaje_fav"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="favoritos_personajes")
    personaje = relationship("Personaje", back_populates="favoritos")


class PlanetaFav(db.Model):
    __tablename__ = "planeta_fav"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="favoritos_planetas")
    planeta = relationship("Planeta", back_populates="favoritos")

class Vehiculo(db.Model):
    __tablename__ = "vehiculo"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    modelo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    fabricante: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    costo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    swapi_id: Mapped[int] = mapped_column(nullable=True)


    favoritos = relationship("VehiculoFav", back_populates="vehiculo", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "fabricante": self.fabricante,
            "costo": self.costo,
            "swapi_id": self.swapi_id
        }

class VehiculoFav(db.Model):
    __tablename__ = "vehiculo_fav"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculo.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="favoritos_vehiculos")
    vehiculo = relationship("Vehiculo", back_populates="favoritos")

