from flask import Flask, request
import json
from model import Model
from scraper import Social, Scraper

app = Flask(__name__)



@app.route('/',methods=["GET"])
def root():
    return app.send_static_file('templates/index.html')


@app.route("/process",methods=["POST"])
def process():
    IDs =  request.form['IDs']
    add_to_model=request.form['add_to_model']
    posts=[]
    for social, id in IDs.items():
        scraper = Scraper()
        curr_weight,curr_text=scraper.get_user_text(Social.REDDIT,id) if (social=="reddit") else scraper.get_user_text(Social.TWITTER,id)
        posts.append((curr_weight,curr_text))
    model=Model()
    close_ids,far_ids=model.process_user(IDs,posts,add_to_model)
    res={"close_ids":close_ids,"far_ids":far_ids}
    return json.dumps(res)
