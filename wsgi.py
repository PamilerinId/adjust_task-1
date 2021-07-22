from main import create_app
from config import get_env

app = create_app(get_env('FLASK_ENV'))

if __name__ == '__main__':
     app.run()