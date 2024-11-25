from flask import Flask, render_template, request, redirect, url_for, session

"""

Vas a desarrollar una aplicación web utilizando Flask que permita a los usuarios gestionar y clasificar series de televisión según su interés. La aplicación permitirá a los usuarios registrarse, iniciar sesión, y clasificar sus series en tres categorías: "Series que me gustarían ver", "Series que estoy viendo", y "Series vistas". Cada serie contendrá datos relevantes como su nombre, sinopsis, género, fecha de estreno, entre otros.

Objetivo del Ejercicio: El objetivo es crear una aplicación web funcional donde los usuarios puedan registrarse, autenticarse y gestionar sus series favoritas. La aplicación debe emplear plantillas Jinja2 para el renderizado dinámico de las páginas y utilizar los objetos request, session, y config de Flask para gestionar datos de formularios, sesiones de usuario y configuraciones de la aplicación.

Requisitos Funcionales:

    Registro de Usuarios:
        La aplicación debe permitir a los nuevos usuarios registrarse con un nombre de usuario y una contraseña.
        Si el usuario ya existe, se debe mostrar un mensaje indicando que el usuario ya está registrado.

    Inicio de Sesión:
        La aplicación debe permitir que los usuarios inicien sesión utilizando su nombre de usuario y contraseña.
        Si el inicio de sesión es correcto, el usuario será redirigido a la página principal de la aplicación.
        Si el nombre de usuario o la contraseña no coinciden, se debe mostrar un mensaje de error.

    Cerrar Sesión:
        Los usuarios deben tener la opción de cerrar sesión, lo que eliminará sus datos de la sesión actual y los redirigirá a la página de inicio de sesión.

    Página de Listado de Series:
        La aplicación debe contar con una página principal donde los usuarios puedan ver su lista de series en tres categorías: Series que me gustarían ver, Series que estoy viendo y Series vistas
        Cada categoría debe mostrar el nombre de la serie y su puntuación.

    Agregar Nuevas Series:
        Los usuarios deben poder agregar nuevas series mediante un formulario.
        Cada serie debe incluir los siguientes campos:
            Nombre de la serie
            Sinopsis
            Puntuación (de 0 a 10)
            Género
            Fecha de estreno
            Número de capítulos
            Duración de los capítulos (en minutos)
            Categoría de la serie (una de las tres mencionadas anteriormente)
        Al enviar el formulario, la serie debe ser añadida a la lista correspondiente y redirigir al usuario a la página principal.

"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'odio_javascript_que_asco'

usuarios = [
    {
        "nombre": "Jonatan",
        "usuario": "Administrador",
        "password": "supercontraseñachupifantastica",
        "pelis_fav": [],
        "pelis_viendo": [],
        "pelis_vistas": []
    }
]

@app.route("/")
def principal():
    if "logged_in" in session and session.get("username"):
        username = session.get('username')
        for usuario in usuarios:
            if usuario["usuario"] == username:
                pelis_fav = usuario["pelis_fav"]
                pelis_viendo = usuario["pelis_viendo"]
                pelis_vistas = usuario["pelis_vistas"]

                return render_template(
                "principal.html",
                    logged_in=True,
                    username=username,
                    pelis_fav=pelis_fav,
                    pelis_viendo=pelis_viendo,
                    pelis_vistas=pelis_vistas
                )
    return redirect(url_for('registro'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error = "El nombre de usario introducido ya está en uso"

    if request.method == 'POST':
        username = request.form['username']

        if comprueba_usuarios(username):
            return render_template('registro.html', error=error)

        name = request.form['name']
        password = request.form['password']

        nuevo_usuario = {
            "nombre": name,
            "usuario": username,
            "password": password,
            "pelis_fav": [],
            "pelis_viendo": [],
            "pelis_vistas": []
        }

        usuarios.append(nuevo_usuario)

        return render_template('login.html')

    return render_template('registro.html')


def comprueba_usuarios(user):
    for usuario in usuarios:
        if usuario["usuario"] == user:
            return True
    return False


@app.route('/login', methods=['GET', 'POST'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for usuario in usuarios:
            if usuario["usuario"] == username and usuario["password"] == password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('principal'))

        error = "Credenciales incorrectas, vuelve a intentarlo"
        return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout_function():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        name = request.form['name']
        synopsis = request.form['synopsis']
        rating = request.form['rating']
        genre = request.form['genre']
        date = request.form['date']
        chapters = request.form['chapters']
        category = request.form['categories']

        if 'username' in session:
            username = session['username']
            for usuario in usuarios:
                if usuario["usuario"] == username:
                    nueva_peli = {
                        "nombre": name,
                        "sinopsis": synopsis,
                        "Puntuacion": rating,
                        "genero": genre,
                        "date": date,
                        "chapters": chapters,
                        "category": category
                    }

                    if category == 'gusta':
                        usuario["pelis_fav"].append(nueva_peli)
                    elif category == 'ver':
                        usuario["pelis_viendo"].append(nueva_peli)
                    elif category == 'visto':
                        usuario["pelis_vistas"].append(nueva_peli)
        return redirect(url_for('principal'))

    return render_template('peliculas.html')



if __name__ == '__main__':
    app.run()
