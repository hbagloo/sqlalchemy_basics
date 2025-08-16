from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///mydatabase.db')

conn = engine.connect()

conn.execute(text('CREATE TABLE IF NOT EXISTS people(name str, age int)'))
conn.commit()



# sessions >> to use ORM
session = Session(engine)

session.execute(text('INSERT INTO people (name, age) VALUES ("heydar", 38);'))
session.commit()
