import requests as r
from datetime import datetime
from flask import render_template,Flask
from bson.json_util import dumps, loads
import pandas as pd
import json




# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    #home=template_env.get_template('index.html')
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/champions')
def champions():
    """Renders the champion page."""
    champNames=get_champion()
    championDict=champNames.json()
    names=[]
    #this page gets all the champions on a list with their picture
    for x in range(len(championDict)):
        names.append(championDict[x]['id'])
    return render_template(
        'champion.html',
        title='Champions',
        champList=sorted(names),
        message='Landing page for champions'
    )

@app.route('/<string:id>')
def OneChamp(id):
    """Renders the champion specific page."""
    oneGuy=get_one_champ(str(id))
    file=oneGuy.json()
    with open('./jsonFiles/allSpellData.json') as f:
        spells=json.load(f)
    return render_template(
        'championSpecific.html',
        champ=oneGuy,
        name = file['name'],
        stats = file['stats'],
        blurb = file['blurb'],
        tags = file['tags'],
        nickname = file['title'],
        spells=spells[id],
        title='Champion Specific',
        year=datetime.now().year,
        message='Landing page for champions'
    )

@app.route('/stats')
def stats():
    """Renders the stats page."""
    champ=get_stats()
    table = pd.DataFrame.from_dict(champ)

    return render_template(
        'statsTest.html',
        title='Stats',
        stats=table,
        year=datetime.now().year,
        message='See all stats'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Learn about Jace'
    )

@app.route('/test')
def test():
    """Just a test"""
    return render_template(
        'test.html',
        title='About',
        year=datetime.now().year,
        message='Learn about html and ccss'
    )

def get_champion():
    return r.get("http://localhost:5000/api/v1/champions")

def get_champ_names():
    return r.get('http://localhost:5000/api/v1/championNames')

def get_one_champ(champ):
    return r.get(f'http://localhost:5000/api/v1/champions/{champ}')

def get_stats():
    return r.get('http://localhost:5000/api/v1/championstats')

if __name__ == '__main__':
    """
    HOST = environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(environ.get('SERVER_PORT', '5555'))
        except ValueError:
            PORT = 5555
        app.run(HOST, PORT)
    """
    app.run(port=5555,debug=True)