from flask import Flask, request, render_template, jsonify
import json
import traceback
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from model import Model
from scraper import Social, Scraper
#from plot.py import plot_network

app = Flask(__name__)
model=Model()

def update_model():
    global model
    model=Model()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_model, trigger="interval", minutes=1)
scheduler.start()


@app.route('/',methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/process",methods=["POST"])
def process():
    try:
        print("Hello")
        social=request.form['social']
        consent=request.form['consent']=='true'
        id=request.form['ID']
        scraper = Scraper()
        posts=scraper.get_user_text(Social.REDDIT,id) if (social=="reddit") else scraper.get_user_text(Social.TWITTER,id)
        IDs={}
        IDs[social]=id
        close_ids,far_ids=model.process_user(IDs,posts,consent)


        res={"close_ids":close_ids,"far_ids":far_ids}
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
