# run.py

from app import app
from app import routes  # Import routes after the app has been created

if __name__ == "__main__":
    app.run(debug=True)
