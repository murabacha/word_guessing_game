from flask import Flask,render_template,request,session,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from collections import defaultdict

computer_input = 'ASOOP'
computer_input = computer_input.upper()
attempt = 1
winning_points = 0
user_inputs = {}
temp_user_input = []

letters = defaultdict(int)
correct_letter = []
for i in computer_input:
    letters[i] += 1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

class UserInputForm(FlaskForm):
    text = StringField('enter your 5 letter word', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Submit')


user_inputs = {

}

@app.route('/', methods=['GET', 'POST'])
def index():
    global attempt
    global user_inputs
    global computer_input
    global winning_points
    global temp_user_input
    global letters
    global correct_letter
    if request.args.get('reset') :
        attempt = 1
        user_inputs = {}
        computer_input = 'ASOOP'
        computer_input = computer_input.upper()
        winning_points = 0
        temp_user_input = []
        letters = defaultdict(int)
        correct_letter = []
        for i in computer_input:
            letters[i] += 1
        return render_template(url_for('index.html',form=UserInputForm(),user_inputs=user_inputs,attempts=(7-attempt)))
    form = UserInputForm()
    if form.validate_on_submit():
        user_input = form.text.data.upper()
        #user_inputs = evaluate(user_input)
        form.text.data = ''
        def evaluate(user_input):
            global attempt
            global temp_user_input
            global letters
            global correct_letter
            global winning_points
            for i in range(0,5):
                if user_input[i] == computer_input[i]:
                    temp_user_input.append([user_input[i],'green'])
                    correct_letter.append(i)
                    letters[user_input[i]] -= 1
                    winning_points += 1

            for i in range(0,5):
                if i in correct_letter:
                        continue
                if user_input[i] in computer_input:
                    
                    if letters[user_input[i]] > 0:
                        temp_user_input.insert(i,[user_input[i],'yellow'])
                        letters[user_input[i]] -= 1
                    elif letters[user_input[i]] <= 0 :
                        temp_user_input.insert(i,[user_input[i],'white'])
                else:
                    temp_user_input.insert(i,[user_input[i],'white'])
            user_inputs[attempt] = temp_user_input
            temp_user_input = []
            correct_letter = []
            
            attempt += 1
        evaluate(user_input)
    if attempt == 7:
        return render_template('index.html',user_inputs=user_inputs,answer=computer_input,try_again=True,message='you lost')
    if winning_points == 5:
        winning_points = 0
        return render_template('index.html',user_inputs=user_inputs,answer=computer_input,message='you won',try_again=True)
    winning_points = 0
    return render_template('index.html', form=form, user_inputs=user_inputs,attempts=(7-attempt))
if attempt == 7:
    user_inputs = {
        
    }
    attempt = 1

if winning_points == 5:
    user_inputs = {
        
    }
    attempt = 1
    winning_points = 0

if __name__ == '__main__':
    app.run(debug=True)