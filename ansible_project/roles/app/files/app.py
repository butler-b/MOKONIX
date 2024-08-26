from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from prometheus_client import Counter, Summary, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 설정
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'exampleuser'
app.config['MYSQL_PASSWORD'] = 'examplepass'
app.config['MYSQL_DB'] = 'hospitaldb'

mysql = MySQL(app)

# 로그 설정
logging.basicConfig(filename='hospital_bed_changes.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNTER = Counter('request_count', 'Number of requests')

# Wrap the application with the Prometheus WSGI middleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Decorator to monitor request duration
def track_request_time(func):
    def wrapper(*args, **kwargs):
        with REQUEST_TIME.time():
            REQUEST_COUNTER.inc()
            return func(*args, **kwargs)
    return wrapper

# 사용자 등록
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        hospital = request.form['hospital']
        role = request.form['role']
        
        try:
            with mysql.connection.cursor() as cur:
                logging.info(f"Attempting to register user: {username}, role: {role}")
                cur.execute("INSERT INTO user (username, password, hospital, role) VALUES (%s, %s, %s, %s)", 
                            (username, password, hospital, role))
                mysql.connection.commit()
            logging.info(f"User registered successfully: {username}")
            flash('Registration successful!', 'success')
        except Exception as e:
            logging.error(f"Error registering user {username}: {str(e)}")
            flash('Registration failed. Please try again.', 'danger')
        return redirect(url_for('login'))
    return render_template('register.html')

# 사용자 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with mysql.connection.cursor() as cur:
                logging.info(f"Attempting to log in user: {username}")
                cur.execute("SELECT * FROM user WHERE username = %s", [username])
                user = cur.fetchone()
                
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[4]
                logging.info(f"User logged in successfully: {username}, role: {user[4]}")
                if user[4] == '간호사':
                    return redirect(url_for('nurse_dashboard'))
                elif user[4] == '구조대원':
                    return redirect(url_for('paramedic_dashboard'))
                else:
                    logging.warning(f"Unauthorized role attempted: {user[4]}")
                    flash('Unauthorized role', 'danger')
                    return redirect(url_for('login'))
            else:
                logging.warning(f"Failed login attempt for user: {username}")
                flash('Invalid username or password', 'danger')
        except Exception as e:
            logging.error(f"Error during login for user {username}: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
        return redirect(url_for('login'))
        
    return render_template('login.html')

# 대시보드
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        logging.info(f"User accessing dashboard: {session['username']}, role: {session['role']}")
        if session['role'] == '간호사':
            return redirect(url_for('nurse_dashboard'))
        elif session['role'] == '구조대원':
            return redirect(url_for('paramedic_dashboard'))
        else:
            logging.warning(f"Unrecognized role: {session['role']}")
            return "Role not recognized", 403
    return redirect(url_for('login'))

# 간호사 대시보드
@app.route('/nurse_dashboard', methods=['GET', 'POST'])
def nurse_dashboard():
    if request.method == 'POST':
        try:
            hospital_name = request.form['hospitalName']
            using_hospital_beds = request.form['usingHospitalBeds']

            with mysql.connection.cursor() as cur:
                logging.info(f"Updating hospital beds for {hospital_name}: {using_hospital_beds}")
                cur.execute("""
                    UPDATE Hos_data 
                    SET UsingHospitalBeds = %s 
                    WHERE HospitalName = %s
                """, (using_hospital_beds, hospital_name))
                mysql.connection.commit()

            logging.info(f"Hospital bed count updated for {hospital_name}: {using_hospital_beds}")
            flash('Hospital bed count updated successfully!', 'success')
        except Exception as e:
            logging.error(f"Error updating hospital beds for {hospital_name}: {str(e)}")
            flash('Failed to update hospital bed count.', 'danger')
            return str(e), 500

    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT HospitalName FROM Hos_data")
            hospitals = cur.fetchall()
        logging.info("Hospital data retrieved successfully.")
    except Exception as e:
        logging.error(f"Error retrieving hospital data: {str(e)}")
        flash('Failed to load hospital data.', 'danger')
        hospitals = []

    return render_template('nurse_dashboard.html', hospitals=hospitals)

# 구조대원 대시보드
@app.route('/paramedic_dashboard')
def paramedic_dashboard():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM Hos_data")
            hospitals = cur.fetchall()
            logging.info(f"Hospitals data retrieved: {hospitals}")
    except Exception as e:
        logging.error(f"Error retrieving hospital data: {str(e)}")
        flash('Failed to load hospital data.', 'danger')
        hospitals = []

    return render_template('paramedic_dashboard.html', hospitals=hospitals)

# 진료 예약
@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        try:
            patient_name = request.form['patient_name']
            appointment_date = request.form['appointment_date']
            appointment_time = request.form['appointment_time']
            doctor_name = request.form['doctor_name']
            contact_info = request.form['contact_info']

            with mysql.connection.cursor() as cur:
                logging.info(f"Booking appointment for {patient_name} with {doctor_name} on {appointment_date} at {appointment_time}")
                cur.execute("""
                    INSERT INTO appointments (patient_name, appointment_date, appointment_time, doctor_name, contact_info)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_name, appointment_date, appointment_time, doctor_name, contact_info))
                mysql.connection.commit()

            logging.info(f"Appointment booked for {patient_name} with {doctor_name}")
            return redirect(url_for('appointment_success'))
        except Exception as e:
            logging.error(f"Error booking appointment for {patient_name}: {str(e)}")
            flash('Failed to book appointment.', 'danger')
            return str(e), 500
    return render_template('book_appointment.html')

# 예약 성공 페이지
@app.route('/appointment-success', methods=['GET'])
def appointment_success():
    logging.info("Appointment success page accessed.")
    return render_template('appointment_success.html')

# 환자 등록
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'role' not in session or session['role'] != '구조대원':
        logging.warning(f"Unauthorized access attempt by {session.get('username')}")
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))

    hospitals_matched = []
    all_patients = []

    if request.method == 'POST':
        try:
            patient_id = request.form.get('patient_id')
            name = request.form.get('name')
            birthdate = request.form.get('birthdate')
            blood_type = request.form.get('blood_type')
            icd = request.form.get('icd').strip()

            logging.info(f"Adding new patient: {name}, ICD: {icd}")

            # ICD 코드 디버깅
            print(f"ICD code provided: {icd}")

            with mysql.connection.cursor() as cur:
                # 환자 정보 추가
                cur.execute("""
                    INSERT INTO MedData (PatientID, Name, BirthDate, BloodType, ICD)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_id, name, birthdate, blood_type, icd))
                mysql.connection.commit()

                # 병원 검색 쿼리
                cur.execute("SELECT * FROM Hos_data WHERE ICD LIKE %s", [f"%{icd}%"])
                hospitals_matched = cur.fetchall()

                # 쿼리 결과 디버깅
                print(f"Matching hospitals found: {hospitals_matched}")

            logging.info(f"Patient added: {name}, searching for matching hospitals")
            logging.info(f"Matching hospitals found: {hospitals_matched}")
            flash('New patient record added successfully!', 'success')
        except Exception as e:
            logging.error(f"Error adding patient {name}: {str(e)}")
            flash('Failed to add patient.', 'danger')
            return str(e), 500

    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM MedData")
            all_patients = cur.fetchall()
            logging.info(f"All patients data retrieved: {all_patients}")
    except Exception as e:
        logging.error(f"Error retrieving patient data: {str(e)}")
        flash('Failed to load patient data.', 'danger')
        all_patients = []

    logging.info(f"Rendering template with hospitals: {hospitals_matched} and patients: {all_patients}")
    return render_template('add_patient.html', 
                           hospitals_matched=hospitals_matched, 
                           all_patients=all_patients)



@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    delete_ids = request.form.getlist('delete_ids')
    
    if delete_ids:
        try:
            with mysql.connection.cursor() as cur:
                for patient_id in delete_ids:
                    cur.execute("DELETE FROM MedData WHERE PatientID = %s", [patient_id])
                mysql.connection.commit()

            flash(f'{len(delete_ids)}명의 환자가 삭제되었습니다.', 'success')
        except Exception as e:
            logging.error(f"Error deleting patients with IDs {delete_ids}: {str(e)}")
            flash('Failed to delete selected patients.', 'danger')
    else:
        flash('삭제할 환자를 선택하세요.', 'danger')
    
    return redirect(url_for('add_patient'))

# 로그아웃
@app.route('/logout')
def logout():
    logging.info(f"User logged out: {session.get('username')}")
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# 응급 구조 센터 페이지
@app.route('/emergency-center')
def emergency_center():
    logging.info("Emergency center page accessed.")
    return render_template('emergency_center.html')
# Index 페이지 라우트
@app.route('/')
def index():
    return redirect('http://localhost')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

