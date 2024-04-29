from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime

db_string = "postgresql://root:root@localhost:5432/postgres"
engine = create_engine(db_string)

# -------------- Partie 2.1 -------------- 

create_user_table_sql = text("""
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INT,
    email VARCHAR(200),
    job VARCHAR(100)
)
""")

create_apps_table_sql = text("""
CREATE TABLE IF NOT EXISTS Apps (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnection TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES Users(id)
)
""")

def run_sql(query: str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(query)
        trans.commit()

def run_sql_with_results(query: str):
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(query)
        trans.commit()
        return result


# -------------- Partie 2.1.1 -------------- 

fake=Faker()
def populate_tables():
    apps=['twitter',"facebook","instagram","snapchat","Linkedin"]
    for i in range(100):
        firstname=fake.first_name()
        lastname=fake.last_name()
        age=random.randrange(18,50)
        email=fake.email()
        job=fake.job().replace("'","")
        insert_user_query=text(f"""
        INSERT INTO users (firstname, lastname, age, email, job)
        VALUES ('{firstname}','{lastname}','{age}','{email}','{job}')
        RETURNING id
        """)
        user_id=run_sql_with_results(insert_user_query).scalar()
        print(user_id)
        datetime.now

        num_apps=random.randint(1,5)
        for i in range(num_apps):
            username=fake.user_name()
            lastconnection=datetime.now()
            apps_name = random.choice(apps)
            sql_insert_app =text(f"""
            INSERT INTO apps (appname, username, lastconnection, user_id)
            VALUES ('{apps_name}','{username}','{lastconnection}','{user_id}')
            """)
            run_sql(sql_insert_app)

# -------------- Partie 2.1.2 -------------- 
def get_users():
    users = run_sql_with_results(text("SELECT * FROM users"))
    data=[]
    for row in users:
        user={
            "id":row[0],
            "firstname":row[1],
            "lastname":row[2],
            "age":row[3],
            "email":row[4],
            "job":row[5]
        }
        data.append(user)

    return data


# -------------- Test des parties 2.1 - 2.1.1 - 2.1.2 -------------- 
if __name__ == "__main__":

    #On créer nos tables et on ajoute les données factices dedans - 200 lignes factices sont ajoutées 
    run_sql(create_user_table_sql)
    run_sql(create_apps_table_sql)
    populate_tables()

    #Chopper la liste des utilisateurs 
    users = get_users()
    print(users)