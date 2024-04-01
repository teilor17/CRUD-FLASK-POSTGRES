from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from database import db
from forms import TrabajadorForm, SupportForm
from models import Trabajador, Support

app = Flask(__name__)
USER_BD = 'postgres'
PASS_BD = 'admin'
URL_BD = 'localhost'
NAME_BD = 'suportbd'
FULL_URL_BD = f'postgresql://{USER_BD}:{PASS_BD}@{URL_BD}/{NAME_BD}'
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_BD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
app.config['SECRET_KEY']='llave_secreta'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def trabajadores():
    trabajadores = Trabajador.query.order_by('compleacomulada')
    supports = Support.query.order_by('trabajador_id')
    total_supports = Support.query.count()
    total_trabajadores = Trabajador.query.count()
    app.logger.debug(f'Listado de personas: {trabajadores}')
    app.logger.debug(f'Listado de personas: {total_trabajadores}')
    return render_template('index.html', trabajadores=trabajadores, total_trabajadores=total_trabajadores, supports=supports, total_supports=total_supports)

@app.route('/supports')
def supports():
    supports = Support.query.order_by('trabajador_id')
    trabajador = Trabajador.query.filter_by(id=id).all()
    total_supports = Support.query.count()
    app.logger.debug(f'Listado de trabajos: {total_supports}')
    return render_template('detallet.html', supports=supports, total_supports=total_supports, trabajador=trabajador)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    trabajador = Trabajador.query.get_or_404(id)
    trabajos = Support.query.filter_by(trabajador_id=id).all()
    app.logger.debug(f'ver persona: {trabajador}')
    return render_template('detalle.html', trabajador=trabajador, trabajos=trabajos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    trabajador = Trabajador(name=None, compleacomulada=None)
    trabajadorform = TrabajadorForm(obj=trabajador)
    if request.method == 'POST':
        if trabajadorform.validate_on_submit():
            trabajadorform.populate_obj(trabajador)
            app.logger.debug(f'trabajador agregado: {trabajador}')
            db.session.add(trabajador)
            db.session.commit()
            return redirect(url_for('trabajadores'))
    return render_template('agregar.html', forma=trabajadorform)

@app.route('/asignar', methods=['GET', 'POST'])
def asignar():
    trabajador = Trabajador.query.order_by(Trabajador.compleacomulada).first()
    support = Support(description=None, complejidad=None, trabajador_id=trabajador.id)
    supportform = SupportForm(obj=support)
    if request.method == 'POST':
        if supportform.validate_on_submit():
            supportform.populate_obj(support)
            app.logger.debug(f'trabajo agregado: {support}')
            db.session.add(support)
            complejidad = support.complejidad
            trabajador.compleacomulada += int(complejidad)
            db.session.commit()
            return redirect(url_for('trabajadores'))
    return render_template('asignar.html', forma=supportform)

if __name__ == '__main__':
    app.run(debug=True)