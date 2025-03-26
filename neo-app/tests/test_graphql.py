import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from models import Photo

def test_graphql_all_photos(client, db):
    # Add test data
    photo = Photo(title="GraphQL Test", filename="graphql.jpg")
    db.session.add(photo)
    db.session.commit()
    
    query = """
        query {
            allPhotos {
                edges {
                    node {
                        title
                        filename
                    }
                }
            }
        }
    """
    
    response = client.post(
        '/graphql',
        json={'query': query}
    )
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['data']['allPhotos']['edges'][0]['node']['title'] == "GraphQL Test"

def test_graphql_create_photo(client):
    mutation = """
        mutation {
            createPhoto(title: "New GraphQL", filename: "new.jpg") {
                photo {
                    id
                    title
                }
            }
        }
    """
    
    response = client.post(
        '/graphql',
        json={'query': mutation}
    )
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['data']['createPhoto']['photo']['title'] == "New GraphQL"
    assert Photo.query.count() == 1

def test_graphql_delete_photo(client, db):
    photo = Photo(title="To Delete", filename="delete.jpg")
    db.session.add(photo)
    db.session.commit()
    
    mutation = f"""
        mutation {{
            deletePhoto(id: {photo.id}) {{
                success
            }}
        }}
    """
    
    response = client.post(
        '/graphql',
        json={'query': mutation}
    )
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['data']['deletePhoto']['success'] is True
    assert Photo.query.count() == 0