import constants

from sqlalchemy import create_engine

import os

username = os.environ['EMOJIPREDICT_DB_USERNAME']
password = os.environ['EMOJIPREDICT_DB_PASSWORD']

engine_ml = create_engine(
    f'mysql://{username}:{password}@localhost:3306/emojipredict')

conn_ml = engine_ml.connect()
results = conn_ml.execute('select data, class from data order by ID;')
conn_ml.close()

for row in results:
    print(f"{row['class']},{row['data']}")
