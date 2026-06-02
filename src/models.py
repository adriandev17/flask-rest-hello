from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False,
                          nullable=False, default=True)

    # Relación con la tabla Favorite
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # ¡Importante! Por seguridad no serializamos el password
        }


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20))

    # Relación con la tabla Favorite
    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120))
    terrain = db.Column(db.String(120))

    # Relación con la tabla Favorite
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)

    # Claves Foráneas (Foreign Keys) - "Los cables" que conectan las tablas
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(
        db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(
        db.Integer, db.ForeignKey('people.id'), nullable=True)

    def __repr__(self):
        return f'<Favorite {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
