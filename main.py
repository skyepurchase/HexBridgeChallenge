from flask import Flask, request, render_template, jsonify
import json
import traceback
import time
import atexit
import random
from apscheduler.schedulers.background import BackgroundScheduler
from model import Model
from scraper import Social, Scraper
#from plot.py import plot_network

app = Flask(__name__)
model=Model()
RESULTS_TO_SHOW=3
RANDOM_PAST_LENGTH=1

scraper = Scraper()

def update_model():
    global model
    model=Model()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_model, trigger="interval", minutes=1)
scheduler.start()


@app.route('/',methods=["GET"])
def root():
    return render_template('index.html')


def add_url(people):
    res=[]
    for p in people:
        for (social,id) in p.items():
            social_enum=Social.TWITTER if social=="twitter" else Social.REDDIT
            social_formatted="twitter-tweet" if social=="twitter" else "reddit-card"
            tweet_urls=scraper.get_user_comment_urls(social_enum,id,item_count=RANDOM_PAST_LENGTH)
            url=tweet_urls[0]#random.choice(tweets)
            res.append({"ID":id,"social":social_formatted,"link":url})
    return res

@app.route("/process",methods=["POST"])
def process():
    try:
        social=request.form['social']
        consent=request.form['consent']=='true'
        id=request.form['ID']
        posts=scraper.get_user_text(Social.REDDIT,id) if (social=="reddit") else scraper.get_user_text(Social.TWITTER,id)
        IDs={}
        IDs[social]=id
        close_ids,far_ids=model.process_user(IDs,posts,consent)
        close_id_num=min(len(close_ids),RESULTS_TO_SHOW)
        far_id_num=min(len(far_ids),RESULTS_TO_SHOW)
        res={"close_ids":add_url(random.sample(close_ids,close_id_num)),"far_ids":add_url(random.sample(far_ids,far_id_num))}
        return res
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        return jsonify(message=str(e)), 500

"""
@app.route("/get_network",methods=["POST"])
def get_network():
    try:
        points=get_points()
        plot_network(points)
        return send_file(network.png)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        return {}
"""
