from flask import Flask

def create_app():
    # Serve static files (like audio) from the "static" folder
    app = Flask(__name__, static_folder='static', template_folder='templates')

    from app.routes import bp
    app.register_blueprint(bp)

    return app
