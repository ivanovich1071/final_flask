from app import create_app, db
from app.models import User, Order, OrderItem

app = create_app()

# Оболочка для Flask shell, чтобы можно было легко работать с базой данных из командной строки
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Order': Order, 'OrderItem': OrderItem}

if __name__ == '__main__':
    app.run(debug=True)



