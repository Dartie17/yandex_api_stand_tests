import sender_stand_request
import data

def get_user_body(first_name): # копирует тело запроса из файла "data", меняет в нем имя и возвращает тело с измененным именем
    current_body = data.user_body.copy() # в переменную передается копия тела запроса из файла "data"
    current_body["firstName"] = first_name # в теле запроса в переменной заменяется имя пользователя
    return current_body # возвращает тело с измененным именем

def positive_assert(first_name):
    user_body = get_user_body(first_name) # В переменную user_body сохраняется обновлённое тело запроса
    user_response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя
    assert user_response.status_code == 201 # Проверяется, что код ответа равен 201
    assert user_response.json()["authToken"] != "" # Проверяется, что в ответе есть поле authToken и оно не пустое
    users_table_response = sender_stand_request.get_users_table() # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"] # Строка, которая должна быть в ответе
    assert users_table_response.text.count(str_user) == 1 # Проверка, что такой пользователь есть и он единственный

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name) # В переменную user_body сохраняется обновлённое тело запроса
    response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя
    assert response.status_code == 400 # Проверяется, что код ответа равен 400
    assert response.json()["code"] == 400 # Проверяется, что атрибут "code" в теле ответа равен "400"
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя
    assert response.status_code == 400 # Проверяется, что код ответа равен 400
    assert response.json()["code"] == 400 # Проверяется, что атрибут "code" в теле ответа равен "400"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Аа")

# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Тест 3. Ошибка
# Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")

# Тест 4. Ошибка
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааa")

# Тест 5. Успешное создание пользователя
# Параметр fisrtName состоит из английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Успешное создание пользователя
# Параметр fisrtName состоит из русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Ошибка
# Параметр fisrtName состоит из слов с пробелами
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

# Тест 8. Ошибка
# Параметр fisrtName состоит из строки спецсимволов
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9. Ошибка
# Параметр fisrtName состоит из строки с цифрами
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

# Тест 12. Ошибка
# Тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12) # В переменную user_body сохраняется обновлённое тело запроса
    response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя
    assert response.status_code == 400  # Проверяется, что код ответа равен 400