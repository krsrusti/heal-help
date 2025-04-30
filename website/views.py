from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import BloodSugar
from . import db

views = Blueprint('views', __name__)



@views.route('/')
def welcome():
    return render_template("welcome.html", user=current_user)

@views.route('/graphs')
@login_required
def graph ():
  

  render_template("graphs.html",user=current_user)



@views.route('/home', methods=['GET', 'POST'])
@login_required
def add_blood_sugar():
    if request.method == 'POST':
      
        meal_time = request.form.get('meal_time')
        print(meal_time)
        log_date = request.form.get('log_date')
        print(log_date)
        blood_sugar_level = request.form.get('blood_sugar_level')
        print(blood_sugar_level)
        sugar_type = request.form.get('sugar_type')
        print(sugar_type)
        user_id = current_user.id
        print(user_id)

        
        if not meal_time or not log_date or not blood_sugar_level or not sugar_type:
            flash('All fields are required', category='error')
            return redirect(url_for('views.add_blood_sugar'))

        try:
            blood_sugar_level = int(blood_sugar_level)
        except ValueError:
            flash('Blood sugar level must be a number', category='error')
            return redirect(url_for('views.add_blood_sugar'))

        
        def get_category(level, sugar_type):
            if sugar_type == "beforeFood":
                if level < 70:
                    return "low"
                elif 70 <= level <= 99:
                    return "normal"
                elif 100 <= level <= 125:
                    return "prediabetes"
                else:
                    return "High"
            elif sugar_type == "afterFood":
                if level < 140:
                    return "normal"
                elif 140 <= level <= 199:
                    return "prediabetes"
                else:
                    return "High"
            else:  
                if level < 70:
                    return "low"
                elif 70 <= level <= 140:
                    return "normal"
                else:
                    return "High"

        category = get_category(blood_sugar_level, sugar_type)

       
        new_log = BloodSugar(
            meal_time=meal_time,
            log_date=log_date,
            blood_sugar_level=blood_sugar_level,
            sugar_type=sugar_type,
            category=category,
            user_id=user_id
        )

        try:
            db.session.add(new_log)
            db.session.commit()
            flash('Blood sugar level logged successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', category='error')

    
    blood_sugar_logs = BloodSugar.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, blood_sugar_logs=blood_sugar_logs)



@views.route('/view_record')
@login_required
def view_record():
    blood_sugar_logs = BloodSugar.query.filter_by(user_id=current_user.id).all()

    def get_category(level, sugar_type):

        
        if sugar_type == "beforeFood":
            if level < 70:
                return "low"
            elif 70 <= level <= 99:
                return "normal"
            elif 100 <= level <= 125:
                return "prediabetes"
            else:
                return "high"
            

        elif sugar_type == "afterFood":
            if level < 140:
                return "normal"
            elif 140 <= level <= 199:
                return "prediabetes"
            else:
                return "high"
            

        else:
            if level < 70:
                return "low"
            elif 70 <= level <= 140:
                return "normal"
            else:
                return "high"


    for log in blood_sugar_logs:
        log.category = get_category(log.blood_sugar_level, log.sugar_type)

    return render_template('view_record.html', user=current_user, blood_sugar_logs=blood_sugar_logs)


