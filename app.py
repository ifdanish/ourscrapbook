from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from models import db, Memory, User
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from forms import MemoryForm, RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
app.config['MONGODB_SETTINGS'] = {
    'db': 'scrapbook',
    'host': 'localhost',
    'port': 27017
}
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # The route to redirect to for login

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add', methods=['GET', 'POST'])
@login_required 
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
            image_filename=filename, # Save only the filename
            user=current_user
        )
        new_memory.save()
        
        flash('New memory added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_memory.html', form=form)

@app.route('/')
@login_required 
def home():
    #memories = Memory.objects.order_by('-event_date')
    #return render_template('home.html', memories=memories)
    memories = Memory.objects(user=current_user).order_by('-event_date')
    
    return render_template('home.html', memories=memories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        new_user.save()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete/<memory_id>', methods=['POST'])
@login_required
def delete_memory(memory_id):
    # Find the memory to delete
    memory_to_delete = Memory.objects.get_or_404(id=memory_id, user=current_user)
    
    # --- Delete the associated image file ---
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], memory_to_delete.image_filename)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    # --- Delete the memory document from the database ---
    memory_to_delete.delete()
    
    return jsonify({'result': 'success'})

@app.route('/edit/<memory_id>', methods=['GET', 'POST'])
@login_required
def edit_memory(memory_id):
    memory_to_edit = Memory.objects.get_or_404(id=memory_id, user=current_user)
    form = MemoryForm(obj=memory_to_edit)

    if form.validate_on_submit():
        # Update the memory's fields with the new data from the form
        memory_to_edit.title = form.title.data
        memory_to_edit.story = form.story.data
        memory_to_edit.event_date = form.event_date.data
        
        # --- Handle optional new file upload ---
        if form.photo.data:
            # Delete the old image file
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], memory_to_edit.image_filename)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            
            # Save the new image file
            file = form.photo.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Update the filename in the database
            memory_to_edit.image_filename = filename

        memory_to_edit.save()
        flash('Memory updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_memory.html', form=form, memory=memory_to_edit)
