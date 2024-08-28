from gw.common import database
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
from flask import Flask, Response, render_template, stream_with_context, jsonify

# Starts up a new Flask Instance
application = Flask(__name__)
# Connects to MongoDB
client = database.connect()
# Database
database.select("metric_db")
db = database.__db
# Collection
metrics = db.metrics_collection

def SortByDate(e):
    return e['timestamp']


@application.route('/')
def index():
    data = metrics.find()
    results = []
    for item in data:
        item['_id'] = str(item['_id'])
        acquired_time = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M')
        time_now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        if acquired_time < time_now - timedelta(minutes=8):
            continue
        else:
            results.append(item)
    # Sort the list by the timestamp to ensure we are putting stuff on the graph in the correct direction
    results.sort(key=SortByDate)
    return render_template('index.html', things = results)

@application.route('/api/datapoint')
def api_datapoint():
    metrics = db.metrics_collection
    data = metrics.find()
    results = []
    for item in data:
        item['_id'] = str(item['_id'])
        acquired_time = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M')
        time_now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        if acquired_time < time_now - timedelta(minutes=8):
            continue
        else:
            results.append(item)
    # Sort the list by the timestamp to ensure we are putting stuff on the graph in the correct direction
    results.sort(key=SortByDate)
    return jsonify({'results':results})
    #return Response(json.dumps(results),mimetype='application/json')

def main():
    application.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()