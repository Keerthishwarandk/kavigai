from flask import Flask
def createApp():
    app = Flask(__name__)
    from  .routes.routes import web_link_bp
    app.register_blueprint(web_link_bp)
    return app