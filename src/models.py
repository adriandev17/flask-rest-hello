from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    # ESTO ES LO QUE FALTA: La conexión bidireccional
    # Permite hacer: "user_actual.favorites" y obtener su lista
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites] # Ahora puedes incluir sus favoritos aquí
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20))
    
    # Relación: Para saber quiénes tienen a este personaje como favorito
    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def serialize(self):
        return {"id": self.id, "name": self.name}

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    
    # Relación: Para saber en qué listas de favoritos está este planeta
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def serialize(self):
        return {"id": self.id, "name": self.name}

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    
    # Las ForeignKeys (Los cables)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    # Nota: No necesitamos poner relationship aquí porque usamos 'backref' arriba.
    # Gracias al backref, el objeto 'Favorite' ya tiene .user, .planet y .people automáticamente.

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None, # Acceso directo gracias al relationship
            "people": self.people.serialize() if self.people else None
        }