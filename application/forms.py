from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField, RadioField, StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import Length, InputRequired, ValidationError, NumberRange, Regexp, EqualTo
from application.models import User

class PredictionForm(FlaskForm):
    #Dropdown menu

    # Store the binned values of the average price of the car brands
    car_brand = SelectField("Car Brand", choices =[
        ('Medium Price', 'Alfa-Romeo'), ('Medium Price', 'Audi'), ('Highend Price', 'BMW'), ('Budget Price', 'Chevrolet'), ('Budget Price', 'Dodge'), ('Budget Price', 'Honda'), 
        ('Budget Price', 'Isuzu'), ('Highend Price', "Jaguar"), ('Medium Price', 'Mazda'), ('Highend Price','Buick'), ('Medium Price', 'Mercury'), ('Budget Price', 'Mitsubishi'),
        ('Medium Price', 'Nissan'), ('Medium Price', 'Peugeot'), ('Budget Price', 'Plymouth'), ('Highend Price', 'Porsche'), ('Budget Price', 'Renault'),
        ('Medium Price', 'Saab'), ('Budget Price', 'Subaru'), ('Budget Price', 'Toyota'), ('Medium Price', 'Volkswagen'), ('Medium Price', "Volvo")], 
        validators = [InputRequired()])
    aspiration = SelectField("Aspiration", choices=[('std', 'Standard'), ('turbo', 'Turbo')], default = "std")
    drive_wheel = SelectField("Drive Wheel", choices =[('4wd', '4 Wheel Drive'), ('fwd', 'Front Wheel Drive'), ('rwd', 'Rear Wheel Drive')], default ="fwd")
    engine_type = SelectField("Engine Type", choices=[
        ('dohc', 'Double Overhead Camshaft'), ('ohcv','Overhead Camshaft, V-shaped'), ('ohc', 'Overhead Camshaft'), ('l', 'Lateral'),
        ('rotor','Rotory'), ('ohcf', 'Overhead Camshaft, Front')], default='ohc')
    
    #Radio Buttons
    car_body = RadioField("Car Body", choices=[
        ('convertible', 'Convertible'), ('hardtop', 'Hardtop'), ('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('wagon','Wagon')],
        validators=[InputRequired()], default='sedan'
        )
    
    cylinder_number = RadioField("Cylinder Number", choices=[
        ('two', '2'), ('four', '4'), ('five', '5'), ('six', '6'), ('eight', '8')], validators=[InputRequired()])

    #Input Fields
    citympg = FloatField("City miles per gallon", validators=[InputRequired(), NumberRange(min=10, message="City mpg has to be more than 10")], default=24.0)
    highwaympg = FloatField("Highway miles per gallon", validators=[InputRequired(), NumberRange(min=15, message="Highway mpg has to be more than 15")], default=30.0)
    carlength = FloatField("Car Length (Inches)", validators=[InputRequired(), NumberRange(min=100, message="Car length has to be above 100 inches")], default=174.0)
    carwidth = FloatField("Car Width (Inches)", validators=[InputRequired(), NumberRange(min=50, message="Car width has to be more than 50 inches")], default=65.5)
    curbweight = FloatField("Curb Weight (Pounds)", validators=[InputRequired(), NumberRange(min=1000, message="Car pounds has to be more than 1000 pounds")], default=2555.0)
    enginesize = FloatField("Engine Size (Cubic Inches)", validators=[InputRequired(), NumberRange(min=40, message="Engine size has to be more than 40 cubic inches")], default=120.0)
    horsepower = FloatField("Horsepower", validators=[InputRequired(), NumberRange(min=40, message="Horsepower has to be more than 40 hp")], default=152.0)
    boreratio = FloatField("Bore Ratio", validators=[InputRequired(), NumberRange(min=2, message="Bore ratio has to be more than 2")], default=3.19)
    wheelbase = FloatField("Wheelbase (Inches)", validators=[InputRequired(), NumberRange(min=80, message="Wheelbase has to be more than 80 inches")], default=102.4)

    # Submit button
    submit = SubmitField("Predict Price")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20), Regexp(r"^[a-zA-Z0-9_.]*",
                                                                                                  message="Username must only contain letters, numbers, underscores and periods.")])
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=100), Regexp(r"[^@]+@[^@]+\.[^@]+", 
                                                                                            message='Invalid email address, please use a valid email address that contains an @')])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20),Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+",
                                                                                            message='Password must contain at least one uppercase letter, one lowercase letter, 1 special character and 1 numerical character.')])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords must match, please try again.")])
    submit = SubmitField("Register")

    # Validates the username
    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    # Validates the email
    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("That email has been registered. Please use a different one or login instead.")
        
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class PasswordResetRequestForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=100), Regexp(r"[^@]+@[^@]+\.[^@]+", 
                                                                                            message='Invalid email address, please use a valid email address that contains an @')])
    submitField = SubmitField("Request Password Reset")

class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=20),Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+",
                                                                                            message='Password must contain at least one uppercase letter, one lowercase letter, 1 special character and 1 numerical character.')])
    confirm_password = PasswordField("Confirm New Password", validators=[InputRequired(), EqualTo("password", message="Passwords must match, please try again.")])
    submit = SubmitField("Reset Password")