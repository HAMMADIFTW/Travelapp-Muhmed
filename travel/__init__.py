from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    Bootstrap5(app)

    # savely store passwords
    Bcrypt(app)

    # setting a secret key
    app.secret_key = 'somerandomvalue'

    # configue database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    # upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # returns User by taking userid
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))

    # add blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)
    from . import api
    app.register_blueprint(api.api_bp)
    
    @app.errorhandler(404) 
    # error function
    def not_found(e): 
      return render_template("404.html", error=e)

    # dictionary of variables that are available to all templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    return app