import mysql.connector
from configuration.config import parameters
class EmployeeDatabase:
    def __init__(self, database_name):
        self.connection = mysql.connector.connect(host=parameters["host"], user=parameters["user"],  password=parameters["password"])
        self.cursor = self.connection.cursor()
        self.database_name = database_name

    def create_database(self):
        try:
            query = f"CREATE DATABASE {self.database_name}"
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating the database: {err}")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

class Employee:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def create_table(self, column_names):
        try:
            column_definitions = ', '.join('{} VARCHAR(255)'.format(col) for col in column_names)
            print("col definition",column_definitions)
            query = "CREATE TABLE {} ({})".format(self.table_name, column_definitions)
            self.db.cursor.execute("USE {}".format(self.db.database_name))
            self.db.cursor.execute(query)
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating the table: {err}")

    def check_duplicate(self, id):
        try:
            query = "SELECT COUNT(*) FROM {} WHERE id = %s".format(self.table_name)
            value = (id,)
            self.db.cursor.execute("USE {}".format(self.db.database_name))
            self.db.cursor.execute(query, value)
            count = self.db.cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Error checking for duplicates: {err}")
            return False

    def insert_employee(self, **kwargs):
        try:
            if self.check_duplicate(kwargs.get('id')):
                print("Employee with ID {} already exists.".format(kwargs.get('id')))
                return
            column_names = ', '.join(kwargs.keys())
            placeholders = ', '.join('%s' for _ in kwargs.values())
            query = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, column_names, placeholders)
            values = tuple(kwargs.values())
            self.db.cursor.execute("USE {}".format(self.db.database_name))
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("Employee added successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting employee: {err}")

    def delete_employee(self, id):
        try:
            if self.check_duplicate(id):
                query = "DELETE FROM {} WHERE id = %s".format(self.table_name)
                values = (id,)
                self.db.cursor.execute("USE {}".format(self.db.database_name))
                self.db.cursor.execute(query, values)
                self.db.connection.commit()
            else:
                print("Employee with ID {} does not exist.".format(id))
        except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")

    def promote_employee(self, id, new_post, salary_increase_percentage):
        try:
            query = "UPDATE {} SET post = %s, salary = salary + salary * %s / 100 WHERE id = %s".format(self.table_name)
            values = (new_post, salary_increase_percentage, id)
            self.db.cursor.execute("USE {}".format(self.db.database_name))
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("Employee promoted successfully.")
        except mysql.connector.Error as err:
            print(f"Error promoting employee: {err}")

def main():
    database_name = "Wipro"
    table_name = "employees"
    db = EmployeeDatabase(database_name)
    e1 = Employee(db, table_name)

    db.create_database()
    e1.create_table(("id", "name", "post", "salary"))

    e1.insert_employee(id=1, name="Ravi", post="senior manager", salary=90000)
    e1.insert_employee(id=2, name="Ravindar jadeja", post="manager", salary=70000)
    e1.insert_employee(id=3, name="senorita", post="receptionist", salary=30000)
    e1.insert_employee(id=4, name="renuka", post="team lead", salary=60000)
    e1.insert_employee(id=5, name="rajendra", post="president", salary=1205864)
    e1.delete_employee(6)
    e1.promote_employee(2, "Vice president", 10)

    select_query = f"SELECT * FROM {table_name}"
    e1.db.cursor.execute(select_query)
    result = e1.db.cursor.fetchall()

    for rec in result:
        print(rec)

    db.close_connection()

if __name__ == "__main__":
    main()
