import os, json, random
from pymongo import MongoClient
from bson.json_util import dumps
from flask import Flask, render_template, url_for, request, redirect, flash, request, send_from_directory, jsonify

mongo = MongoClient("mongodb+srv://thomas:{DB_PASSWORD}@cluster0.640kn.mongodb.net/jokemon?retryWrites=true&w=majority".format(DB_PASSWORD=os.getenv("DB_PASSWORD")))
db = mongo.jokemon

app = Flask(__name__)

rarity_vals = [
    {
        "title":"Joesus Christ",
        "color":0
    },
    {
        "title":"Mythic",
        "color": 15401215
    },
    {
        "title":"Legendary",
        "color": 5375
    },
    {
        "title":"Rare",
        "color": 16711680
    },
    {
        "title":"Special",
        "color": 65321
    },
    {
        "title":"Fundamental",
        "color": 5127936
    },
]

rarity_weights = [
    0.0001,
    0.0499,
    0.1, 
    0.15,
    0.3,
    0.4 
]

# Main Routes

@app.route('/')
def index():
    players = json.loads(dumps(list(db.temp_user.find())))
    for player in players:
        player['card_count'] = len(player['card_inventory'])
    players = list(sorted(players, key=lambda players: player['card_count'], reverse=True))[::-1]
    return render_template("index.html", first=players[0], second=players[1], third=players[2])

@app.route('/cards')
def cards():
    joes = json.loads(dumps(list(db.jokemon.find())))
    joesus = []
    mythic = []
    legendary = []
    rare = []
    special = []
    fundamental = []
    for joe in joes:
        if joe['rarity']['title'] == 'Mythic':
            mythic.append(joe)
        elif joe['rarity']['title'] == 'Legendary':
            legendary.append(joe)
        elif joe['rarity']['title'] == 'Rare':
            rare.append(joe)
        elif joe['rarity']['title'] == 'Special':
            special.append(joe)
        elif joe['rarity']['title'] == 'Fundamental':
            fundamental.append(joe)
        elif joe['rarity']['title'] == 'Joesus Christ':
            joe['title'] = '?'*len(joe['title'].split(' ')[0]) + ' ' + joe['title'].split(' ')[1]
            joesus.append(joe)
    return render_template("cards.html", card_rarities=[joesus,mythic,legendary,rare,special,fundamental])

@app.route('/leaderboard')
def leaderboard():
    players = json.loads(dumps(list(db.temp_user.find())))
    for player in players:
        player['card_count'] = len(player['card_inventory'])
    players = list(sorted(players, key=lambda players: player['card_count'], reverse=True))[::-1]
    return render_template("leaderboard.html", players=players)

@app.route('/rarity')
def rarity():
    return render_template("rarity.html")

@app.route('/lootbox')
def lootbox():
    joes = json.loads(dumps(list(db.jokemon.find())))
    joesus = []
    mythic = []
    legendary = []
    rare = []
    special = []
    fundamental = []
    for joe in joes:
        if joe['rarity']['title'] == 'Mythic':
            mythic.append(joe)
        elif joe['rarity']['title'] == 'Legendary':
            legendary.append(joe)
        elif joe['rarity']['title'] == 'Rare':
            rare.append(joe)
        elif joe['rarity']['title'] == 'Special':
            special.append(joe)
        elif joe['rarity']['title'] == 'Fundamental':
            fundamental.append(joe)
        elif joe['rarity']['title'] == 'Joesus Christ':
            joe['image_url'] = 'https://www.digiseller.ru/preview/599286/p1_2134247_b8bd3e19.png'
            joesus.append(joe)
    # Handle randomizing and weighting here
    results = []
    d = random.random()
    if d >= 0.05:
        joesus = []
    cards=[random.sample(joesus, len(joesus)),random.sample(mythic,len(mythic))[:1],random.sample(legendary,len(legendary))[:2],random.sample(rare, len(rare))[:3],random.sample(special, len(special))[:6],fundamental[:8]]
    for types in cards:
        for card in types:
            results.append(card)
    # Final shuffle 
    results = random.sample(results, len(results))
    return render_template("lootbox.html", cards=results)

# API
@app.route('/api/leaderboard')
def apiLeaderboard():
    jokemon = json.loads(dumps(list(db.jokemon.find())))
    return jsonify(jokemon)

@app.route('/api/winner', methods=['POST'])
def apiWinner():
    jokemon = json.loads(dumps(list(db.jokemon.find())))
    joes = json.loads(dumps(list(db.jokemon.find())))
    joesus = []
    mythic = []
    legendary = []
    rare = []
    special = []
    fundamental = []
    for joe in joes:
        if joe['rarity']['title'] == 'Mythic':
            mythic.append(joe)
        elif joe['rarity']['title'] == 'Legendary':
            legendary.append(joe)
        elif joe['rarity']['title'] == 'Rare':
            rare.append(joe)
        elif joe['rarity']['title'] == 'Special':
            special.append(joe)
        elif joe['rarity']['title'] == 'Fundamental':
            fundamental.append(joe)
        elif joe['rarity']['title'] == 'Joesus Christ':
            joe['image_url'] = 'https://www.digiseller.ru/preview/599286/p1_2134247_b8bd3e19.png'
            joesus.append(joe)
    results = []
    winner = None
    d = random.random()
    if d > 0 and d <= 0.4:
        winner = random.choice(fundamental)
    elif d > 0.4 and d <= 0.7:
        winner = random.choice(special)
    elif d > 0.7 and d <= 0.85:
        winner = random.choice(rare)
    elif d > 0.85 and d <= 0.95:
        winner = random.choice(legendary)
    elif d > 0.95 and d <= 0.999:
        winner = random.choice(mythic)
    elif d > 0.999 and d < 1:
        winner = random.choice(joesus)
    else:
        winner = random.choice(fundamental)
        
    return jsonify(winner)