from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

# Define your models here

# Clear all tables
def clear_all_tables():
    with app.app_context():

        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

if __name__ == '__main__':
    clear_all_tables()
    print("All tables cleared.")
