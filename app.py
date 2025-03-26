import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from models import db, Photo
from config import Config
from schemas import schema

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        title = request.form.get('title', 'Untitled')
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            photo = Photo(title=title, filename=filename)
            db.session.add(photo)
            db.session.commit()
            
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/photo/<int:photo_id>')
def photo_detail(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('detail.html', photo=photo)

@app.route('/photo/<int:photo_id>/delete', methods=['POST'])
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    
    # Remove file from filesystem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(photo)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# GraphQL endpoint
from flask_graphql import GraphQLView
app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True
))

if __name__ == '__main__':
    app.run(host='0.0.0.0')