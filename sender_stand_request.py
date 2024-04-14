import configuration
import requests
import data

def get_users_table(): # запрос на получение данных из таблицы "user_model"
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

def post_new_user(body): # запрос на создание нового пользователя, принимает в себя тело запроса
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)