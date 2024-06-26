
from flask import request
from flask import Flask, render_template, request, redirect, url_for
from config import *
from ClaseFormulario import formulario
import base64
from datetime import *
from publicaciones import *
from mensajes import *
from bson import ObjectId


# con_bd = conexion() #Baquero
con_bd = Conexion()  # alex

app = Flask(__name__)


@app.route('/')
def login():
    # rednerizado con jinja2
    coleccionPersonas = con_bd['users']
    PersonasRegistradas = coleccionPersonas.find()
    return render_template('login.html', datos=PersonasRegistradas)


@app.route('/guardar_registro', methods=['POST'])
def agregarPersona():
    personas = con_bd['users']
    # personas =con_bd['Registro'] Baquero
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    configContraseña = request.form['configContraseña']

    if nombre and apellido and correo and contraseña and configContraseña:
        persona1 = formulario(nombre, apellido, correo,
                              contraseña, configContraseña, None)
        personas.insert_one(persona1.formato_doc())
        return redirect(url_for('login'))

    else:
        return "Error "

# prueba de funcionamiento y rendereizado de la pagina principal

# logica de inicio de sesion


@app.route('/iniciarSesion', methods=['post'])
def iniciarSesion():
    users = con_bd['users']
    correo_acceso = request.form['Email_de_acceso']
    contraseña_acceso = request.form['Contraseña_de_acceso']

    # verificar si se puede implementar mas condiciones respecto a ello
    # print('datos dek ususario depuesdel envio de la imagen', datos_usuario)
    usuario_Existente = users.find_one(
        {'correo': correo_acceso, 'contraseña': contraseña_acceso})
    if usuario_Existente:
        nombre, apellido, correo, imagen = usuario_Existente['nombre'], usuario_Existente[
            'apellido'], usuario_Existente['correo'], usuario_Existente['image']

        # print(imagen, 'fffffffffffffffffffffffffffffffffffffff')
        imagen_base64 = base64.b64encode(
            imagen).decode('utf-8') if imagen else None

        # imagen_base64 = request.args.get('imagen_base64', None)
        # print('existe' if imagen_base64 else 'no existe')

        return index(usuario_Existente, imagen_base64)
    else:
        return 'No existe el usuario'


# logica para editar los datos del ussuario desde la configuracion
@ app.route('/principal')
def index(usuario_Existente, imagen_base64):
    users = con_bd['users']
    listUsers = users.find()
    colSolicitudesPendientes = con_bd['Solicitudes_Pendientes']
    SolicitudesPendientes = colSolicitudesPendientes.find()
    colpublicaciones = con_bd['publicaciones']
    publicaciones = colpublicaciones.find()
    correo_acceso = usuario_Existente['correo']
    usuario = users.find_one({'correo': correo_acceso})
    imagen = usuario.get('image', None)
    imagen_base64 = base64.b64encode(
        imagen).decode('utf-8') if imagen else None

    return render_template('pagina_principal.html', usuario_Existente=usuario_Existente, imagen_base64=imagen_base64, publicaciones=publicaciones, listUsers=listUsers, solicitudes=SolicitudesPendientes)


@app.route('/upload/<correo>', methods=['POST', 'GET'])
def upload(correo):

    usuario_correo = correo
    print(usuario_correo)
    # Aquí puedes usar usuario_correo para acceder al correo electrónico del usuario
    users = con_bd['users']
    correo_acceso = usuario_correo
    # envio de datos y actualizaciones respecto a las publicaciones
    colSolicitudesPendientes = con_bd['Solicitudes_Pendientes']
    SolicitudesPendientes = colSolicitudesPendientes.find()
    listUsers = users.find()
    colpublicaciones = con_bd['publicaciones']
    publicaciones = colpublicaciones.find()
    # ---------------------------------------------------------------
    print(usuario_correo, ' estos son los datos del usuario')
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        users.update_one({'correo': correo_acceso}, {
            '$set': {'image': imagen.read()}})
        usuario_Existente = users.find_one(
            {'correo': correo_acceso})
        imagen = usuario_Existente.get('image', None)
        imagen_base64 = base64.b64encode(
            imagen).decode('utf-8') if imagen else None
        return render_template('pagina_principal.html', usuario_Existente=usuario_Existente, imagen_base64=imagen_base64, publicaciones=publicaciones, listUsers=listUsers, solicitudes=SolicitudesPendientes)
    return 'No se ha proporcionado ninguna imagen'

