import pytest
import os
from io import BytesIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from models import Photo

def test_index(client, db):
    # Add test data
    photo = Photo(title="Test", filename="test.jpg")
    db.session.add(photo)
    db.session.commit()
    
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test" in response.data

def test_photo_upload(client, app):
    data = {
        'title': 'New Photo',
        'file': (BytesIO(b"fake image data"), 'test.jpg')
    }
    
    # Verify upload folder exists
    upload_dir = app.config['UPLOAD_FOLDER']
    assert os.path.exists(upload_dir)
    
    response = client.post(
        '/upload',
        data=data,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 302  # Redirect after success
    assert Photo.query.count() == 1
    
    # Verify file was saved in the temp directory
    assert os.path.exists(os.path.join(upload_dir, 'test.jpg'))

def test_photo_detail(client, db):
    photo = Photo(title="Detail Test", filename="detail.jpg")
    db.session.add(photo)
    db.session.commit()
    
    response = client.get(f'/photo/{photo.id}')
    assert response.status_code == 200
    assert b"Detail Test" in response.data

def test_photo_delete(client, db, app):
    # Setup
    upload_dir = app.config['UPLOAD_FOLDER']
    test_file = os.path.join(upload_dir, 'delete_test.jpg')
    
    # Create test file
    with open(test_file, 'wb') as f:
        f.write(b"dummy content")
    
    # Create DB record
    photo = Photo(title="Delete Test", filename="delete_test.jpg")
    db.session.add(photo)
    db.session.commit()
    
    # Test deletion
    response = client.post(f'/photo/{photo.id}/delete')
    
    # Verify
    assert response.status_code == 302
    assert Photo.query.count() == 0
    assert not os.path.exists(test_file)