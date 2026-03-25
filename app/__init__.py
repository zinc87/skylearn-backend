from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import lessons, quizzes, code, progress, leaderboard
    app.register_blueprint(lessons.bp)
    app.register_blueprint(quizzes.bp)
    app.register_blueprint(code.bp)
    app.register_blueprint(progress.bp)
    app.register_blueprint(leaderboard.bp)

    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    return app


