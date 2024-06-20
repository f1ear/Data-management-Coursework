# Основной код

# подключаем модули
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# создаем Flask приложение и получаем объект app
app = Flask(__name__)
# указываем, что приложение работает с БД по этому пути
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# инициализируем БД через SQLAlchemy в Flask
db = SQLAlchemy(app)

# модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    transactions = db.relationship('Transaction', backref='user')

    # функция для преобразования в правильный формат, чтобы можно было в Json отправлять данные
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# модель транзакций
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    # функция для преобразования в правильный формат, чтобы можно было в Json отправлять данные
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# контроллер модели пользователей
class UserController:
    # метод добавления пользователя с данными из POST запроса
    @staticmethod
    def create_user(data):
        new_user = User(username=data['username'], email=data['email'], password=data['password'], balance=data['balance'])
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id}, 201

    # метод обновления пользователя с ID user_id с данными из PUT запроса
    @staticmethod
    def update_user(user_id, data):
        user = User.query.get_or_404(user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.balance = data.get('balance', user.balance)
        db.session.commit()
        return {'message': 'User updated successfully'}

    # метод удаления пользователя с ID user_id по DELETE запросу
    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

    # метод отправки списка всех пользователей по GET запросу 
    @staticmethod
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

# контроллер модели транзакций
class TransactionController:
    # метод добавления транзакции с данными из POST запроса
    @staticmethod
    def create_transaction(data):
        buyer = User.query.get_or_404(data['user_id'])
        seller = User.query.get_or_404(data['seller_id'])
        if buyer.balance < data['item_price']:
            return {'message': 'Insufficient balance'}, 400
        new_transaction = Transaction(user_id=data['user_id'], seller_id=data['seller_id'], item_name=data['item_name'], item_price=data['item_price'], transaction_type=data['transaction_type'])
        buyer.balance -= data['item_price']
        seller.balance += data['item_price']
        db.session.add(new_transaction)
        db.session.commit()
        return {'id': new_transaction.id}, 201

    # метод удаления транзакции с ID transaction_id по DELETE запросу
    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return {'message': 'Transaction deleted successfully'}

    # метод для отправки списка всех транзакций по GET запросу
    @staticmethod
    def get_transactions():
        transactions = Transaction.query.all()
        return jsonify([transaction.to_dict() for transaction in transactions])

# маршрут /users для запросов GET - отправляет список всех пользователей в таблице 
@app.route('/users', methods=['GET'])
def get_users():
    return UserController.get_users()

# маршрут /users для запросов POST - создает нового пользователя 
@app.route('/users', methods=['POST'])
def create_user():
    return UserController.create_user(request.get_json())

# маршрут /users/<int:user_id> для запросов PUT - обновляет данные пользователя с ID user_id 
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return UserController.update_user(user_id, request.get_json())

# маршрут /users/<int:user_id> для запросов DELETE - удаляет пользователя с ID user_id 
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)

# маршрут /transactions для запросов GET - отправляет список всех транзакций в таблице
@app.route('/transactions', methods=['GET'])
def get_transactions():
    return TransactionController.get_transactions()

# маршрут /transactions для запросов POST - создает новую транзакцию 
@app.route('/transactions', methods=['POST'])
def create_transaction():
    return TransactionController.create_transaction(request.get_json())

# маршрут /transactions/<int:transaction_id> для запросов DELETE - удаляет транзакцию с ID transaction_id
@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)

# собственно, main()
if __name__ == '__main__':
    # при запуске Flask приложения - создаем БД (если БД пустая, т. е. только что создана), либо подключаем её
    with app.app_context():
        db.create_all()
    # запускаем Flask приложение
    app.run(debug=True)
