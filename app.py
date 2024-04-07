from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


DATABASE = 'database.db'
TOPIC = "Zakriya/testing"

User=''
Passw=''

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bus (
            Name VARCHAR(100) NOT NULL,
            Route VARCHAR(100) NOT NULL,
            BusNo VARCHAR(20) NOT NULL,
            Capacity INT NOT NULL,
            DriverName VARCHAR(100) NOT NULL,
            DriverId VARCHAR(20) NOT NULL
        ); ''')
    
    
    conn.commit()
    conn.close()


create_table()



def create_table1():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            StudentID VARCHAR(20) PRIMARY KEY,
            StudentName VARCHAR(100),
            Department VARCHAR(100),
            Degree VARCHAR(100),
            ContactNumber VARCHAR(20),
            BusName VARCHAR(100));''')
    
    
    conn.commit()
    conn.close()

create_table1()

@app.route('/buses', methods=['GET'])
def get_available_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bus")
    data = cursor.fetchall()
    conn.close()
    bus_list = [
        {
        'Name': row[0],
        'Route': row[1],
        'BusNo': row[2],
        'Capacity': row[3],
        'DriverName': row[4],
        'DriverId': row[5]
        }
        for row in data
    ]
    return jsonify(bus_list)
@app.route('/login', methods=['GET'])
def login():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student")
    data = cursor.fetchall()
    conn.close()
    bus_list = [
        {

        'StudentID': row[0],
        'Name': row[1],
        'Department': row[2],
        'Degree': row[3],
        'ContactNumber': row[4],
        'Password': row[6]
        }
        for row in data
    ]
    return jsonify(bus_list)
@app.route('/enrollg', methods=['GET'])
def enrollg():
    print(global_user)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Student where StudentID=? and Password=?",(global_user,global_passw))
    data = cursor.fetchall()
    conn.close()
    bus_list = [
        {

        'StudentID': row[0],
        'Name': row[1],
        'Department': row[2],
        'Degree': row[3],
        'ContactNumber': row[4],
        }
        for row in data
    ]
    return jsonify(bus_list)
@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    bus = data['Busname']
    print(bus)
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Student SET BusName=? WHERE StudentID=? AND Password=?", (bus, global_user, global_passw))
        conn.commit()
        return jsonify({'message': 'Bus data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        
        conn.close()
@app.route('/delete', methods=['POST'])
def delete():
   
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Student SET BusName=NULL WHERE StudentID=? AND Password=?", ( global_user, global_passw))
        conn.commit()
        return jsonify({'message': 'Bus data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        
        conn.close()
@app.route('/deleteBus', methods=['POST'])
def deleteBus():
    data = request.get_json()
    bus = data['selectedBusName']
    print(bus)
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Student SET BusName = NULL WHERE BusName = ?", (bus,))
        cursor.execute("DELETE from Bus where Name= ? ", (bus,))
        conn.commit()
        return jsonify({'message': 'Bus data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        
        conn.close()
@app.route('/updatebus', methods=['POST'])
def UpdateBus():
    data = request.get_json()
    bus = data['Busname']
    print(bus)
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Student SET BusName=? WHERE StudentID=? AND Password=?", ( bus,global_user, global_passw))
        conn.commit()
        return jsonify({'message': 'Bus data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        
        conn.close()
    # You may want to return something to indicate success
@app.route('/check', methods=['POST'])
def check():
    global global_user, global_passw
    
    data = request.get_json()
    print(data)
    
    
    global_user = data['username']
    global_passw = data['password']
    print(global_passw)
    
    # You may want to return something to indicate success
    return jsonify({'message': 'Data stored successfully'}), 200

@app.route('/Update', methods=['POST'])
def process_products():
    data = request.get_json()
   

    if 'bus_data' not in data:
        return jsonify({'error': 'Bus data not provided'}), 400

    bus_data = data['bus_data']


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
    
            # Extracting data from the bus dictionary
        name = bus_data['Name']
        route = bus_data['Route']
        bus_no = bus_data['BusNo']
        capacity = bus_data['Capacity']
        driver_name = bus_data['DriverName']
        driver_id = bus_data['DriverId']
    
            # Update the bus entity in the database
        cursor.execute(
            "UPDATE Bus SET Name=?, Route=?, BusNo=?, Capacity=?, DriverName=?, DriverId=? WHERE Name=?",
            (name, route, bus_no, capacity, driver_name, driver_id, name)
            )

        conn.commit()

        return jsonify({'message': 'Bus data updated successfully'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        conn.close()

@app.route('/signup', methods=['POST'])
def enroll_student():
    data = request.get_json()
    if 'bus_data' not in data:
        return jsonify({'error': 'Bus data not provided'}), 400
    student_data = data['bus_data']
    print(student_data)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:    
            # Extracting data from the bus dictionary
        studentId = student_data['StudentID']
        sname = student_data['Name']
        depart = student_data['Department']
        degree = student_data['Degree']
        cnumber = student_data['ContactNumber']
        password = student_data['password']
        
    
            # Update the bus entity in the database
        cursor.execute(
         "INSERT INTO Student(StudentID, StudentName, Department, Degree, ContactNumber, Password) VALUES (?,?,?,?,?,?)",
        (studentId, sname, depart, degree, cnumber, password))
        print('Hi')
        conn.commit()

        return jsonify({'message': 'Bus data updated successfully'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        
        conn.close()



# @app.route('/route', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     var1 = data.get('var1')
#     var2 = data.get('var2')

#     if not var1 or not var2:
#         return jsonify({'error': 'Missing var1 or var2'}), 400

#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute(
#         'INSERT INTO sample (var1, var2) VALUES (?, ?)',
#         (var1, var2)
#     )
#     conn.commit()
#     conn.close()

#     return jsonify({'message': 'vars created successfully'})

###########For Students###################
@app.route('/add', methods=['POST'])
def add_bus():
    data = request.get_json()
   

    if 'bus_data' not in data:
        return jsonify({'error': 'Bus data not provided'}), 400

    bus_data = data['bus_data']


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
    
            # Extracting data from the bus dictionary
        name = bus_data['Name']
        route = bus_data['Route']
        bus_no = bus_data['BusNo']
        capacity = bus_data['Capacity']
        driver_name = bus_data['DriverName']
        driver_id = bus_data['DriverId']
        
    
            # Update the bus entity in the database
        cursor.execute(
         "INSERT INTO Bus(Name, Route, BusNo, Capacity, DriverName, DriverId) VALUES (?,?,?,?,?,?)",
        (name, route, bus_no, capacity, driver_name, driver_id))

        conn.commit()

        return jsonify({'message': 'Bus data updated successfully'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        conn.close()

    
if __name__ == '__main__':
    app.run(debug=False)