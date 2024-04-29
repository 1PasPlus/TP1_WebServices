from faker import Faker
import random
from datetime import datetime
from flask import Flask

# -------------- Partie 2.2 -------------- 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------- Partie 2.2.3 -------------- 

def populate_tables_with_orm():
    fake = Faker()
    apps = ['twitter', "facebook", "instagram", "snapchat", "Linkedin"]
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randint(18, 50)
        email = fake.email()
        job = fake.job().replace("'", "")

        user = User(firstname=firstname, lastname=lastname, age=age, email=email, job=job)
        db.session.add(user)
        db.session.commit()

        num_apps = random.randint(1, 5)
        for _ in range(num_apps):
            username = fake.user_name()
            lastconnection = datetime.now()
            app_name = random.choice(apps)

            app = App(appname=app_name, username=username, lastconnection=lastconnection, user=user)
            db.session.add(app)
            db.session.commit()

# -------------- Partie 2.2.4 -------------- 

@app.route("/users", methods=["GET"])
def get_users_with_apps():
    users = User.query.all()
    data = []
    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "age": user.age,
            "email": user.email,
            "job": user.job,
            "apps": [{
                "appname": app.appname,
                "username": app.username,
                "lastconnection": app.lastconnection
            } for app in user.apps]
        }
        data.append(user_data)

    return {"users": data}

# -------------- Test de la partie 2.2 -------------- 
if __name__ == "__main__":

    from flask_sqlalchemy import SQLAlchemy
    app.app_context().push()  
    db = SQLAlchemy(app)  

    # -------------- Partie 2.2.2 -------------- 
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        firstname = db.Column(db.String(100))
        lastname = db.Column(db.String(100))
        age = db.Column(db.Integer)
        email = db.Column(db.String(200))
        job = db.Column(db.String(100))
        apps = db.relationship('App', backref='user', lazy=True)

    class App(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        appname = db.Column(db.String(100))
        username = db.Column(db.String(100))
        lastconnection = db.Column(db.TIMESTAMP(timezone=True))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    db.create_all()
    populate_tables_with_orm()

    users_orm = get_users_with_apps()
    print (users_orm)

    app.run(host="0.0.0.0", port=8181)
