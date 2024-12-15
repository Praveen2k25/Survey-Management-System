from flask import Flask, render_template, request, jsonify
import mariadb

app = Flask(__name__)


db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'surveyss' 
}


def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def survey_form():
    return render_template('survey_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    name = request.form['name']
    income = request.form['income']
    employment_status = request.form['status']
    relationship_status = request.form['relationship']

   
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
          
            cursor.execute('''
                INSERT INTO resp (name, income, employment_status, relationship_status)
                VALUES (?, ?, ?, ?)
            ''', (name, income, employment_status, relationship_status))
            conn.commit()
            response = {'success': True}
        except mariadb.Error as e:
            print(f"Error saving to the database: {e}")
            response = {'success': False, 'error': str(e)}
        finally:
            conn.close()
    else:
        response = {'success': False, 'error': 'Database connection failed.'}

    return jsonify(response)

@app.route('/responses', methods=['GET'])
def view_responses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, income, employment_status, relationship_status FROM resp")
        responses = cursor.fetchall()
        conn.close()

   
        response_list = [{'name': row[0], 'income': row[1], 'employment_status': row[2], 'relationship_status': row[3]} for row in responses]
        return jsonify(response_list)  
    else:
        return jsonify({'success': False, 'error': 'Database connection failed.'})

if __name__ == '__main__':
    app.run(debug=True)
