from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from models import db
from models import Alumnos

app = Flask(__name__)  # normalmente va oculta
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)

# validar que exista el recurso
@app.errorhandler(404)
# cache (e)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/")
@app.route("/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form = create_form,alumnos = alumno)

@app.route('/detalles', methods = ['GET','POST'])
def detalles():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get('id')
        nombre = alum1.nombre
        apaterno = alum1.apaterno
        email = alum1.email
        return render_template('detalles.html',id=id, nombre = nombre, apaterno = apaterno, email = email)


@app.route('/Alumnos1',methods = ['GET','POST'])
def Alumnos1():
    create_form = forms.UserForm2(request.form)
    if request.method == 'POST':
        alu = Alumnos(nombre = create_form.nombre.data,
                      apaterno = create_form.apaterno.data,
                      email = create_form.email.data)
        db.session.add(alu)
        db.session.commit()
        return redirect(url_for('index.html'))
    return render_template('Alumnos1.html',form = create_form)

if __name__ == '__main__':
    csrf.init_app(app)  
    db.init_app(app)   

    with app.app_context():
        db.create_all()

    app.run()