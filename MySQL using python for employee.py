import mysql.connector

class Employee:
    def __init__(self, host, user, password, database_name, table_name):
        self.my_db = mysql.connector.connect(host=host, user=user, password=password)  # use to setup conncetion btwn sql and python
        self.cur = self.my_db.cursor()               # intilizing cursor inorder to work in python
        self.database_name = database_name          # adding database name as class attribute so that can be used by any method of the given class
        self.table_name = table_name               # adding table name as class attribute so that can be used by any method of the given class

    def create_database(self):
        self.cur.execute("CREATE DATABASE {}".format(self.database_name))
        self.my_db.commit()

    def create_table(self, column_names):
        column_definitions = ', '.join('{} VARCHAR(255)'.format(col) for col in column_names)  # List comprehension for table column name creation
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
            print("Employee with ID {} not exists.".format(id))  # can use f string also

    def promote_employee(self, id, new_post, salary_increase_percentage):
        query = "UPDATE {} SET post = %s, salary = salary + salary * %s / 100 WHERE id = %s".format(self.table_name)  # like in sql update Table_name Col1=x,Col2=y.... where id =Z
        values = (new_post, salary_increase_percentage, id)
        self.cur.execute("USE {}".format(self.database_name))
        self.cur.execute(query, values)
        self.my_db.commit()

    def close_connection(self):
        self.cur.close()
        self.my_db.close()
database_name = "empd"
table_name = "empllo"
e1 = Employee("localhost", "root", "admin123", database_name, table_name)


e1.create_database()
e1.create_table(("id", "name", "post", "salary"))
e1.insert_employee(id=1, name="Ravi", post="senior manager", salary=90000)
e1.insert_employee(id=2, name="Ravindar jadeja", post='manager', salary=70000)
e1.insert_employee(id=3, name="senorita", post="receptionist", salary=30000)
e1.insert_employee(id=4, name="renuka", post="team lead", salary=60000)
e1.insert_employee(id=5, name="rajendra", post="president", salary=1205864)
e1.delete_employee(6)
##e1.promote_employee(2, "Vice president", 0)

s = "SELECT * FROM {}".format(table_name)
e1.cur.execute(s)
result = e1.cur.fetchall()

for rec in result:
    print(rec)

e1.close_connection()
