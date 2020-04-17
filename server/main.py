from flask import Flask, render_template, request, Response
from flask_cors import CORS
import json
import os
import pickle
from datetime import datetime
from pytz import timezone
from flask_socketio import SocketIO, emit

import predict_passes as predict
from robot import Robot
from utils import is_mount_available

app = Flask("__main__")
# CORS(app)

socketio = SocketIO(app)


ROOT_DIR = os.environ['ROOT_DIR']
IMAGE_DIR = os.environ['IMAGE_OUTPUT_DIR']
DATA_DIR = os.path.join(ROOT_DIR, 'data')

robot = Robot()  # Singleton for the system


def get_timestamp(tt):
    return tt.strftime("%X %Z %x")

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
    passes = predict.predict_passes(lat, lon, cache=False)
    return Response(format_passes_as_json(passes), mimetype='application/json')


@app.route('/image_list')
def get_observation_file_list():
    static_dir = 'static'

    images = [{'file_name': 'static/observations/space.jpg'}]
    for path, dirs, files in os.walk(IMAGE_DIR):
        hosted_path = path[path.index(static_dir):]
        images += [{'file_name': os.path.join(hosted_path, f)} for f in files]

    return Response(json.dumps(images), mimetype='application/json')

@socketio.on('get_system_status')
def get_status():
    print('received a status request')
    emit('system_status', json.dumps({'mount_connected': is_mount_available()}))

@socketio.on('connect')
def on_connect():
    print("received connection")

@socketio.on('JOG_MOUNT')
def jog(jog_data):
    ax = int(jog_data['axis'])
    val = int(jog_data['value'])
    print("Jogging: axis={}, distance={}".format(ax, val))
    if ax == 0:
        ret = robot.tracker.move_relative(ra=val, dec=0)
    if ax == 1:
        ret = robot.tracker.move_relative(ra=0, dec=val)
    robot.tracker.wait_for_move()
    emit('done_jogging')


@socketio.on('run')
def run():
    robot.calibrate(0, 0)  # FIX THIS
    session_id = robot.start_session()
    if session_id > 0:
        return "Session starting", 200
    else:
        return "Failed to start session - maybe one is already running", 500


#@app.route('/stop_run')
def stop_run():
    print("received!")
    robot.stop_session()
    return "Session stopped", 200


@app.route('/upcoming_passes')
def get_upcoming_passes():
    '''pass data structured in the following tuple:
        (SAT_NAME, time, (el, az, rng))
    '''
    return Response(
        format_passes_as_json(robot.session.passes),
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
    socketio.run(app, host='0.0.0.0', port=80)
