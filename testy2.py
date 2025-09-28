from flask import Flask,session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
def index():
   if 'visits' not in session:
      session['visits'] = 0
   session['visits'] += 1
   return 'Number of visits: %s' % session['visits']

if __name__ == '__main__':
   app.run(debug=True)