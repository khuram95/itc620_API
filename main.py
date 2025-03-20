# app.py
from flask import Flask
from flask_cors import CORS
from db import db
from api import api_bp
from urllib.parse import quote_plus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'murdoch_ict_620_group_1'

# Configure CORS
from flask_cors import CORS

CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "https://projectitc620.vercel.app",
                "https://kzml8u6k78vedta1r0p0.lite.vusercontent.net",
                "https://kzmp10ggke8jnyfvk8qt.lite.vusercontent.net",
                # Usually, an “origin” does not include a path like /admin.
                # If you truly need that, note that browsers normally send
                # only scheme + domain + port as the Origin header.
                "https://kzmnhxayiyd7lk1olbgl.lite.vusercontent.net"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": "*"
        }
    }
)


# Configure MySQL database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://new_db:@lbc#47Sjui2@localhost/drug_checker'

password = '@lbc#47Sjui2'
encoded_password = quote_plus(password)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://drug_admin:{encoded_password}@109.199.100.122/drug_checker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)