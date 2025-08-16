from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, func

engine = create_engine('sqlite:///mydatabase.db')

meta = MetaData()

people = Table(
    'people',
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

things = Table(
    'things',
    meta,
    Column('id', Integer, primary_key=True), 
    Column('description', String, nullable=False), 
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))
)

meta.create_all(engine)

conn = engine.connect()

#---------INSERT-----------------------
#insert_statement = people.insert().values(name='hacer', age=34)
#result = conn.execute(insert_statement)
#conn.commit()

#--------- SELECT-----------
# select_statement = people.select().where(people.c.age<36)
# result = conn.execute(select_statement)

# for row in result.fetchall():
#     print (row)

# ------------ update ---------
update_statement = people.update().where(people.c.name=='heydar').values(age=37)
result = conn.execute(update_statement)
conn.commit()

'''
with engine.begin() as conn:
    result = conn.execute(update_statement)
'''

#---------- delete --------------
'''
delete_statement = people.delete().where(people.c.name == 'heydar')
result = conn.execute(delete_statement)
conn.commit()
'''


'''
insert_statement = people.insert().values(name='heydar2',age=38)
result = conn.execute(insert_statement)
conn.commit()

'''
# 1 to many relationship - every person could have many things




insert_people = people.insert().values([
    {'name':'person1', 'age': 30},
    {'name':'person2', 'age': 31},
    {'name':'person3', 'age': 32},
    {'name':'person4', 'age': 33},
    {'name':'person5', 'age': 22},
    {'name':'person6', 'age': 39},
])

insert_things = things.insert().values([
    {'owner':2, 'description':'Laptop', 'value': 800.25},
    {'owner':2, 'description':'Mouse', 'value': 50.25},
    {'owner':2, 'description':'Keyboard', 'value': 100.25},
    {'owner':3, 'description':'Book', 'value': 30},
    {'owner':4, 'description':'Bottle', 'value': 10.25},
    {'owner':5, 'description':'Speaker', 'value': 80.25},
])


conn.execute(insert_people)
conn.commit() # since we use id frompepole in hings table , we first add peole and commit to have them in db, then we add things which will use the ids from persons

conn.execute(insert_things)
conn.commit()


join_statement = people.join(things, people.c.id == things.c.owner)  # we could also use outerjoin instead of just join 
select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement)

result = conn.execute(select_statement)

for row in result.fetchall():
    print(row)

#----------------------aggregation -------
group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner,).having(func.sum(things.c.value)>50)

result = conn.execute(group_by_statement)
for row in result.fetchall():
    print (row)
