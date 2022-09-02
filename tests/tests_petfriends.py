from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Owl', animal_type='Robot',
                                     age='10000', pet_photo='images/png222.png'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='2'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#ниже дополнительные 10 тестов по заданию

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    ''''Проверяем что при вводе неправльных логина и пароля API ключ не получить'''

    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_pets_with_invalid_filter(filter='123'):
    ''''Проверяем что нельзя получить список питомцев с неправильным фильтром'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500

def test_add_photo_of_pet_pngformat_invalid(pet_photo='images/png222.png'):

    """Проверяем что при попытке обновления фотографии не происходит ошибка"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем список питомцев, если он не пустой меняем фото первого питомца на фото загруженное через тест
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и что фото обновилось
        assert status == 200
        assert pet_photo in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_all_pet_info_with_wrong_key():

    """Проверяем невозможность получения информации о питомцах если указан неверный ключ"""

    # передаем неправильный ключ и пытаемся получить список питомцев
    _, auth_key = (200, {'key': 'a4134079016cdc14ede99b06bf521cc403c1bba99cc86efc7c88b243'})
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа = 403
    assert status == 403

def test_add_new_pet_simple_with_invalid_key(name='Альфа', animal_type='Кошка',
                                     age='21'):

    """Проверяем что нельзя добавить питомца с неправильным API Key"""

    # запиcываем неправильный ключ в переменную
    _, auth_key = (200, {'key': 'a4134079016cdc14ede99b06bf521cc403c1bba99cc86efc7c88b243'})

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_response_from_create_pet_simple(name='Альфа', animal_type='Кошка',
                                     age='21'):

    """Проверяем что ответ сервера соответствует документации API"""
    #создаем пример ответа из документации
    example = {
               "age": int,
               "animal_type": str,
               "created_at": str,
               "id": str,
               "name": str,
               "pet_photo": str,
               "user_id": str
}
    #запрашиваем ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    #сравниваем пример ответа из документации с ответом сервера
    assert result.keys() == example.keys()

def test_response_body_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает ответ согласно документации"""
    # создаем пример ответа из документации
    example = {
                "key": str
              }
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные c примером
    assert result.keys() == example.keys()

def test_response_from_api_get_all_pets(filter='my_pets'):
    """ Проверяем что запрос get the list of pets возвращает ответ согласно документации"""
    #создаем пример ответа из документации
    example = {
        "age": int,
        "animal_type": str,
        "created_at": str,
        "id": str,
        "name": str,
        "pet_photo": str,
        "user_id": str
    }


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    #сравниваем пример из документации с ответом сервера
    assert result['pets'][0].keys() == example.keys()

def test_add_photo_of_pet(pet_photo='images/cat1.jpg'):

    """Проверяем что можно добавить фото питомца с корректными данными,
       для того что бы тест работал правильно в него нужно каждый раз передавть новое фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Сохраняем фото до обновления
    r = my_pets['pets'][0]['pet_photo']
    # Проверяем список питомцев, если он не пустой меняем фото первого питомца на фото загруженное через тест
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и что фото обновилось
        assert status == 200
        assert r != result['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_simple_with_valid_data(name='Черемушка', animal_type='Кошка',
                                     age='2'):

    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

