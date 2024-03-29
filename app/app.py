# # save this as app.py
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, World sou alex!"
#####################################
# inicializacion base
#####################################

from flask import Flask, render_template

# definicion de archivo principal
app = Flask(__name__)


@app.route('/')
def login():
    # rednerizado con jinja2
    return render_template('login.html')

# prueba de funcionamiento y rendereizado de la pagina principal


@app.route('/pagina_principal')
def pagina_principla():
    return render_template('pagina_principal.html')


@app.route('/publicacion')
def agregarUser():
    return render_template('publicacion.html')


@app.route('/personInformation')
def inforPerson():
    return render_template('informacionPersona.html')

if __name__ == '__main__':
    app.run(debug=True)
