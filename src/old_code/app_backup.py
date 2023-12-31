
import itertools
import time
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, login_required, logout_user
from flask_htmx import HTMX
from sqlalchemy.exc import IntegrityError as SQLIntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

import cv2

import os

basepath = os.getcwd()
static_path = os.path.join(basepath,'static')

CONTEXT = { # put settings here
    'site_title' : 'Arvids morohule',
    'site_title_url_target' : '/',
    'welcome_msg' : 'Hei og velkommen til Arvids morohule',
    'default_profile_pic' : '/media/default_profile_pic.png',
    'allow_anonymous_users' : True,
    'live_stream' : True,

           }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
camera=cv2.VideoCapture(0)
htmx = HTMX(app)
live_stream = CONTEXT['live_stream']

def generate_frames():
    while live_stream:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.png',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    if not live_stream:
        return None
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


# Chat room

# ... (your existing code)

messages = []  # List to store messages

@app.route('/chat')
@login_required
def chat():
    context = CONTEXT.copy()
    context.update({
        'active_tab': 'chat',
        'user': current_user,
    })
    return render_template('chat.html', **context)

@app.route('/send-message', methods=['POST'])
@login_required
def send_message():
    message = request.form['message']
    messages.append(f'{current_user.username}: {message}')
    return jsonify({'success': True})

@app.route('/chat-stream')
def chat_stream():
    def generate_messages():
        for idx, message in enumerate(itertools.count()):
            yield f'data: <li>{messages[-1]}</li>\n\n'
            time.sleep(0.1)

    return Response(generate_messages(), mimetype="text/event-stream")





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    # level = db.Column(db.Integer)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            # Hvis både fornavn og etternavn er satt
            # Vis fornavn + etternavn
            return f'{self.first_name} {self.last_name}'
        
        # Hvis ikke, bare vis brukernavnet
        return self.username

    @property
    def display_name(self):
        return self.full_name
            
    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


messages = []  # List to store messages

@app.post("/start-connection")
def start_connection():
    return """<div hx-ext="sse" sse-connect="/connect" sse-swap="message">
        Contents of this box will be updated in real time
        with every SSE message received from the chatroom.
    </div>"""

@app.route("/connect")
def publish_hello():
    def stream():
        for idx in itertools.count():
            msg = f'data: <p class=" card-text">Det har gått <strong>{idx}</strong> sekunder</p>\n\n'
            yield msg
            time.sleep(0.1)

    return Response(stream(), mimetype="text/event-stream")

@app.post("/ping")
def route_clicked():
    print("ping")
    return """<button class="btn btn-lg btn-secondary" hx-post="/pong" hx-swap="outerHTML">Pong</button>"""

@app.post("/pong")
def route_pong():
    print("pong")
    return """<button class="btn btn-lg btn-primary" hx-post="/ping" hx-swap="outerHTML">Ping</button>"""

@app.route('/static')
def static_view():
    context = CONTEXT.copy()
    context.update({
        'active_tab':'index',
        'user' : current_user,
    })
    return render_template('index.html', **context)

@app.route('/')
def index():
    context = CONTEXT.copy()
    context.update({
        'active_tab':'index',
        'user' : current_user,
    })
    return render_template('index.html', **context)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    context = CONTEXT.copy()
    context.update({
        'active_tab' : 'profile',
        'user' : current_user,
        'userdata' : vars(current_user), # testing
    })
    return render_template('profile.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    context = CONTEXT.copy()
    context.update({
        'active_tab':'register',
        'user' : current_user,
    })

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password) 
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except SQLIntegrityError as e:
            # User already exists
            flash('Brukernavnet eksisterer fra før, beklager!','warning')
            return redirect(url_for('register'))
        
        flash('Brukerkonto opprettet, gratulerer!', 'success')
        
        return redirect(url_for('login'))
    return render_template('register.html',**context)

@app.route('/login', methods=['GET', 'POST'])
def login():

    context = CONTEXT.copy()
    context.update({
        'active_tab':'login',
        'user' : current_user,
    })

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password:
                password_valid = check_password_hash(user.password, password)
            else:
                flash("Du må skrive inn et gyldig brukernavn!")
        else:
            flash("Du må skrive inn et gyldig brukernavn!")

        
        if user and password_valid:
            flash(f'Innloggingen var vellykket, velkommen tilbake {user}!', 'success')
            flash(f'Vi setter pris på ditt medlemskap', 'warning')
            flash(f'Betal mere penger ellers smeller det!', 'danger')
            
            login_user(user)  # Log the user in

            return redirect(url_for('index'))
        else:
            flash('Feil med pålogging', 'error')
    return render_template('login.html',**context)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Du ble logget ut","warning")
    return redirect('/')


@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
    context = CONTEXT.copy()
    context.update({
        'active_tab': 'profile',
        'user': current_user,
    })

    if request.method == 'POST':
        # Get updated profile information from the form
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']

        # Update the user's profile information in the database
        current_user.first_name = new_first_name
        current_user.last_name = new_last_name

        # Commit changes to the database
        db.session.commit()

        flash('Profil oppdatert!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile_update.html', **context)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, 
            # host="10.82.65.199", 
            # port=80,
            )
