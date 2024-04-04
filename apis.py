import csv, sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/healthcheck/')
def hello_world():
   return f"I'm alive"

'''
Function to Create a table
'''
def initialize_app():
    # Connect to the SQLite database (creates a new database if it doesn't exist)
    try:    
        conn = sqlite3.connect('customer.db')
        cursor = conn.cursor()

        # Create a table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customer_dimension (
                        cust_no INTEGER PRIMARY KEY,
                        firstname TEXT,
                        lastname TEXT,
                        email TEXT,
                        city TEXT,
                        phonenumber TEXT)''')

        # Commit the changes
        conn.commit()

        # Close the cursor and the connection
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
'''
Dump data from csv to SQLITE3
'''
@app.route('/dump_data/')
def dumpData():
    try:
        # Initialize the Flask app
        initialize_app()

        with app.app_context():
            conn = sqlite3.connect('customer.db')
            cursor = conn.cursor()

            # Read data from the CSV file
            data = []
            with open('cust_dimension.csv', 'r', newline='') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    cust_no = row['cust_no']
                    firstname = row['firstname']
                    lastname = row['lastname']
                    email = row['email']
                    city=row['city']
                    phonenumber = row['phonenumber']
                    data.append((cust_no, firstname, lastname, email, city, phonenumber))

            # Insert data into the table using bulk insertion
            cursor.executemany("INSERT INTO customer_dimension (cust_no, firstname, lastname, email, city, phonenumber) \
                            VALUES (?, ?, ?, ?, ?, ?)", data)

            # Commit the changes
            conn.commit()

            # Close the cursor and the connection
            cursor.close()
            conn.close()
        return jsonify({'message': 'Data dumped successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

'''
Route to drop the table
Returns 200
'''
@app.route('/drop_table/')
def dropTable():
    try:
        with app.app_context():
            conn = sqlite3.connect('customer.db')
            cursor = conn.cursor()
            
            cursor.execute('''DROP TABLE IF EXISTS customer_dimension''')
            
            conn.commit()
            cursor.close()
            conn.close()

        return jsonify({'message': 'Table dropped successfully'}), 200
    except Exception as e:
       return jsonify({'error': str(e)}), 500 

'''
Delete the row from table
Returns 204cus
'''
@app.route('/customer/<cust_no>', methods=['DELETE'])
def deleteRow(cust_no):
    try:
        with app.app_context():
            conn = sqlite3.connect('customer.db')
            cursor = conn.cursor()
        
            cursor.execute('''SELECT * FROM customer_dimension where cust_no = ?''',(cust_no,))
            rows = cursor.fetchone()

            if rows is None:
                return jsonify({'message': 'No data found'}), 404
            
            cursor.execute('''DELETE FROM customer_dimension where cust_no = ?''',(cust_no,))
            conn.commit()
            cursor.close()
            conn.close()

        return jsonify({'message': '{cust_no}} deleted successfully'}), 204
    except Exception as e:
       return jsonify({'error': str(e)}), 500 

'''
Route to get a customer with customer ID.
'''
@app.route('/customer/<cust_no>', methods=['GET'])
def getRow(cust_no):
    try:
        with app.app_context():
            conn = sqlite3.connect('customer.db')
            cursor = conn.cursor()
        
            cursor.execute('''SELECT * FROM customer_dimension where cust_no = ?''',(cust_no,))
            rows = cursor.fetchone()

            if rows is None:
                return jsonify({'message': 'No data found'}), 404
            cursor.close()
            conn.close()

        return jsonify({'message': 'Row fetched successfully',
                        'data': rows}), 200
    except Exception as e:
       return jsonify({'error': str(e)}), 500

'''
Route to add a new row
'''
@app.route('/customer', methods=['POST'])
def add_customer():
    try:
        with app.app_context():
            # Connect to the SQLite database
            conn = sqlite3.connect('customer.db')
            cursor = conn.cursor()

            # Parse request data
            data = request.get_json()
            cust_no = data.get('cust_no')
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            email = data.get('email')
            city = data.get('city')
            phonenumber = data.get('phonenumber')

            # Check if customer with the same cust_no already exists
            cursor.execute("SELECT * FROM customer_dimension WHERE cust_no=?", (cust_no,))
            if cursor.fetchone():
                return jsonify({'error': f'Customer with ID {cust_no} already exists'}), 409

            # Insert new customer into the database
            cursor.execute("INSERT INTO customer_dimension (cust_no, firstname, lastname, email, city, phonenumber) VALUES (?, ?, ?, ?, ?, ?)",
                        (cust_no, firstname, lastname, email, city, phonenumber))

            # Commit changes
            conn.commit()

        return jsonify({'message': 'Customer added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)