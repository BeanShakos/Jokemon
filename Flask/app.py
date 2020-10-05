import os, json
from pymongo import MongoClient
from bson.json_util import dumps
from flask import Flask, render_template, url_for, request, redirect, flash, request, send_from_directory, jsonify

mongo = MongoClient("mongodb+srv://thomas:{DB_PASSWORD}@cluster0.640kn.mongodb.net/jokemon?retryWrites=true&w=majority".format(DB_PASSWORD=os.getenv("DB_PASSWORD")))
db = mongo.jokemon

app = Flask(__name__)

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
    joes = list(sorted(joes, key=lambda joe: joe['rarity']['title'], reverse=True))[::-1]
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

# API
@app.route('/api/leaderboard')
def apiLeaderboard():
    jokemon = json.loads(dumps(list(db.jokemon.find())))
    return jsonify(jokemon)