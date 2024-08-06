import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')

# Создайте папку, если она не существует
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(instance_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False






