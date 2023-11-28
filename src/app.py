import sys
from datetime import datetime
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, login_required, logout_user
from flask_htmx import HTMX
from sqlalchemy.exc import IntegrityError as SQLIntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



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
htmx = HTMX(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), default="")
    last_name = db.Column(db.String(80), default="")
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', back_populates='user')


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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='posts')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the post was created
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp when the post was last modified
    
    def __repr__(self):
        return f'<Post {self.title}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/posts')
def posts():
    context = CONTEXT.copy()
    context.update({
        'active_tab': 'posts',
        'user': current_user,
        'posts': Post.query.all()  # Fetch all posts from the database
    })
    return render_template('posts.html', **context)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    context = CONTEXT.copy()
    context.update({
        'active_tab': 'create-post',
        'user': current_user,
    })

    if request.method == 'POST':
        # Get post data from the form
        title = request.form['title']
        content = request.form['content']

        # Create a new post object and associate it with the current user
        new_post = Post(title=title, content=content, user=current_user)

        # Add the post to the database session and commit the changes
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('posts'))  # Redirect to the list of posts page after creating a post

    return render_template('create_post.html', **context)

@app.post("/ping")
def route_clicked():
    print("ping")
    return """<button class="btn btn-lg btn-secondary" hx-post="/pong" hx-swap="outerHTML">Pong</button>"""

@app.post("/pong")
def route_pong():
    print("pong")
    return """<button class="btn btn-lg btn-primary" hx-post="/ping" hx-swap="outerHTML">Ping</button>"""

@app.route('/')
def index():
    context = CONTEXT.copy()
    context.update({
        'active_tab':'index',
        'user' : current_user,
    })
    return render_template('index.html', **context)

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
                flash('Du må skrive inn et gyldig brukernavn!', 'warning')
        else:
            flash('Du må skrive inn et gyldig brukernavn!', 'warning')

        
        if user and password_valid:
            flash(f'Innloggingen var vellykket, velkommen tilbake {user}!', 'success')
            flash(f'Vi setter pris på ditt medlemskap', 'warning')
            flash(f'Betal mere penger ellers smeller det!', 'danger')
            
            login_success = login_user(user)  # Log the user in
            if not login_user:
                # User is disabled with is_active=False
                flash('Beklager, men denne brukerkontoen er deaktivert!', 'warning')
                return redirect(url_for('login'))

            return redirect(url_for('index'))
        else:
            flash('Feil med pålogging', 'warning')
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
        if 'drop_all' in sys.argv:
            # DROP ALL TABLES, RESET ALL DATA
            # USE THIS TO DELETE ALL DATA
            if 'y' == input('WARNING, THIS WILL DELETE ALL DATA! CONTINUE? (y/n)').lower():
                 print('OK, DROPPING ALL TABLES...')
                 db.drop_all()
                 print('ALL TABLES DROPPED, DATA RESET!')
        db.create_all()
    app.run(
        debug=True, 
        # host="10.82.65.199", # lokalnettverk - replace with lan ip
        # host="0.0.0.0", # alle interfaces
        # port=80 # krever admin/root - bruk standard http port
            )
