from flask import Flask
from flask_cors import CORS
from db import db
from api import api_bp
from urllib.parse import quote_plus
from asgiref.wsgi import WsgiToAsgi  # Import the adapter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'murdoch_ict_620_group_1'

# Configure CORS
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
                "https://kzmnhxayiyd7lk1olbgl.lite.vusercontent.net"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": "*"
        }
    }
)

# Configure MySQL database connection
password = '@lbc#47Sjui2'
encoded_password = quote_plus(password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://drug_admin:{encoded_password}@109.199.100.122/drug_checker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and register the API blueprint
db.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')

# Create the database tables
with app.app_context():
    db.create_all()

# Wrap the Flask app using WsgiToAsgi to make it compatible with ASGI servers
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host="127.0.0.1", port=8000, log_level="debug")
