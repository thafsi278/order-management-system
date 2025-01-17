from flask import Flask
from views import views

# Function that initializes flask application
def create_app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix="/")
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=8000)
    return app

if __name__ == '__main__':
    create_app() # Calling function