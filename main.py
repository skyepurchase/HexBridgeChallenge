from flask import Flask, request, render_template, jsonify
import json
import traceback
from model import Model
from scraper import Social, Scraper
#from plot.py import plot_network

app = Flask(__name__)



@app.route('/',methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/process",methods=["POST"])
def process():
    try:
        social=request.form['social']
        consent=request.form['consent']
        id=request.form['ID']
        scraper = Scraper()
        posts=scraper.get_user_text(Social.REDDIT,id) if (social=="reddit") else scraper.get_user_text(Social.TWITTER,id)
        model=Model()
        IDs={}
        IDs[social]=id
        close_ids,far_ids=model.process_user(IDs,posts,consent)
        res={"close_ids":close_ids,"far_ids":far_ids}
        print("Returning: " + str(res))
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
