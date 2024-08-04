from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Установите страницу входа для LoginManager
    login_manager.login_view = 'main.login'  # Название в формате "blueprint_name.view_name"
    login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."

    # Регистрация маршрутов через Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Загрузчик пользователя
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

