import unittest
import json
from App import app, db, User, Transaction

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'balance': 100.0
        }
        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_user(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'balance': 100.0
        }
        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        user_id = json.loads(response.data)['id']
        update_data = {
            'username': 'updated',
            'email': 'updated@test.com',
            'password': 'updated',
            'balance': 200.0
        }
        response = self.app.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'balance': 100.0
        }
        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        user_id = json.loads(response.data)['id']
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

class TestTransactionAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_get_transactions(self):
        response = self.app.get('/transactions')
        self.assertEqual(response.status_code, 200)

    def test_post_transaction(self):
        user_data = {
            'username': 'buyer',
            'email': 'buyer@test.com',
            'password': 'test',
            'balance': 200.0
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        buyer_id = json.loads(response.data)['id']

        user_data = {
            'username': 'seller',
            'email': 'seller@test.com',
            'password': 'test',
            'balance': 0.0
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        seller_id = json.loads(response.data)['id']

        transaction_data = {
            'user_id': buyer_id,
            'seller_id': seller_id,
            'item_name': 'item',
            'item_price': 100.0,
            'transaction_type': 'purchase'
        }
        response = self.app.post('/transactions', data=json.dumps(transaction_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_transaction(self):
        user_data = {
            'username': 'buyer',
            'email': 'buyer@test.com',
            'password': 'test',
            'balance': 200.0
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        buyer_id = json.loads(response.data)['id']

        user_data = {
            'username': 'seller',
            'email': 'seller@test.com',
            'password': 'test',
            'balance': 0.0
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        seller_id = json.loads(response.data)['id']

        transaction_data = {
            'user_id': buyer_id,
            'seller_id': seller_id,
            'item_name': 'item',
            'item_price': 100.0,
            'transaction_type': 'purchase'
        }
        response = self.app.post('/transactions', data=json.dumps(transaction_data), content_type='application/json')
        transaction_id = json.loads(response.data)['id']

        response = self.app.delete(f'/transactions/{transaction_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    with open("unit tests.txt", 'w') as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