# @app.route('/Cargarimagen/<correo>', methods=['POST'])
# def upload(correo):
#     users = con_bd['users']
#     correo_acceso = correo
#     if 'image' in request.files:
#         image = request.files['image']
#         if image.filename != '':
#             # Guarda la imagen en el usuario en MongoDB
#             users.update_one({'correo': correo_acceso}, {
#                              '$set': {'image': image.read()}})
#     # Redirige de vuelta a la página principal o a donde quieras después de cargar la imagen
#     return redirect(url_for('principal'))


# logica para cargar la publicacion de cada uno de los estudiantes

# @app.route('/subirPublicacion', method='POST')
# def subirPublicacion():
#     publicaciones = con_bd['publicaciones']
#     usuario = request.form['correo']
#     return 'publvicaicon'


# actualizar los datos del ussuario desde l configuracion
@app.route('/actualizarDatos/<correoExistente>', methods=['POST'])
def ActualizarDatos(correoExistente):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    nueva_contraseña = request.form['nueva_contraseña']
    if nombre == None and correo == None and contraseña == None and nueva_contraseña == None or nombre == '' and correo == '' and contraseña == '' and nueva_contraseña == '':
        return 'No se ingreso ningun dato, por favor regrese a la pagina anterior'
    else:

        users = con_bd['users']
        usuario = users.find_one({'correo': correo})
        _contraeña_Anterior = usuario['contraseña']

        if contraseña != contraseña:
            return 'La contraseña ingresada no coincide con la anterior'

        users.update_one({'correo': correo}, {'$set': {

            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contraseña': nueva_contraseña
        }})

        # envio de datos y actualizaciones respecto a las publicaciones
        colSolicitudesPendientes = con_bd['Solicitudes_Pendientes']
        SolicitudesPendientes = colSolicitudesPendientes.find()
        imagen = usuario.get('image', None)
        imagen_base64 = base64.b64encode(
            imagen).decode('utf-8') if imagen else None
        listUsers = users.find()
        colpublicaciones = con_bd['publicaciones']
        publicaciones = colpublicaciones.find()
        # ---------------------------------------------------------------
        return render_template('pagina_principal.html', usuario_Existente=usuario_Existente, imagen_base64=imagen_base64, publicaciones=publicaciones, listUsers=listUsers, solicitudes=SolicitudesPendientes)


@app.route('/subirPublicacion/<correo>', methods=['POST'])
def SubirPublicacion(correo):
    texto = request.form['texto']
    users = con_bd['users']
    if 'imagen' in request.files:
        imagen = request.files['imagen']
    else:
        imagen = None

    usuario = users.find_one({'correo': correo})
    nombre = usuario['nombre']
    publicacion = Publicacion(correo, nombre, texto)

    colPublicaciones = con_bd['publicaciones']
    colPublicaciones.insert_one(publicacion.formato_doc())

    # envio de datos y actualizaciones respecto a las publicaciones
    colSolicitudesPendientes = con_bd['Solicitudes_Pendientes']
    SolicitudesPendientes = colSolicitudesPendientes.find()
    imagen = usuario.get('image', None)
    imagen_base64 = base64.b64encode(
        imagen).decode('utf-8') if imagen else None
    listUsers = users.find()
    colpublicaciones = con_bd['publicaciones']
    publicaciones = colpublicaciones.find()
    # ---------------------------------------------------------------
    return render_template('pagina_principal.html', usuario_Existente=usuario, imagen_base64=imagen_base64, publicaciones=publicaciones, listUsers=listUsers, solicitudes=SolicitudesPendientes)


