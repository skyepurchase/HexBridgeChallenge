from flask import Flask, request, render_template
import json
import traceback
from model import Model
from scraper import Social, Scraper

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
        return json.dumps(res)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        return json.dumps({"close_ids":[],"far_ids":[]})
