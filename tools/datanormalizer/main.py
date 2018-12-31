from pymongo import MongoClient
from bson.objectid import ObjectId
import os


def normalize_references(game, node_name):
    print('Processing {0}'.format(node_name))
    nodes = game[node_name]
    print('Found {0} entries for {1}'.format(len(nodes), node_name))

    refs = []
    for node in nodes:
        if type(node) != ObjectId:
            existing = db[node_name].find_one({'name': node['name']})
            if existing is None:
                inserted = db[node_name].insert_one(node)
                refs.append(inserted.inserted_id)
            else:
                refs.append(existing['_id'])
        else:
            print('Weird. {0} {1} is already a ref'.format(node_name, node))
            refs.append(node)

    db.Games.update_one({'_id': game['_id']}, {'$set': {node_name: refs}})
    print('Successfully processed {0}'.format(node_name))



print("Starting program")
connstr = os.getenv('CONN_STR')
dbname = os.getenv('DB_NAME')

if connstr is None:
    raise Exception('Environment variable CONN_STR must be set first') 
if dbname is None:
    raise Exception('Environment variable DB_NAME must be set first') 

mongocli = MongoClient(connstr)
db = mongocli[dbname]

print('Connected to {0}'.format(dbname))
skip = 0
page_size = 1000

while True:
    games = list(db.Games.find().limit(page_size).skip(skip))
    retrieved_count = len(games)

    if retrieved_count == 0:
        exit

    skip = skip + retrieved_count

    print('Retrieved {0} games'.format(retrieved_count))

    for game in games:
        print('Processing game {0}'.format(game['name']))
        normalize_references(game, 'genres')
        normalize_references(game, 'publishers')
        normalize_references(game, 'developers')
        normalize_references(game, 'platforms')
        





