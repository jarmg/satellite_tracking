from flask import Flask, render_template, request
app = Flask("__main__")


@app.route('/')
def serve_main():
    return render_template('index.html', flask_token="hello!") 


@app.route('/generate_passes')
def generate_pass_preditions():
    pass


@app.route('/images')
def server_images():
    pass


@app.route('/status')
def show_status():
    pass


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
