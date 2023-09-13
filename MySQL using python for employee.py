import mysql.connector

class Employee:
    def __init__(self, host, user, password, database_name, table_name):
        self.my_db = mysql.connector.connect(host=host, user=user, password=password)  
        self.cur = self.my_db.cursor()              
        self.database_name = database_name          
        self.table_name = table_name              

    def create_database(self):
        self.cur.execute("CREATE DATABASE {}".format(self.database_name))
        self.my_db.commit()

    def create_table(self, column_names):
        column_definitions = ', '.join('{} VARCHAR(255)'.format(col) for col in column_names)  
        create_table_query = "CREATE TABLE {} ({})".format(self.table_name, column_definitions)
        self.cur.execute("USE {}".format(self.database_name))
        self.cur.execute(create_table_query)
        self.my_db.commit()

    def check_duplicate(self, id):
        query = "SELECT COUNT(*) FROM {} WHERE id = %s".format(self.table_name)
        value = (id,)
        self.cur.execute("USE {}".format(self.database_name))
        self.cur.execute(query, value)
        count = self.cur.fetchone()[0]
        return count > 0

    def insert_employee(self, **kwargs):
        if self.check_duplicate(kwargs.get('id')):
            print("Employee with ID {} already exists.".format(kwargs.get('id')))
            return

        column_names = ', '.join(kwargs.keys())
        placeholders = ', '.join('%s' for _ in kwargs.values())
        query = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, column_names, placeholders)
        values = tuple(kwargs.values())
        self.cur.execute("USE {}".format(self.database_name))
        self.cur.execute(query, values)
        self.my_db.commit()
        print("Employee added successfully.")

    def delete_employee(self,id):
        if self.check_duplicate(id):
            query = "DELETE FROM {} WHERE id = %s".format(self.table_name)
            values = (id,)
            self.cur.execute("USE {}".format(self.database_name))
            self.cur.execute(query, values)
            self.my_db.commit()
        else:
            print("Employee with ID {} not exists.".format(id)) 

    def promote_employee(self, id, new_post, salary_increase_percentage):
        query = "UPDATE {} SET post = %s, salary = salary + salary * %s / 100 WHERE id = %s".format(self.table_name) 
        values = (new_post, salary_increase_percentage, id)
        self.cur.execute("USE {}".format(self.database_name))
        self.cur.execute(query, values)
        self.my_db.commit()

    def close_connection(self):
        self.cur.close()
        self.my_db.close()
        
database_name = "database_name"
table_name = "table_name"
e1 = Employee("host", "user", "password", database_name, table_name)


e1.create_database()

e1.create_table(("id", "name", "post", "salary"))
e1.insert_employee(id=1, name="name", post="post", salary=salary)
e1.insert_employee(id=2, name="name", post="post", salary=salary)
e1.insert_employee(id=3, name="name", post="post", salary=salary)

e1.delete_employee(1)          # For deleting employee using Id
e1.promote_employee(2, "New_Post", salary incremenmt percentage)   # For Promoting employee using Id, New_Post, Percentage increase in salary.

s = "SELECT * FROM {}".format(table_name)   # To fetch all Employees
e1.cur.execute(s)
result = e1.cur.fetchall()

for rec in result:
    print(rec)

e1.close_connection()
