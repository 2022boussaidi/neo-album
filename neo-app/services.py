from models import db, Photo
from utils import allowed_file
import os
from werkzeug.utils import secure_filename
from config import Config
from flask import redirect, url_for

#get photos service 
def get_all_photos():
    return Photo.query.order_by(Photo.uploaded_at.desc()).all()

# handle photo upload serivce 
def handle_photo_upload(request):
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    title = request.form.get('title', 'Untitled')
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Use current_app to get the config
        from flask import current_app
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file.save(os.path.join(upload_folder, filename))
        
        photo = Photo(title=title, filename=filename)
        db.session.add(photo)
        db.session.commit()
        
        return redirect(url_for('index'))
    return redirect(request.url)

#detail photo service
def get_photo_detail(photo_id):
    return Photo.query.get_or_404(photo_id)
#delete service 
def delete_photo_file(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    from flask import current_app
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(photo)
    db.session.commit()