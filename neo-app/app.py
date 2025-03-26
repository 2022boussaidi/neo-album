from flask import Flask
from controllers import init_routes
from models import db
from config import Config
from flask_graphql import GraphQLView
from schemas import schema

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Create upload folder if it doesn't exist
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize routes
    init_routes(app)
    
    # Add GraphQL endpoint
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Enable GraphiQL interface
        )
    )
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')