from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# declarative_base :in sqlalchemy ORM style, declarative_base is a replacement for metadata object

engine = create_engine('sqlite:///orm_db.db', echo=True)

Base = declarative_base() # we will inherit from Base in our classes

class Person(Base):  # the name of table in our python code is Person
    __tablename__ = 'people' # the name of the table in db
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    things = relationship('Thing', back_populates='person') # here we defined a relationshp, using this attribute we will be able to have access to things that beong to each person

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id')) # owner will get its value from people id from people table

    person = relationship('Person', back_populates='things')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_person = Person(name='p2', age='35',)
session.add(new_person)
session.flush()  # flush temporarily add newperson so if we need this for other folowing lines we whould not et error - but still we do not commit and this flush is temporarily- to save new person in db we will commit in the following lines

# new_thing = Thing(description='camera', value=50.5, owner=new_person.id)
new_thing = Thing(description='camera2', value=20.5, owner=new_person.id)
session.add(new_thing)

session.commit()

print ([t.description for t in new_person.things])
print(new_thing.person.name)

# -----queries ---

result = session.query(Person.id, Person.name, Person.age).all() #output list of python tuples included id,name,age of all rows of table person in db
print (result)

# other way for abve code
print('**************')
result2 = session.query(Person).all()  #>>out put a lsit of python objects
print ([p.name for p in result2])

# --------- filter --------
print('*************')
result3 = session.query(Person.name, Person.age).filter(Person.age <31).all()
print (result3)

# ---------------- delete -----------
result4 = session.query(Thing).filter(Thing.value < 50).delete()
session.commit()

# ------- update --------------
result5 = session.query(Person).filter(Person.name=='p1').update({'name':'updated_name'})
session.commit()

#------------- join ---------
result6 = session.query(Person.name, Thing.description).join(Thing).all()
print ('join*********')
print ( result6)

#----------------- aggregation -----------
result7 = session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).all()

print('aggregation********')
print(result7)

#--------- having
result8 = session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).having(Thing.value<70).all()

print('aggregation - having cluase ********')
print(result8)

#---------close---------
session.close()

