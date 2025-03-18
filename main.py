# app.py
from flask import Flask
from flask_cors import CORS
from db import db
from api import api_bp
from urllib.parse import quote_plus

app = Flask(__name__)

# Configure CORS
CORS(
    app,
    origins=[
        "https://projectitc620.vercel.app",
        "https://kzml8u6k78vedta1r0p0.lite.vusercontent.net",
        "https://kzmp10ggke8jnyfvk8qt.lite.vusercontent.net",
        "https://kzmnhxayiyd7lk1olbgl.lite.vusercontent.net/admin"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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