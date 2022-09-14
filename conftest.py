import pytest, time, requests, json
from api import PetFriends

pf = PetFriends()

@pytest.fixture(scope='class')
def email():
    email = 'valid_email'
    return email


@pytest.fixture(scope='class')
def password():
    password = 'valid_password'
    return password


@pytest.fixture(scope='class')
def get_key():
    headers = {'email': 'valid_password',
               'password': 'valid_email'
               }

    response = requests.get('https://petfriends.skillfactory.ru/api/key', headers=headers)
    assert response.status_code == 200
    assert 'key' in response.json()
    return response.json()

@pytest.fixture(autouse=True)
def time_delta():
    start_time = time.time()
    yield
    end_time = time.time()
    print (f"\nТест шел: {end_time - start_time}")

@pytest.fixture(autouse=True)
def request_fixture(request):
    if 'pet' or 'pets' in request.function.__name__:
        print(f'\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}')

@pytest.fixture(autouse=True)
def request_fixture(request):
    if 'invalid' or 'wrong' in request.function.__name__:
        print(f'\nЗапущен негативный тест: {request.function.__name__}')