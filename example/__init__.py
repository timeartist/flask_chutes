from flask import Flask, render_template
from flask_chutes import enable_chutes

app = Flask(__name__)
app.config['REDIS_CONN'] = {'host':'redis-host', 'db':0}
enable_chutes(app)

@app.route('/')
def index():
    return render_template('index.html')