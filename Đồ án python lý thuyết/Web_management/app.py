from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Khóa bảo mật cho session

bcrypt = Bcrypt()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="employee_management",
    auth_plugin="mysql_native_password"
)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Sử dụng .get() để tránh KeyError
        password = request.form.get('password')

        # Kiểm tra thông tin đăng nhập
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid username or password", 401

    return render_template('login.html')


#Route Logout
@app.route('/logout')
def logout():
    # Kiểm tra nếu người dùng đang đăng nhập
    if 'logged_in' in session:
        session.pop('logged_in', None)  # Xóa session logged_in
    return redirect(url_for('login'))

# Hàm để kết nối với MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="employee_management"
    )

# Hàm để lấy dữ liệu nhân viên từ MySQL
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

# Hàm để thêm nhân viên vào MySQL
def add_employee(name, position, department, salary):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO employees (name, position, department, salary) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, position, department, salary))
    conn.commit()
    conn.close()

# Hàm để tìm kiếm nhân viên theo tên hoặc vị trí
def search_employees(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute(
        "SELECT * FROM employees WHERE name LIKE %s OR position LIKE %s",
        (search_query, search_query)
    )
    employees = cursor.fetchall()
    conn.close()
    return employees

# Route chính để hiển thị trang HTML, yêu cầu đăng nhập
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# API để lấy dữ liệu nhân viên dưới dạng JSON
@app.route('/api/employees')
def employees():
    employees = get_employees()
    employee_data = [{"id": emp[0], "name": emp[1], "position": emp[2], "department": emp[3], "salary": float(emp[4])} for emp in employees]
    return jsonify(employee_data)

# API để thêm nhân viên mới
@app.route('/api/add_employee', methods=['POST'])
def add_employee_route():
    data = request.json
    name = data.get('name')
    position = data.get('position')
    department = data.get('department')
    salary = data.get('salary')

    add_employee(name, position, department, salary)
    return jsonify({"message": "Employee added successfully"}), 201

# Hàm để cập nhật thông tin nhân viên
def update_employee(emp_id, name, position, department, salary):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE employees 
        SET name = %s, position = %s, department = %s, salary = %s 
        WHERE id = %s
    """
    cursor.execute(query, (name, position, department, salary, emp_id))
    conn.commit()
    conn.close()

# API để cập nhật nhân viên
@app.route('/api/update_employee', methods=['PUT'])
def update_employee_route():
    data = request.json
    emp_id = data.get('id')
    name = data.get('name')
    position = data.get('position')
    department = data.get('department')
    salary = data.get('salary')
    
    update_employee(emp_id, name, position, department, salary)
    return jsonify({"message": "Employee updated successfully"}), 200

# Hàm để xóa nhân viên
def delete_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (emp_id,))
    conn.commit()
    conn.close()

# API để xóa nhân viên
@app.route('/api/delete_employee/<int:emp_id>', methods=['DELETE'])
def delete_employee_route(emp_id):
    delete_employee(emp_id)
    return jsonify({"message": "Employee deleted successfully"}), 200

@app.errorhandler(404)
def page_not_found(e):
    return "The page does not exist", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
