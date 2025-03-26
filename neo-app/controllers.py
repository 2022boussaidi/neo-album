from flask import render_template, request, redirect, url_for, send_from_directory
from services import (
    get_all_photos,
    handle_photo_upload,
    get_photo_detail,
    delete_photo_file
)
from config import Config
from schemas import schema


def init_routes(app):
    @app.route('/')
    def index():
        photos = get_all_photos()
        return render_template('index.html', photos=photos)
    
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            return handle_photo_upload(request)
        return render_template('upload.html')
    
    @app.route('/photo/<int:photo_id>')
    def photo_detail(photo_id):
        photo = get_photo_detail(photo_id)
        return render_template('detail.html', photo=photo)
    
    @app.route('/photo/<int:photo_id>/delete', methods=['POST'])
    def delete_photo(photo_id):
        delete_photo_file(photo_id)
        return redirect(url_for('index'))
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    
    