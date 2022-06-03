from flask import Flask
from flask import render_template

app = Flask(__name__)


import requests
import pandas as pd
import json


class mlbDataFrame:
    def __init__(self):
        self.pullMlbData()
    def pullMlbData(self):
        content = requests.get('https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=2021&sportId=1&stats=season&group=hitting&gameType=P&limit=600&offset=0&sortStat=totalBases&order=desc').content
        j = json.loads(content)['stats']
        df = pd.DataFrame(j)
        df['pickTheStickValue'] = (df.totalBases+df.baseOnBalls+df.stolenBases) - 0.5*(df.atBats-df.hits+df.caughtStealing)
        self.battingDataFrame = df.sort_values(by='pickTheStickValue',ascending=False,inplace=False)

    def generateHtml(self):
        self.minimizedDf = self.battingDataFrame.copy()[['playerInitLastName','teamAbbrev','pickTheStickValue']]
        self.minimizedDf.columns = ('Player','Team','Points')
        self.htmlDataFrame = self.minimizedDf.to_html()
        return self.htmlDataFrame

data = mlbDataFrame()

@app.route("/")
def landingPage():
    return render_template('landingPage.html')

@app.route('/points')
def dataPage():
    return data.generateHtml()