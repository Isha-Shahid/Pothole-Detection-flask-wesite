import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "esha_secret_key"

# --- 1. DATABASE & UPLOAD CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)


# --- 2. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), default="Pending")
    status = db.Column(db.String(20), default="Reported")
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


# --- 3. ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        selected_role = request.form.get('role')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            if user.role == selected_role:
                session['user'] = user.fullname
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect(url_for(f"{user.role}_dashboard"))
            else:
                flash("Unauthorized: Access denied for this specific workspace.")
        else:
            flash("Invalid credentials. Please try again.")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for('login'))

        new_user = User(fullname=fullname, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/report', methods=['POST'])
def report():
    if 'pothole_image' not in request.files:
        flash("No image uploaded")
        return redirect(request.url)

    file = request.files['pothole_image']
    location = request.form.get('location')

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # FYP TIP: This is where you would call your AI model.
        # For now, we are simulating AI result as "Moderate"
        new_report = Report(location=location, image_file=filename, severity="Moderate")
        db.session.add(new_report)
        db.session.commit()

        flash("Report submitted! AI is analyzing the severity.")
        return redirect(url_for('user_dashboard'))


# --- 4. ACTION ROUTES ---

@app.route('/fix/<int:report_id>', methods=['POST'])
def fix_report(report_id):
    if session.get('role') != 'maintenance':
        return redirect(url_for('login'))

    report = Report.query.get_or_404(report_id)
    report.status = "Fixed"
    db.session.commit()
    flash(f"Job #RG-{report_id} marked as Fixed!")
    return redirect(url_for('maintenance_dashboard'))


# --- 5. DASHBOARDS ---

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    all_reports = Report.query.all()
    total = len(all_reports)
    active = Report.query.filter_by(status='Reported').count()
    fixed = Report.query.filter_by(status='Fixed').count()

    # Chart Stats
    crit = Report.query.filter_by(severity='Critical').count()
    mod = Report.query.filter_by(severity='Moderate').count()
    min_r = Report.query.filter_by(severity='Minor').count()

    rate = round((fixed / total * 100), 1) if total > 0 else 0

    return render_template('admin.html',
                           user=session['user'],
                           reports=all_reports,
                           active_count=active,
                           repair_rate=rate,
                           crit_count=crit, mod_count=mod, min_count=min_r)


@app.route('/maintenance_dashboard')
def maintenance_dashboard():
    if session.get('role') != 'maintenance':
        return redirect(url_for('login'))

    pending_jobs = Report.query.filter_by(status="Reported").all()
    return render_template('maintenance.html', user=session['user'], reports=pending_jobs)


@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login'))

    # Show all reports so users can see existing issues
    all_reports = Report.query.order_by(Report.date_posted.desc()).all()
    return render_template('user.html', user=session['user'], reports=all_reports)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)