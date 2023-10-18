from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError as SQLIntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

CONTEXT = { # put settings here
    'site_title' : 'Arvids morohule',
    'site_title_url_target' : '/',
    'welcome_msg' : 'Hei og velkommen til Arvids morohule',
    'default_profile_pic' : '/media/default_profile_pic.png',
    'allow_anonymous_users' : True,

           }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

login_manager = LoginManager(app)
db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        
        flash('Account created successfully!', 'success')
        
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
        password_valid = check_password_hash(user.password, password)
        if user and password_valid:
            flash(f'Innloggingen var vellykket, velkommen tilbake {user}!', 'success')
            flash(f'Vi setter pris på ditt medlemskap', 'warning')
            flash(f'Betal mere penger ellers smeller det!', 'danger')
            
            login_user(user)  # Log the user in

            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html',**context)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Du ble logget ut","warning")
    return redirect('/')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
