import constants

from sqlalchemy import create_engine

import os

username = os.environ['EMOJIPREDICT_DB_USERNAME']
password = os.environ['EMOJIPREDICT_DB_PASSWORD']

engine = create_engine(
    f'mysql://{username}:{password}@localhost:3306/emojipredict')

data = []

# Visualize
conn = engine.connect()
results = conn.execute('select ID, data, class from data;')
classes = {0: 0, 1: 0}
for row in results:
    _class = row['class']
    classes[_class] += 1
    record = {
        'class': row['class'],
        'data': row['data'].split(',')
    }
    data.append(record)
conn.close()

print('Number of data points per class')
print(classes)

features = {}
classes = {}
for i in range(constants.NUM_FEATURES):
    features[i] = {
        'c00': 0,
        'c01': 0,
        'c10': 0,
        'c11': 0,
    }
for i in range(constants.NUM_CLASSES):
    classes[i] = {
        'c': 0,
    }

train = range(0, 512)
counter = 0

for record in data:
    # if (counter < limit):
    #     counter+=1
    # else:
    #     continue

    if counter not in train:
        counter+=1
        continue

    counter+=1

    _class = record['class']
    classes[record['class']]['c'] += 1
    for i in range(constants.NUM_FEATURES):
        value = record['data'][i]
        index = f'c{value}{_class}'

        features[i][index] += 1

# # print(features[463])
# print(features[800])

conn = engine.connect()
conn.execute('delete from feature;')
conn.close()

conn = engine.connect()
for i in range(constants.NUM_FEATURES):
    f = features[i]
    features[i]['p00'] = (f['c00']+1) / (f['c00'] + f['c10'] + 2)
    features[i]['p10'] = (f['c10']+1) / (f['c00'] + f['c10'] + 2)
    features[i]['p01'] = (f['c01']+1) / (f['c01'] + f['c11'] + 2)
    features[i]['p11'] = (f['c11']+1) / (f['c01'] + f['c11'] + 2)
    conn.execute(
        f"""insert into feature values (   {i},
                                            {features[i]['c00']}, {features[i]['c01']}, {features[i]['c10']}, {features[i]['c11']},
                                            {features[i]['p00']}, {features[i]['p01']}, {features[i]['p10']}, {features[i]['p11']});""")
conn.close()

conn = engine.connect()
conn.execute('delete from class;')
conn.close()

conn = engine.connect()
for i in range(constants.NUM_CLASSES):
    classes[i]['p'] = (classes[i]['c'] + 1) / (classes[i]['c'] + classes[1]['c'] + 2)
    conn.execute(
        f"insert into class values ({i}, {classes[i]['c']}, {classes[i]['p']})")

# print(features[463])
print(features[800])
print(classes)
