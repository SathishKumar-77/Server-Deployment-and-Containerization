# # '''
# # Tests for jwt flask app.
# # '''
# # import os
# # import json
# # import pytest

# # import main

# # SECRET = 'TestSecret'
# # TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
# # EMAIL = 'wolf@thedoor.com'
# # PASSWORD = 'huff-puff'

# # @pytest.fixture
# # def client():
# #     os.environ['JWT_SECRET'] = SECRET
# #     main.APP.config['TESTING'] = True
# #     client = main.APP.test_client()

# #     yield client



# # def test_health(client):
# #     response = client.get('/')
# #     assert response.status_code == 200
# #     assert response.json == 'Healthy'


# # def test_auth(client):
# #     body = {'email': EMAIL,
# #             'password': PASSWORD}
# #     response = client.post('/auth', 
# #                            data=json.dumps(body),
# #                            content_type='application/json')

# #     assert response.status_code == 200
# #     token = response.json['token']
# #     assert token is not None



# '''
# Tests for jwt flask app.
# '''
# import os
# import json
# import jwt
# import pytest

# import main

# SECRET = 'TestSecret'
# TOKEN = jwt.encode(
#     {
#         'exp': 1671306790,
#         'nbf': 1560097190,
#         'email': 'wolf@thedoor.com'
#     },
#     SECRET,
#     algorithm='HS256'
# )
# EMAIL = 'wolf@thedoor.com'
# PASSWORD = 'huff-puff'

# @pytest.fixture
# def client():
#     os.environ['JWT_SECRET'] = SECRET
#     main.APP.config['TESTING'] = True
#     client = main.APP.test_client()

#     yield client


# def test_health(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert response.json == 'Healthy'


# def test_auth(client):
#     body = {'email': EMAIL, 'password': PASSWORD}
#     response = client.post('/auth', 
#                            data=json.dumps(body),
#                            content_type='application/json')
#     assert response.status_code == 200
#     token = response.json['token']
#     assert token is not None

#     # Decode the token and verify its contents
#     decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
#     assert decoded_token['email'] == EMAIL


# def test_auth_missing_email(client):
#     body = {'password': PASSWORD}
#     response = client.post('/auth', 
#                            data=json.dumps(body),
#                            content_type='application/json')
#     assert response.status_code == 400
#     assert response.json['message'] == 'Missing parameter: email'


# def test_auth_missing_password(client):
#     body = {'email': EMAIL}
#     response = client.post('/auth', 
#                            data=json.dumps(body),
#                            content_type='application/json')
#     assert response.status_code == 400
#     assert response.json['message'] == 'Missing parameter: password'


# def test_contents(client):
#     headers = {'Authorization': f'Bearer {TOKEN}'}
#     response = client.get('/contents', headers=headers)
#     assert response.status_code == 200
#     data = response.json
#     assert data['email'] == EMAIL


# def test_contents_no_token(client):
#     response = client.get('/contents')
#     assert response.status_code == 401


# def test_contents_invalid_token(client):
#     headers = {'Authorization': 'Bearer invalid_token'}
#     response = client.get('/contents', headers=headers)
#     assert response.status_code == 401


import os
import json
import jwt
import datetime
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET = os.getenv('JWT_SECRET', 'TestSecret')  # Ensure this matches the .env file setting
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

TOKEN = jwt.encode(
    {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=2),
        'nbf': datetime.datetime.utcnow(),
        'email': EMAIL
    },
    SECRET,
    algorithm='HS256'
).decode('utf-8')  # Decode to string

print("Generated Token:", TOKEN)


import main

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()
    yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL, 'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')
    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

    # Decode the token and verify its contents
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    assert decoded_token['email'] == EMAIL


def test_auth_missing_email(client):
    body = {'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'Missing parameter: email'


def test_auth_missing_password(client):
    body = {'email': EMAIL}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'Missing parameter: password'


def test_contents(client):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = client.get('/contents', headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data['email'] == EMAIL


def test_contents_no_token(client):
    response = client.get('/contents')
    assert response.status_code == 401


def test_contents_invalid_token(client):
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get('/contents', headers=headers)
    assert response.status_code == 401


