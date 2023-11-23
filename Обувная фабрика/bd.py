import sqlite3 as q
class bd:
    __path = str
    __list_attr = {}

    def __init__(self,path:str):
        self.__path = path

    def create_table(self,table_name: str, attr_list: dict):
        with q.connect(self.__path) as db:
            attr = ''
            for i in attr_list:
                if i != list(attr_list)[-1]:
                    attr +=f'{i} {attr_list[i]},\n'
                else: attr+=f'{i} {attr_list[i]}'
            db.cursor().execute("""
                CREATE TABLE IF NOT EXISTS {} (
                    {}
                );
            """.format(table_name,attr))
            self.__list_attr[table_name] = attr_list
    def read_table(self,table_name) -> list:
        with q.connect(self.__path) as db:
            c = db.cursor()
            c.execute("""
                SELECT * FROM {};
            """.format(table_name))    
            data = c.fetchall()
            result = []
            for i in data:
                tmp = {}
                for j in range(len(self.__list_attr[table_name])):
                    tmp[list(self.__list_attr[table_name])[j]]  = list(i)[j]
                result.append(tmp)
            return result
        
    def insert(self,table_name:str,attr_dict:dict):
        with q.connect(self.__path) as db:
            in_attr = ''
            attr = ''
            for i in attr_dict:
                if i != list(attr_dict)[-1]:
                    in_attr+=f'{i},'
                else: in_attr+=f'{i}'
            for i in range(len(attr_dict)):
                if i != len(attr_dict)-1:
                    if self.__list_attr[table_name][list(self.__list_attr[table_name])[i+1]] == 'text':
                        attr+=f'"{attr_dict[list(attr_dict)[i]]}",'
                    else: attr+=f'{attr_dict[list(attr_dict)[i]]},'
                else:
                    if self.__list_attr[table_name][list(self.__list_attr[table_name])[i+1]] == 'text':
                        attr+=f'"{attr_dict[list(attr_dict)[i]]}"'
                    else: attr+=f'{attr_dict[list(attr_dict)[i]]}'
            db.cursor().execute("""
                INSERT INTO {} ({}) VALUES ({})
            """.format(table_name,in_attr,attr))    
    def delete(self,table_name:str,id:int):
        with q.connect(self.__path) as db:
            db.cursor().execute("""
                DELETE FROM {} WHERE id = {}
            """.format(table_name,id))   

    def update(self,table_name:str,id:int,update_attr):
        with q.connect(self.__path) as db:
            db.cursor().execute("""
                UPDATE {}
                SET {} = "{}"
                WHERE id = {}
            """.format(table_name,list(update_attr)[0],update_attr[list(update_attr)[0]],id))   
