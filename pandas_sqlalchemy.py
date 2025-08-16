import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydatabase.db')

df = pd.read_sql('SELECT * FROM people', con=engine)
print (df)

new_data=pd.DataFrame({'name':['pd_pesrson1', 'pd_person2'], 'age': [35,45]})
new_data.to_sql('people', con=engine, if_exists='append', index=False)