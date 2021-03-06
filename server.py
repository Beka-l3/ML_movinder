"""Flask app for recommendation request handling"""

import json
from flask import Flask, request, abort
from recommend import KNNModel


app = Flask(__name__)
model = KNNModel()


@app.route("/get_recommendation", methods=["GET"])
def recommend():
    """Return recommendation on the list of movies"""
    ids = json.loads(request.args.get("recommend_on"))
    exceptions = json.loads(request.args.get("movie_exceptions"))
    recommendations = []
    if len(ids) > 0:
        recommendations = model.recommend_on_ids(ids[0], exceptions)
    else:
        recommendations = model.recommend_top(exceptions)
    if len(recommendations) == 0:
        abort(404, description="Movie not found")
    return json.dumps(recommendations)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=False)
