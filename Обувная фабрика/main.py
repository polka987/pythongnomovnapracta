from bd import bd
import pyautogui as gui
from tabulate import tabulate

db = bd
db = bd('bd.db')
db.create_table('users',{'id':'INTEGER PRIMARY KEY','name':'text','login':'text','password':'text','role':'text'})
db.create_table('shoes',{'id':'INTEGER PRIMARY KEY','title':'text','size':'int','material':'text','cena':'text'})
users = db.read_table('users')
tovars = db.read_table('shoes')
zakaz = []
if len(users) == 0:
    db.insert('users',{'name':'user','login':'user','password':'user','role':'user'})
    db.insert('users',{'name':'admin','login':'admin','password':'admin','role':'admin'})
    db.insert('shoes',{'title':'деревянные',"size":40,"material":'камень','cena':"500"})
    db.insert('shoes',{'title':'кирпичные',"size":94,"material":'дерево','cena':"9000"})



def auth(login: str, password: str) -> str:
    for i in users:
        if i['name'] == login and i["password"] == password:
            return i['role']
    return None
def reg(name:str, login:str, password:str) -> str:
    db.insert('users',{'name':name,'login':login,'password':password,'role':'user'})
    return 'user'

def admin():
    result = gui.confirm('Выберите действие', buttons=["Посмотреть все товары", "Посмотреть всех пользователей"])
    match(result):
        case 'Посмотреть все товары':
            CRUD_tovar()
        case 'Посмотреть всех пользователей':
            CRUD_user()
        case _:
            main()

def create_user():
    try:
        db.insert('users',{'name':gui.prompt("Введите имя пользователя: ")
                       ,'login':gui.prompt("Введите логин пользователя: "),'password':gui.prompt("Введите пароль пользователя: "),'role':'user'})
    except: gui.alert('Произошла ошибки')
    global users
    users = db.read_table('users')
    CRUD_user()

def delete_user():
    try:
        db.delete('users',int(gui.prompt("Введите id пользователя, которого хотите удалить: ")))
    except: gui.alert('Произошла ошибки')
    global users
    users = db.read_table('users')
    CRUD_user()
    
def update_user():
    try:
        db.update('users',gui.prompt("Введите id пользователя, которого хотите изменить данные"),{gui.confirm("Выбирите столбец, который хотите изменить", buttons=['name','login','password','role']): gui.prompt("Введите новое значение: ")})
    except: gui.alert('Произошла ошибки')
    global users
    users = db.read_table('users')
    CRUD_user()

def CRUD_user():
    result = gui.confirm(tabulate(users,tablefmt="textile",headers='keys'), buttons=["Добавить пользователя", "Удалить пользователя","Изменить пользователя"])
    if result == None:
        admin()
    elif result == "Добавить пользователя":
        create_user()
    elif result == "Удалить пользователя":
        delete_user()
    elif result == "Изменить пользователя":
        update_user()

def update_tovar():
    pass

def create_tovar():
    try:
        db.insert('shoes',{'title':gui.prompt("Введите название товара: "),'size':gui.prompt("Введите размер товара: "),'material':gui.prompt("Введите материал товара: "),'cena':gui.prompt("Введите цену товара: ")})
    except: gui.alert('Произошла ошибки')
    global tovars
    tovars = db.read_table('shoes')
    CRUD_tovar()

def delete_tovar():
    try:
        db.delete('shoes',int(gui.prompt("Введите id товара, которого хотите удалить: ")))
    except: gui.alert('Произошла ошибки')
    global tovars
    tovars = db.read_table('shoes')
    CRUD_tovar()

        
def CRUD_tovar():
    result = gui.confirm(tabulate(tovars,tablefmt="textile", headers='keys'), buttons=["Добавить товар", "Удалить товар","Изменить товар"])
    if result == None:
        admin()
    elif result == "Добавить товар":
        create_tovar()
    elif result == "Удалить товар":
        delete_tovar()
    elif result == "Изменить товар":
        update_tovar()

def user():
    result = gui.confirm('Выберите действие', buttons=["Сделать заказ", "Посмотреть мои заказы"])
    match(result):
        case 'Сделать заказ':
            result = gui.confirm(tabulate(tovars,tablefmt="textile", headers='keys'), buttons=[i["title"] for i in tovars ])
            for i in tovars:
                if i['title'] == result:
                    zakaz.append(i)
            user()
        case 'Посмотреть мои заказы':
            print(zakaz)
            result = gui.confirm(tabulate(zakaz,tablefmt="textile",headers='keys'))
            user()
        case _:
            main()

def menu(role:str):
    if role == 'admin':
        admin()
    elif role == 'user':
        user()

            
def main():
    result = gui.confirm('Выберите действие', buttons=["Авторизация", "Регистрация"])
    match(result):
        case 'Авторизация':
            role = auth(gui.prompt("Введите логин: "),gui.prompt("Введите пароль: ")) 
            if role != None: menu(role)
            else: main()
        case 'Регистрация':
            role = reg(gui.prompt("Введите Ваше имя: "),gui.prompt("Введите новый логин: "),gui.prompt("Введите новый пароль: "))
            menu(role)

if __name__ == '__main__':
    users = db.read_table('users')
    tovars = db.read_table('shoes')
    main()