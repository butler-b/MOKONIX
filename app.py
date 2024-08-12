from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:soldesk@localhost/CareDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

# 사용자 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# 병원 데이터 모델 정의
class HospitalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usinghospitalbed = db.Column(db.Integer, nullable=False)

# 데이터베이스와 테이블 생성
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hospital = request.form['hospital']
        role = request.form['role']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, hospital=hospital, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    role = session.get('role')
    if role == 'nurse':
        return redirect(url_for('nurse_homepage'))
    elif role == 'emergency':
        return redirect(url_for('emergency_homepage'))
    return redirect(url_for('index'))

@app.route('/nurse_homepage', methods=['GET', 'POST'])
def nurse_homepage():
    if request.method == 'POST':
        new_bed_count = request.form.get('usinghospitalbed')
        hospital_data = HospitalData.query.first()
        if hospital_data:
            hospital_data.usinghospitalbed = new_bed_count
            db.session.commit()
            flash('Hospital bed count updated!', 'success')
        else:
            flash('No hospital data found!', 'danger')
    return render_template('nurse_homepage.html')

@app.route('/emergency_homepage')
def emergency_homepage():
    return render_template('emergency_homepage.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 데이터베이스와 테이블을 생성합니다.
    with app.app_context():
        create_tables()
    app.run(debug=True)
