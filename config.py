"""
Global Configuration for Application
"""
import os
import json

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
	vcap = json.loads(os.environ['VCAP_SERVICES'])
	DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

# Get configuration from environment
DATABASE_URI = os.getenv(
	"DATABASE_URI",
	"postgres://postgres:postgres@localhost:5432/postgres"
)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")

FLASK_APP = "service:app" 

FLASK_APP = os.getenv(
	"FLASK_APP", "service:app"
)
