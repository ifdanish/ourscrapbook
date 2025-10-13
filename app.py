from flask import Flask, render_template
from models import db, Memory
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
app.config['MONGODB_SETTINGS'] = {
    'db': 'scrapbook',
    'host': 'localhost',
    'port': 27017
}
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

@app.route('/')
def home():
    memories = Memory.objects.order_by('-event_date')
    return render_template('home.html', memories=memories)
