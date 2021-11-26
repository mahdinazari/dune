from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
csrf = CSRFProtect()
cors = CORS(resources={r"/api/*": {"origins": "*"}})

