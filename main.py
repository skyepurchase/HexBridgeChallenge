from flask import Flask, request
import json
from model.py import process_user

app = Flask(__name__)


@app.route("/process",methods=["POST"])
def process():
    IDs =  request.form['IDs']
    add_to_model=request.form['add_to_model']
    posts=[]
    for social, id in IDs.items():
        curr_weight,curr_text=get_user_text(social,id)
        posts.append((curr_weight,curr_text))
    close_ids,far_ids=process_user(IDs,posts,add_to_model)
    res={"close_ids":close_ids,"far_ids":far_ids}
    return json.dumps(res)
