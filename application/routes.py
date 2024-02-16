from application import app, bcrypt, login_manager, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask import render_template, request, flash, url_for, redirect, jsonify,json
from application.forms import PredictionForm, LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from application import ai_model
from application import db
from application.models import Entry, User
from datetime import datetime
import pandas as pd
import pytz, jwt

# Remove entry from database based on id
def remove_entry(id):
    try: 
        # Retrieve entry from database
        entry = db.get_or_404(Entry, id) 
        db.session.delete(entry) 
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0
    
# Add entry to database
def add_entry(new_entry):
    try:
        # Add user id to entry
        new_entry.user_id = current_user.id
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

# Retrieve all entries from database
def get_entries():
    try:
        # Retrieve all entries from database
        entries = db.session.execute(db.select(Entry).filter(Entry.user_id==current_user.id).order_by(Entry.id)).scalars()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return []
        
# Send password reset email
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message("Password Reset Request", recipients=[user.email], sender="daaa2b01.2214449.tanwentaobryan@gmail.com")
    msg.body = f'''
    Hi, {user.username}!

    To reset your password, visit the following link:
    {url_for("reset_password", token=token, _external=True)}

    CarGuru Team thanks you for using our service!

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

# Define user loader callback for Flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/predict", methods=['GET','POST'])
def predict():
    form = PredictionForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            carsprice_range = form.car_brand.data
            aspiration = form.aspiration.data
            citympg = form.citympg.data
            carlength = form.carlength.data
            curbweight = form.curbweight.data
            horsepower = form.horsepower.data
            wheelbase = form.wheelbase.data
            carbody = form.car_body.data
            drivewheel = form.drive_wheel.data
            enginetype = form.engine_type.data
            highwaympg = form.highwaympg.data
            carwidth = form.carwidth.data
            enginesize = form.enginesize.data
            boreratio = form.boreratio.data
            cylindernumber = form.cylinder_number.data

            # Calculate for fuel economy data
            fueleconomy = round((citympg * 0.55) + (highwaympg * 0.45), 2)
            timezone = pytz.timezone("Asia/Singapore")
            current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)

            X = [[aspiration, carbody, drivewheel, enginetype, cylindernumber, carsprice_range, fueleconomy, carlength, carwidth, curbweight, enginesize, boreratio, horsepower, wheelbase]]
            X_columns = ['aspiration', 'carbody', 'drivewheel', 'enginetype', 'cylindernumber', 'carsprice_range', 'fueleconomy', 'carlength', 'carwidth', 'curbweight', 'enginesize', 'boreratio', 'horsepower', 'wheelbase']
            X_df = pd.DataFrame(X, columns=X_columns)

            result = ai_model.predict(X_df)
            new_entry = Entry(carsprice_range = carsprice_range, 
                        aspiration = aspiration, 
                        carlength = carlength, 
                        curbweight = curbweight,
                        horsepower = horsepower,
                        wheelbase = wheelbase,
                        carbody = carbody,
                        drivewheel= drivewheel,
                        enginetype =enginetype,
                        carwidth = carwidth,
                        enginesize =enginesize,
                        boreratio = boreratio,
                        cylindernumber=cylindernumber,
                        fueleconomy = fueleconomy,
                        prediction=float(round(result[0], 2)), 
                        predicted_on=current_time)
            add_entry(new_entry) 
            flash(f"Prediction: ${result[0]:.2f}","success") 
        else: 
            flash("Error, cannot proceed with prediction","danger") 
    return render_template("index.html", title="Enter Car Price Parameters", form=form, index=True, entries=get_entries())

@app.route("/prediction")
@login_required
def index_page():
    form1 = PredictionForm()
    return render_template("index.html", form =form1, title="Enter Car Price Parameters")

@app.route("/home")
@login_required
def home():
    return render_template("home.html", title="What are the features used to affect the price of a car?")

@app.route("/history")
@login_required
def history_page():
    form = PredictionForm()
    return render_template("history.html", title="Prediction History", form=form, entries=get_entries())

@app.route('/remove', methods=['POST'])
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"] 
    remove_entry(id) 
    return render_template("history.html", title="Prediction History", form=form, entries = get_entries(), index=True) 

# Handles http://127.0.0.1:5000/
@app.route("/")
@app.route("/index")
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                flash(f'Welcome {form.username.data}! You are now logged in,', 'success')
                login_user(user, remember=form.remember.data)
                return redirect(url_for("home"))
            
        flash('Login Unsucessful. Please check your credentials again.', 'danger')

    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_page"))


@app.route("/register", methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    # Check if user is already logged in
    if current_user.is_authenticated:
        flash(f"You are already logged in as {current_user.username}", "info")
        return redirect(url_for("home"))

    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # Change timezone to Singapore
        timezone = pytz.timezone("Asia/Singapore")
        current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)

        # Add user to database
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, timestamp=current_time)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Try logging in now.', 'success')
    return render_template("register.html", title="Registration", form=form)

@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password_page():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # Checks if email exist in the database
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash("An email has been sent with instructions to reset your password.", "info")
            return redirect(url_for("login_page"))
        flash("Unregistered email. Please try again.", 'danger')
    
    return render_template("forgot_password.html", title="Forgot Password", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Invalid or expired token. Please try again.", "danger")
        return redirect(url_for("foreget_password_page"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated. You are now able to login.", "success")
        return redirect(url_for("login_page"))
    return render_template("reset_password.html", title="Reset Password", form=form)

####################### APIs for Unit Testing #######################

#### APIs - Prediction ####

# Predict API - test prediction
@app.route('/api/predict', methods=['GET', 'POST'])
def predict_api():
    data = request.get_json()
    X = [[data['aspiration'], data['carbody'], data['drivewheel'], data['enginetype'], data['cylindernumber'], data['carsprice_range'], 
          data['fueleconomy'], data['carlength'], data['carwidth'], data['curbweight'], data['enginesize'], data['boreratio'], 
          data['horsepower'], data['wheelbase']]]
    X_columns = ['aspiration', 'carbody', 'drivewheel', 'enginetype', 'cylindernumber', 'carsprice_range', 
                 'fueleconomy', 'carlength', 'carwidth', 'curbweight', 'enginesize', 'boreratio', 'horsepower', 'wheelbase']
    X_df = pd.DataFrame(X, columns=X_columns)
    result = ai_model.predict(X_df)
    return jsonify({'prediction': round(result[0],2)})

# Function for adding entry to database
def add_entry_API(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

# Add entry API - test adding entry to database
@app.route('/api/add_entry', methods=['POST'])
def add_api():
    #Retrieve data from request
    data = request.get_json()

    #Retrieve each field from data
    carsprice_range = data['carsprice_range']
    aspiration = data['aspiration']
    carlength = data['carlength']
    curbweight = data['curbweight']
    horsepower = data['horsepower']
    wheelbase = data['wheelbase']
    carbody = data['carbody']
    drivewheel = data['drivewheel']
    enginetype = data['enginetype']
    carwidth = data['carwidth']
    enginesize = data['enginesize']
    boreratio = data['boreratio']
    cylindernumber = data['cylindernumber']
    fueleconomy = data['fueleconomy']
    prediction = data['prediction']

    email = data["email"]
    # Retrieve the user id from database
    user_id = User.query.filter_by(email=email).first().id
    timezone = pytz.timezone("Asia/Singapore")
    current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
    #Create an Entry object that stores all the data for db action
    new_entry = Entry(
        user_id = user_id,
        carsprice_range = carsprice_range,
        aspiration = aspiration,
        carlength = carlength,
        curbweight = curbweight,
        horsepower = horsepower,
        wheelbase = wheelbase,
        carbody = carbody,
        drivewheel= drivewheel,
        enginetype =enginetype,
        carwidth = carwidth,
        enginesize =enginesize,
        boreratio = boreratio,
        cylindernumber=cylindernumber,
        fueleconomy = fueleconomy,
        prediction = prediction,
        predicted_on=current_time)
    # Invoke the add entry function to add entry
    new_result = add_entry_API(new_entry)

    # Stores the user's email in the variable
    user_email = User.query.filter_by(id=user_id).first().email

    # Return the id of the entry added
    return jsonify({'id': new_result, 'email': user_email})

# Function for retrieving entry from database based on user_id
def get_entries_API(user_id):
    try:
        # Retrieve all entries from database
        entries = db.session.execute(db.select(Entry).filter(Entry.user_id==user_id).order_by(Entry.id)).scalars()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return []
    
# Retrieve entry API test retrieving entry from database based on user_id
@app.route('/api/get_entries', methods=['GET'])
def get_api():
    # Retrieve data from request
    data = request.get_json()

    # Retrieve each field from data
    user_email = data['user_email']

    # Retrieve the user id from database
    user_id = User.query.filter_by(email = user_email).first().id

    # Retrieve all entries from database
    new_result = get_entries_API(user_id)
    new_results = []
    # Serialise the entries retrieved in JSON
    for entry in new_result:
        # Stores the user's email in the variable
        email = User.query.filter_by(id = entry.user_id).first().email
        new_results.append({'entry_id': entry.id,'user_email': email ,'prediction': entry.prediction})

    # Return the entries retrieved
    return jsonify({'entries': new_results})

# Function for removing entry from database based on entry_id
def remove_entry_API(entry_id):
    try:
        # Retrieve entry from database
        entry = db.get_or_404(Entry, entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'status': 'success', 'entry_id':entry_id, 'message':'Entry is removed successfully.'}
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return {'status': 'error', 'entry_id':0, 'message':str(error)}

# Remove entry API - test removing entry from database based on entry_id
@app.route('/api/remove_entry/<id>', methods=['GET'])
def remove_api(id):
    # Delete the entry from the database
    new_result = remove_entry_API(id)

    # Return the id of the entry deleted
    return jsonify(new_result)


#### APIs - Authentication ####

# Function for registering user to database
def register_user_API(user, email, password):
    try:
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password)

        # Change timezone to Singapore
        timezone = pytz.timezone("Asia/Singapore")
        current_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)

        # Add user to database
        new_user = User(username=user, email=email, password=hashed_password, timestamp=current_time)
        db.session.add(new_user)
        db.session.commit()

        # Return the id of the user added
        return new_user.id
    
    # Registration failure
    except Exception as e:
        db.session.rollback()
        flash(e, "danger")
        return None

# Register API - test user registration
@app.route('/api/register', methods=["GET","POST"])
def register_api():
    data = request.get_json()

    # Retrieve each field from data
    username = data['username']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

    # Check if password do not match the confirmed password
    if password != confirm_password:
        return jsonify({'status': 'error','registered': False ,'message': 'Passwords do not match.'})
        
    # Register the user
    new_user = register_user_API(username, email, password)
    
    if new_user is not None:
        # Return the userid in response
        return jsonify({'status': 'success', "registered": True, 'userid': new_user})
    else:
        return jsonify({'status': 'error', "registered": False})
    
# Function for logging in user
def login_user_API(username, password):
    # Validate the user
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Return the userid in response
        return user.id
    else:
        return None

# Login API - test user login
@app.route('/api/login', methods=["GET", "POST"])
def login_api():
    data = request.get_json()

    # Retrieve each field from data
    username = data["username"]
    password = data["password"]

    # Login the user
    result = login_user_API(username, password)

    if result:
        return jsonify({'status': 'success', 'userid': result, "logged_in": True})
    else:
        return jsonify({'status': 'error',"logged_in": False})
    

#### APIs - Password Reset ####

# Function for confirming user email
def check_email_API(email):
    # Validate the user
    user = User.query.filter_by(email=email).first()

    if user:
        # Return the userid in response
        return user.id
    else:
        return None

# Check email API - test if user email exist in the database
@app.route('/api/email_confirm', methods=["GET"])
def confirm_email():
    data = request.get_json()

    # Retrieve each field from data
    email = data["email"]

    # Check if email exists in the database
    result = check_email_API(email)

    if result:
        return jsonify({'status': 'success', 'userid': result, "email_confirm": True})
    else:
        return jsonify({'status': 'error', "email_confirm": False})