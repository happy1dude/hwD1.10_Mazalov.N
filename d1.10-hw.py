import sys
import json
import requests
from trello import TrelloApi
# Данные авторизации в API Trello  
auth_params = {    
    'key': "тут должен быть ваш key",    
    'token': "тут должен быть ваш token", } 

trelloNew =  TrelloApi(auth_params['key'], auth_params['token'])

# newboard = trelloNew.boards.new('Доска для создания своего приложения')
# print(newboard)
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}" 
board_id = "TOLfDH0N"

def newBoard(name):
    #Создаём новую доску
    newboard = trelloNew.boards.new(name)
    print(newboard['name'] + ', успешно создана!')

def read():
    #Получим данные со всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # print(column_data)
    #Выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        #Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + '. Количество задач: ' + str(len(task_data)))
                                 
        if not task_data:
            print('\t' + 'No have tasks!')
            continue
        for task in task_data:
            print('\t' + task['name'])

def createList(name):
    #Получим данные о нужной доске
    board_data = requests.get(base_url.format('boards') + '/' + board_id, params=auth_params).json()
    
    #Полный id доски, полученный из ответа на board_data
    board_id_long = board_data['id']
    # print(get_id1)
  
    #Создание нового списка
    new_list = requests.post(base_url.format('boards/') + board_id_long + '/lists', data={'name': name, **auth_params})
    # print(new_list.status_code)
    if new_list.status_code == 200:
        print('Список успешно создан!')
    else:
        print('Что-то пошло не так! :(')
    
    


def createNewTask(name, column_name):
    #Получим данные со всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    print(column_data)
    #Переберем данные обо всех колонках, пока не найдем ту колонку, которая нужна
    for column in column_data:
        if column['name'] == column_name:
            #Создадим задачу с именем _name_ в найденой колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    #Получим данные со всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # print(column_data)

    #Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    #Теперь у нас есть id задачи, которую мы хотим переместить
    #Переберем данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            #И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    if sys.argv[1] == 'read':
        read()
    elif sys.argv[1] == 'createList':
        createList(sys.argv[2])
    elif sys.argv[1] == 'createNewTask':
        createNewTask(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'newBoard':
        newBoard(sys.argv[2])
