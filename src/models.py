from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorites=db.Table(
    'favorites',
    db.Model.metadata,
    db.Column("user_id",db.ForeignKey("user.id")),
    db.Column("planet_id",db.ForeignKey("planet.id")),
    db.Column("character_id",db.ForeignKey("character.id"))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    
    def serialize_user(self):
        return{
            "id":self.id,
            "username":self.username
        }

   


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250),nullable=False)
    climate = db.Column(db.String(50))

    def serialize_planet(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "climate":self.climate
        }

   
    


class Character(db.Model):
    __tablename__='character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    alive = db.Column(db.Boolean,nullable=False)

    def serialize_character(self):
        return{
            "id":self.id,
            "name":self.name,
            "alive":self.alive
        }

