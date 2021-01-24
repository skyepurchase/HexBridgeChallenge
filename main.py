from flask import Flask, request, render_template
import json
from model import Model
from scraper import Social, Scraper

app = Flask(__name__)



@app.route('/',methods=["GET"])
def root():
    print("Call to root")
    return render_template('index.html')


@app.route("/process",methods=["POST"])
def process():
    social=request.form['social']
    consent=request.form['consent']
    id=request.form['ID']
    scraper = Scraper()
    curr_weight,curr_text=scraper.get_user_text(Social.REDDIT,id) if (social=="reddit") else scraper.get_user_text(Social.TWITTER,id)
    model=Model()
    IDs={}
    IDs[social]=id
    posts=[(curr_weight,curr_text)]
    close_ids,far_ids=model.process_user(IDs,posts,consent)
    res={"close_ids":close_ids,"far_ids":far_ids}
    return json.dumps(res)
