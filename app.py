import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_esto_en_produccion')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://postgres.kiofulhnplvuuamvclym:C4M1l04ndr3s2004@aws-0-us-east-2.pooler.supabase.com:6543/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ══════════════════════════════
# MODELOS
# ══════════════════════════════

class Usuario(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(100), unique=True, nullable=False)
    password      = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    progresos     = db.relationship('Progreso', backref='usuario', lazy=True)
    logros        = db.relationship('UsuarioLogro', backref='usuario', lazy=True)
    intentos      = db.relationship('Intento', backref='usuario', lazy=True)


class Modulo(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    slug        = db.Column(db.String(50), unique=True, nullable=False)
    nombre      = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    icono       = db.Column(db.String(10), default='📚')
    orden       = db.Column(db.Integer, nullable=False)
    puntaje_minimo = db.Column(db.Integer, default=7)
    total_preguntas = db.Column(db.Integer, default=10)


class Progreso(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    usuario_id  = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    modulo_id   = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    completado  = db.Column(db.Boolean, default=False)
    mejor_puntaje = db.Column(db.Integer, default=0)
    fecha_completado = db.Column(db.DateTime)
    modulo      = db.relationship('Modulo')


class Intento(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    usuario_id  = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    modulo_id   = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    puntaje     = db.Column(db.Integer, nullable=False)
    fecha       = db.Column(db.DateTime, default=datetime.utcnow)
    modulo      = db.relationship('Modulo')


class Logro(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    slug        = db.Column(db.String(50), unique=True, nullable=False)
    nombre      = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    icono       = db.Column(db.String(10), default='🏅')
    tipo        = db.Column(db.String(30), default='modulo')


class UsuarioLogro(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    usuario_id  = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    logro_id    = db.Column(db.Integer, db.ForeignKey('logro.id'), nullable=False)
    fecha       = db.Column(db.DateTime, default=datetime.utcnow)
    logro       = db.relationship('Logro')


# ══════════════════════════════
# USER LOADER
# ══════════════════════════════

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


# ══════════════════════════════
# INICIALIZAR BD
# ══════════════════════════════

MODULOS_INICIALES = [
    dict(slug='programacion',          nombre='Programación',          icono='💻', orden=1,  descripcion='Lógica, algoritmos y creación de soluciones digitales.'),
    dict(slug='multimedia',            nombre='Multimedia',            icono='🎨', orden=2,  descripcion='Diseño, edición de contenido y comunicación visual.'),
    dict(slug='internet-seguro',       nombre='Internet Seguro',       icono='🛡️', orden=3,  descripcion='Navega de forma segura y protege tu información.'),
    dict(slug='ciberseguridad',        nombre='Ciberseguridad',        icono='🔐', orden=4,  descripcion='Amenazas digitales, privacidad y defensa en línea.'),
    dict(slug='robotica',              nombre='Robótica',              icono='🤖', orden=5,  descripcion='Máquinas programables, sensores y automatización.'),
    dict(slug='inteligencia-artificial', nombre='Inteligencia Artificial', icono='🧠', orden=6, descripcion='IA, algoritmos de aprendizaje y ética digital.'),
    dict(slug='videojuegos',           nombre='Videojuegos',           icono='🎮', orden=7,  descripcion='Diseño, mecánicas y creación de videojuegos.'),
    dict(slug='redes-sociales',        nombre='Redes Sociales',        icono='📱', orden=8,  descripcion='Comunicación digital, privacidad y ciudadanía digital.'),
    dict(slug='realidad-virtual',      nombre='Realidad Virtual',      icono='🕶️', orden=9,  descripcion='Simulaciones inmersivas, VR y entornos 360°.'),
    dict(slug='creacion-contenido',    nombre='Creación de Contenido', icono='📸', orden=10, descripcion='Podcasts, videos, diseño y publicaciones digitales.'),
]

LOGROS_INICIALES = [
    dict(slug='primer-codigo',     nombre='Primer Código',         icono='💻', tipo='modulo',   descripcion='Completaste el mundo de Programación.'),
    dict(slug='artista-digital',   nombre='Artista Digital',       icono='🎨', tipo='modulo',   descripcion='Completaste el mundo de Multimedia.'),
    dict(slug='guardian-digital',  nombre='Guardián Digital',      icono='🛡️', tipo='modulo',   descripcion='Completaste Internet Seguro.'),
    dict(slug='hacker-etico',      nombre='Hacker Ético',          icono='🔐', tipo='modulo',   descripcion='Completaste el mundo de Ciberseguridad.'),
    dict(slug='robotista',         nombre='Robotista',             icono='🤖', tipo='modulo',   descripcion='Completaste el mundo de Robótica.'),
    dict(slug='mente-artificial',  nombre='Mente Artificial',      icono='🧠', tipo='modulo',   descripcion='Completaste Inteligencia Artificial.'),
    dict(slug='game-designer',     nombre='Game Designer',         icono='🎮', tipo='modulo',   descripcion='Completaste el mundo de Videojuegos.'),
    dict(slug='influencer-tic',    nombre='Influencer TIC',        icono='📱', tipo='modulo',   descripcion='Completaste Redes Sociales.'),
    dict(slug='explorador-vr',     nombre='Explorador VR',         icono='🕶️', tipo='modulo',   descripcion='Completaste Realidad Virtual.'),
    dict(slug='creador-tic',       nombre='Creador TIC',           icono='📸', tipo='modulo',   descripcion='Completaste Creación de Contenido.'),
    dict(slug='maestro-tic',       nombre='Maestro TIC',           icono='🏆', tipo='especial', descripcion='¡Completaste TODOS los mundos!'),
    dict(slug='quiz-perfecto',     nombre='Quiz Perfecto',         icono='⭐', tipo='especial', descripcion='Obtuviste 10/10 en algún quiz.'),
    dict(slug='perseverante',      nombre='Perseverante',          icono='💪', tipo='especial', descripcion='Pasaste un quiz en el segundo intento.'),
]

LOGRO_POR_MODULO = {
    'programacion':         'primer-codigo',
    'multimedia':           'artista-digital',
    'internet-seguro':      'guardian-digital',
    'ciberseguridad':       'hacker-etico',
    'robotica':             'robotista',
    'inteligencia-artificial': 'mente-artificial',
    'videojuegos':          'game-designer',
    'redes-sociales':       'influencer-tic',
    'realidad-virtual':     'explorador-vr',
    'creacion-contenido':   'creador-tic',
}


def inicializar_db():
    db.create_all()

    for m in MODULOS_INICIALES:
        if not Modulo.query.filter_by(slug=m['slug']).first():
            db.session.add(Modulo(**m))

    for l in LOGROS_INICIALES:
        if not Logro.query.filter_by(slug=l['slug']).first():
            db.session.add(Logro(**l))

    db.session.commit()


# ══════════════════════════════
# HELPERS
# ══════════════════════════════

def puede_acceder(usuario_id, slug_modulo):
    modulo = Modulo.query.filter_by(slug=slug_modulo).first()
    if not modulo:
        return False
    if modulo.orden == 1:
        return True
    anterior = Modulo.query.filter_by(orden=modulo.orden - 1).first()
    if not anterior:
        return True
    progreso = Progreso.query.filter_by(usuario_id=usuario_id, modulo_id=anterior.id).first()
    return progreso and progreso.completado


def otorgar_logro(usuario_id, logro_slug):
    logro = Logro.query.filter_by(slug=logro_slug).first()
    if not logro:
        return
    ya_tiene = UsuarioLogro.query.filter_by(usuario_id=usuario_id, logro_id=logro.id).first()
    if not ya_tiene:
        db.session.add(UsuarioLogro(usuario_id=usuario_id, logro_id=logro.id))
        db.session.commit()


def get_estado_modulos(usuario_id):
    todos = Modulo.query.order_by(Modulo.orden).all()
    progresos = {p.modulo_id: p for p in Progreso.query.filter_by(usuario_id=usuario_id).all()}
    result = []
    for m in todos:
        p = progresos.get(m.id)
        accede = puede_acceder(usuario_id, m.slug)
        result.append({
            'modulo': m,
            'progreso': p,
            'completado': p.completado if p else False,
            'mejor_puntaje': p.mejor_puntaje if p else 0,
            'puede_acceder': accede,
        })
    return result


# ══════════════════════════════
# RUTAS PRINCIPALES
# ══════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/herramientas')
def herramientas():
    return render_template('herramientas_tic.html')


@app.route('/universo')
def universo():
    return render_template('universo_tic.html')


@app.route('/retos')
def retos():
    modulos = Modulo.query.order_by(Modulo.orden).all()
    estado = get_estado_modulos(current_user.id) if current_user.is_authenticated else []
    return render_template('sala_retos_tic.html', modulos=modulos, estado=estado)


# ══════════════════════════════
# MUNDOS
# ══════════════════════════════

TEMPLATE_MAP = {
    'programacion':            'mundos/programacion.html',
    'multimedia':              'mundos/multimedia.html',
    'internet-seguro':         'mundos/internet_seguro.html',
    'ciberseguridad':          'mundos/ciberseguridad.html',
    'robotica':                'mundos/robotica.html',
    'inteligencia-artificial': 'mundos/inteligencia_artificial.html',
    'videojuegos':             'mundos/videojuegos.html',
    'redes-sociales':          'mundos/redes_sociales.html',
    'realidad-virtual':        'mundos/realidad_virtual.html',
    'creacion-contenido':      'mundos/creacion_contenido.html',
}


@app.route('/mundos/<slug>')
@login_required
def mundo(slug):
    modulo = Modulo.query.filter_by(slug=slug).first_or_404()
    if not puede_acceder(current_user.id, slug):
        anterior = Modulo.query.filter_by(orden=modulo.orden - 1).first()
        return render_template('bloqueado.html', modulo=modulo, anterior=anterior)
    template = TEMPLATE_MAP.get(slug)
    if not template:
        return render_template('404.html'), 404
    progreso = Progreso.query.filter_by(usuario_id=current_user.id, modulo_id=modulo.id).first()
    intentos_count = Intento.query.filter_by(usuario_id=current_user.id, modulo_id=modulo.id).count()
    return render_template(template, modulo=modulo, progreso=progreso, intentos_count=intentos_count)


# ══════════════════════════════
# GUARDAR RESULTADO QUIZ (AJAX)
# ══════════════════════════════

@app.route('/quiz/resultado', methods=['POST'])
@login_required
def guardar_resultado():
    data    = request.get_json()
    slug    = data.get('slug')
    puntaje = int(data.get('puntaje', 0))
    total   = int(data.get('total', 10))

    modulo = Modulo.query.filter_by(slug=slug).first()
    if not modulo:
        return jsonify(success=False, error='Módulo no encontrado'), 404
    if not puede_acceder(current_user.id, slug):
        return jsonify(success=False, error='Sin acceso'), 403

    intentos_previos = Intento.query.filter_by(usuario_id=current_user.id, modulo_id=modulo.id).count()
    db.session.add(Intento(usuario_id=current_user.id, modulo_id=modulo.id, puntaje=puntaje))

    progreso = Progreso.query.filter_by(usuario_id=current_user.id, modulo_id=modulo.id).first()
    if not progreso:
        progreso = Progreso(usuario_id=current_user.id, modulo_id=modulo.id)
        db.session.add(progreso)

    if puntaje > progreso.mejor_puntaje:
        progreso.mejor_puntaje = puntaje

    nuevos_logros = []
    paso = puntaje >= modulo.puntaje_minimo

    if paso and not progreso.completado:
        progreso.completado = True
        progreso.fecha_completado = datetime.utcnow()
        logro_slug = LOGRO_POR_MODULO.get(slug)
        if logro_slug:
            otorgar_logro(current_user.id, logro_slug)
            nuevos_logros.append(logro_slug)
        completados = Progreso.query.filter_by(usuario_id=current_user.id, completado=True).count()
        if completados >= len(MODULOS_INICIALES):
            otorgar_logro(current_user.id, 'maestro-tic')
            nuevos_logros.append('maestro-tic')

    if puntaje == total:
        otorgar_logro(current_user.id, 'quiz-perfecto')
        nuevos_logros.append('quiz-perfecto')

    if paso and intentos_previos == 1:
        otorgar_logro(current_user.id, 'perseverante')
        nuevos_logros.append('perseverante')

    db.session.commit()
    return jsonify(success=True, paso=paso, puntaje=puntaje, minimo=modulo.puntaje_minimo, nuevos_logros=nuevos_logros)


# ══════════════════════════════
# AUTH
# ══════════════════════════════

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Usuario o contraseña incorrectos')
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if Usuario.query.filter_by(username=username).first():
            return render_template('registro.html', error='Ese nombre de usuario ya existe')
        nuevo = Usuario(username=username, password=generate_password_hash(password))
        db.session.add(nuevo)
        db.session.commit()
        login_user(nuevo)
        return redirect(url_for('dashboard'))
    return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ══════════════════════════════
# DASHBOARD
# ══════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    estado = get_estado_modulos(current_user.id)
    logros_usuario = UsuarioLogro.query.filter_by(usuario_id=current_user.id).order_by(UsuarioLogro.fecha.desc()).all()
    todos_logros = Logro.query.all()
    logros_ids = {ul.logro_id for ul in logros_usuario}
    completados = sum(1 for e in estado if e['completado'])
    total = len(estado)
    pct = round((completados / total) * 100) if total else 0
    return render_template('dashboard.html', estado=estado, logros_usuario=logros_usuario,
                           todos_logros=todos_logros, logros_ids=logros_ids,
                           completados=completados, total=total, pct=pct)


# ══════════════════════════════
# ERRORES
# ══════════════════════════════

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_servidor(e):
    return render_template('404.html'), 500


# ══════════════════════════════
# RUN
# ══════════════════════════════

if __name__ == '__main__':
    with app.app_context():
        inicializar_db()
    app.run(debug=False)