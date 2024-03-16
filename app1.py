from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    profile = db.relationship('Profile', uselist=False, backref='user', lazy=True)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    full_name = request.form['full_name']

    user = User(username=username)
    profile = Profile(full_name=full_name)

    user.profile = profile

    db.session.add(user)
    db.session.commit()

    return render_template('index.html', users=User.query.all())


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