@app.route('/enviarSolicitud/<correo>', methods=['POST'])
def enviarSolicitud(correo):
    EnviarCorreoA = request.form.get('CorreoOtroUsuario')
    users = con_bd['users']
    usuario = users.find_one({'correo': correo})

    coleccionSolicitudes = con_bd['Solicitudes_Pendientes']

    if not coleccionSolicitudes.find_one({'correo_enviador': correo, 'correo_receptor': EnviarCorreoA}):
        coleccionSolicitudes.insert_one({
            'correo_enviador': correo,
            'correo_receptor': EnviarCorreoA
        })

    solicitudes = coleccionSolicitudes.find()
    imagen = usuario.get('image', None)
    imagen_base64 = base64.b64encode(
        imagen).decode('utf-8') if imagen else None
    listUsers = users.find()
    colpublicaciones = con_bd['publicaciones']
    publicaciones = colpublicaciones.find()

    return render_template('pagina_principal.html', usuario_Existente=usuario, imagen_base64=imagen_base64, publicaciones=publicaciones, listUsers=listUsers, solicitudes=solicitudes)


@app.route('/AceptarSolicitud/<correo_enviador>', methods=['POST'])
def AceptarSolicitud(correo_enviador):
    users = con_bd['users']
    correo = request.form.get('correo')

    coleccionSolicitudes = con_bd['Solicitudes_Pendientes']

    coleccionSolicitudes.delete_one(
        {'correo_enviador': correo_enviador, 'correo_receptor': correo})

    coleccionMensajeria = con_bd['Mensajes']
    if not coleccionMensajeria.find_one({'$or': [{'usuario1': correo, 'usuario2': correo_enviador}, {'usuario1': correo_enviador, 'usuario2': correo}]}):
        mensajes = Mensajes(correo, correo_enviador)
        coleccionMensajeria.insert_one(mensajes.formato_doc())

    return 'Se creo el chat'


@app.route('/mensajeria/<correo>')
def ventanaMensajeria(correo):
    usuarios = con_bd['users']
    usuario = usuarios.find_one({'correo': correo})
    colMensajes = con_bd['Mensajes']
    chats_usuario1 = list(colMensajes.find({'usuario1': correo}))
    chats_usuario2 = list(colMensajes.find({'usuario2': correo}))

    if chats_usuario1 or chats_usuario2:
        return render_template('mensajes.html', usuario_Existente=usuario, chats=chats_usuario1 + chats_usuario2)


@app.route('/enviarMensaje', methods=['POST'])
def enviarMensaje():
    Correo_usuario_Existente = request.form['usuario_Existente']
    mensaje = request.form['mensaje']
    autor = Correo_usuario_Existente
    fecha = datetime.now().strftime('Enviado a las %H:%M del %Y-%m-%d')
    usuarios = con_bd['users']
    usuario = usuarios.find_one({'correo': Correo_usuario_Existente})

    correo = usuario["correo"]

    _ID = ObjectId(usuario["_id"])
    colMensajes = con_bd['Mensajes']
    chats_usuario1 = list(colMensajes.find({'usuario1': correo}))
    chats_usuario2 = list(colMensajes.find({'usuario2': correo}))

    coleccionMensajeria = con_bd['Mensajes']
    coleccionMensajeria.update_one(
        {'_id': _ID},
        {'$push': {'mensajes': {'autor': autor, 'contenido': mensaje, 'fecha': fecha}}}
    )
    print('Enviado')
    # return f'{Correo_usuario_Existente}{mensaje}{autor}{fecha}'
    return render_template('mensajes.html', usuario_Existente=Correo_usuario_Existente, chats=chats_usuario1 + chats_usuario2)
    # revisar el envio de mensajes y una nueva forma para accesasr al chat


@ app.route('/pagina_principal')
def pagina_principla(datos_usuario):

    return render_template('pagina_principal.html', datos_usuario=datos_usuario)


@ app.route('/publicacion')
def agregarUser():
    return render_template('publicacion.html')


@ app.route('/personInformation')
def inforPerson():
    return render_template('informacionPersona.html')

# modulo de configuraciones


@ app.route('/configuracion')
def configuracion():
    return render_template('configuracionCuenta.html')


@ app.route('/mensajes')
def mesnajes():
    return render_template('mensajes.html')


if __name__ == '__main__':
    app.run(debug=True)
