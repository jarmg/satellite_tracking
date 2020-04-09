from flask import Flask, render_template, request, Response
from flask_cors import CORS
import json
import os
import pickle
from datetime import datetime
from pytz import timezone
import predict_passes as predict
from run import Runner 
 

app = Flask("__main__")
CORS(app)

ROOT_DIR = os.environ['ROOT_DIR']
IMAGE_DIR = os.environ['IMAGE_OUTPUT_DIR']
DATA_DIR = os.path.join(ROOT_DIR, 'data')                                  

session = Runner(mock=True)


def get_timestamp(tt):
    tz_pst = timezone('US/Pacific')
    return tt.utc_datetime().astimezone(tz_pst).strftime("%X %Z %x")


def format_passes_as_json(passes):
    pass_data = [{
            'satellite': sat,
            'time': get_timestamp(ts),
            'elevation': "{:.2f} deg".format(elev.degrees),
            'azimuth': "{:.2f} deg".format(az.degrees),
            'range': "{:.2f} km".format(rng.km)
        } for sat, ts, (elev, az, rng) in passes]
    return json.dumps(pass_data)


@app.route('/')
def serve_main():
    return render_template('index.html', flask_token="hello!")


@app.route('/generate_passes')
def generate_pass_predictions():
    # TODO jarmg: take parameters
    lat = '47.647654'
    lon = '-122.324748'
    passes = predict.predict_passes(lat, lon)
    return Response(format_passes_as_json(passes), mimetype='application/json')


@app.route('/image_list')
def get_observation_file_list():
    static_dir = 'static'

    images = [{'file_name': 'static/observations/space.jpg'}]
    for path, dirs, files in os.walk(IMAGE_DIR):
        hosted_path = path[path.index(static_dir):]
        images += [{'file_name': os.path.join(hosted_path, f)} for f in files]

    return Response(json.dumps(images), mimetype='application/json')


@app.route('/status')
def show_status():
    pass

@app.route('/jog')
def jog():
    az = int(request.args.get('azimuth'))
    el = int(request.args.get('elevation'))
    print("Jogging: az={}, el={}".format(az, el))
    return session.sat_tracker.move_relative(ra=az, dec=el)


@app.route('/upcoming_passes')
def get_upcoming_passes():
    '''pass data structured in the following tuple:
        (SAT_NAME, time, (el, az, rng))
    '''
    now_utc = datetime.now(timezone('UTC'))

    def is_upcoming(p):
        return p[1].utc_datetime() > now_utc

    passes = pickle.load(open(os.path.join(DATA_DIR, 'passes.pkl'), 'rb'))
    upcoming_passes = filter(is_upcoming, passes)
    return Response(
            format_passes_as_json(upcoming_passes),
            mimetype='application/json')


@app.route('/tle', methods=['GET', 'POST'])
def upload_tle():
    if request.method == 'POST':
        file = request.files['file'] 
        file.save('/data/tle_data.txt')
    if request.method == 'GET':
        tles = open('/data/tle_data.txt')
        return(tles.read())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
