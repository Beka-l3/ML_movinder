from flask import Flask, request
from recommend import KNNModel
import json

app = Flask(__name__)
model = KNNModel()

@app.route("/get_recommendation", methods=['GET'])
def recommend():
    ids = json.loads(request.args.get("recommend_on"))
    exceptions = json.loads(request.args.get("movie_exceptions"))
    
    recommendations = []
    if len(ids) > 0:
        recommendations = model.recommend_on_ids(ids[0], exceptions)
    else:
        recommendations = model.recommend_top(exceptions)

    return json.dumps(recommendations)

if __name__ == "__main__":
    app.run('0.0.0.0', port = 5000, debug = False)