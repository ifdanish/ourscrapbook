from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Memory
from werkzeug.utils import secure_filename
from forms import MemoryForm
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
app.config['MONGODB_SETTINGS'] = {
    'db': 'scrapbook',
    'host': 'localhost',
    'port': 27017
}
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

@app.route('/add', methods=['GET', 'POST'])
def add_memory():
    form = MemoryForm()
    if form.validate_on_submit():
        # --- Handle the file upload ---
        file = form.photo.data
        # Use secure_filename to prevent malicious filenames
        filename = secure_filename(file.filename)
        # Construct the full save path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- Create a new Memory object and save to database ---
        new_memory = Memory(
            title=form.title.data,
            story=form.story.data,
            event_date=form.event_date.data,
            image_filename=filename # Save only the filename
        )
        new_memory.save()
        
        flash('New memory added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_memory.html', form=form)

@app.route('/')
def home():
    memories = Memory.objects.order_by('-event_date')
    return render_template('home.html', memories=memories)
