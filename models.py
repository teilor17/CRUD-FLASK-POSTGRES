from database import db

class Trabajador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    compleacomulada = db.Column(db.Integer, default=0)

    def __init__(self, name, compleacomulada):
        self.name = name
        self.compleacomulada = compleacomulada

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    complejidad = db.Column(db.Integer, nullable=False)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajador.id'), nullable=True)

    def __init__(self, description, complejidad, trabajador_id):
        self.description = description
        self.complejidad = complejidad
        self.trabajador_id = trabajador_id