from app import createApp
from flask_cors import CORS

app = createApp()


if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)
