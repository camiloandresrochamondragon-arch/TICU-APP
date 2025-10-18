from flask import Flask, render_template

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Mundos TICU
@app.route('/mundos/programacion')
def mundo_programacion():
    return render_template('mundos/programacion.html')

@app.route('/mundos/multimedia')
def mundo_multimedia():
    return render_template('mundos/multimedia.html')

@app.route('/mundos/internet-seguro')
def mundo_internet_seguro():
    return render_template('mundos/internet_seguro.html')

@app.route('/mundos/robotica')
def mundo_robotica():
    return render_template('mundos/robotica.html')

@app.route('/mundos/ciberseguridad')
def mundo_ciberseguridad():
    return render_template('mundos/ciberseguridad.html')

@app.route('/mundos/creacion-contenido')
def mundo_creacion_contenido():
    return render_template('mundos/creacion_contenido.html')

@app.route('/mundos/inteligencia-artificial')
def mundo_inteligencia_artificial():
    return render_template('mundos/inteligencia_artificial.html')

@app.route('/mundos/realidad-virtual')
def mundo_realidad_virtual():
    return render_template('mundos/realidad_virtual.html')

@app.route('/mundos/redes-sociales')
def mundo_redes_sociales():
    return render_template('mundos/redes_sociales.html')

@app.route('/mundos/videojuegos')
def mundo_videojuegos():
    return render_template('mundos/videojuegos.html')

# Secciones generales
@app.route('/universo-tic')
def universo_tic():
    return render_template('universo_tic.html')

@app.route('/sala-retos-tic')
def sala_retos_tic():
    return render_template('sala_retos_tic.html')

@app.route('/herramientas-tic')
def herramientas_tic():
    return render_template('herramientas_tic.html')

# Página de error personalizada (opcional)
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)