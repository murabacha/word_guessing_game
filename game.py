from flask import Flask,render_template,request,session,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from collections import defaultdict
import random

a_lot = ["ALBUM","HINGE","MONEY","SCRAP","GAMER","GLASS","SCOUR","BEING","DELVE","YIELD","METAL","TIPSY","SLUNG","FARCE","GECKO",
         "SHINE","CANNY","MIDST","BADGE","HOMER","TRAIN","STORY","HAIRY","FORGO","LARVA","TRASH","ZESTY","SHOWN","HEIST","ASKEW",
         
        "INERT","OLIVE","PLANT","OXIDE","CARGO","FOYER","FLAIR","AMPLE","CHEEK","SHAME","MINCE","CHUNK","ROYAL","SQUAD","BLACK",
        "STAIR","SCARE","FORAY","COMMA","NATAL","SHAWL","FEWER","TROPE","SNOUT","LOWLY","STOVE","SHALL","FOUND","NYMPH","EPOXY",
        "DEPOT","CHEST","PURGE","SLOSH","THEIR","RENEW","ALLOW","SAUTE","MOVIE","CATER","TEASE","SMELT","FOCUS","TODAY","WATCH",
        "LAPSE","MONTH","SWEET","HOARD","CLOTH","BRINE","AHEAD","MOURN","NASTY","RUPEE","CHOKE","CHANT","SPILL","VIVID","BLOKE",
        "TROVE","THORN","OTHER","TACIT","SWILL","DODGE","SHAKE","CAULK","AROMA","CYNIC","ROBIN","ULTRA","ULCER","PAUSE","HUMOR",
        "FRAME","ELDER","SKILL","ALOFT","PLEAT","SHARD","MOIST","THOSE","LIGHT","WRUNG","COULD","PERKY","MOUNT","WHACK","SUGAR",
        "KNOLL","CRIMP","WINCE","PRICK","ROBOT","POINT","PROXY","SHIRE","SOLAR","PANIC","TANGY","ABBEY","FAVOR","DRINK","QUERY",
        "GORGE","CRANK","SLUMP","BANAL","TIGER","SIEGE","TRUSS","BOOST","REBUS","UNIFY","TROLL","TAPIR","ASIDE","FERRY","ACUTE",
        "PICKY","WEARY","GRIPE","CRAZE","PLUCK","BRAKE","BATON","CHAMP","PEACH","USING","TRACE","VITAL","SONIC","MASSE","CONIC",
        "VIRAL","RHINO","BREAK","TRIAD","EPOCH","USHER","EXULT","GRIME","CHEAT","SOLVE","BRING","PROVE","STORE","TILDE","CLOCK",
        "WROTE","RETCH","PERCH","ROUGE","RADIO","SURER","FINER","VODKA","HERON","CHILL","GAUDY","PITHY","SMART","BADLY","ROGUE",
        "GROUP","FIXER","GROIN","DUCHY","COAST","BLURT","PULPY","ALTAR","GREAT","BRIAR","CLICK","GOUGE","WORLD","ERODE","BOOZY",
        "DOZEN","FLING","GROWL","ABYSS","STEED","ENEMA","JAUNT","COMET","TWEED","PILOT","DUTCH","BELCH","OUGHT","DOWRY","THUMB",
        "HYPER","HATCH","ALONE","MOTOR","ABACK","GUILD","KEBAB","SPEND","FJORD","ESSAY","SPRAY","SPICY","AGATE","SALAD","BASIC",
        "MOULT","CORNY","FORGE","CIVIC","ISLET","LABOR","GAMMA","LYING","AUDIT","ROUND","LOOPY","LUSTY","GOLEM","GONER","GREET",
        "START","LAPEL","BIOME","PARRY","SHRUB","FRONT","WOOER","TOTEM","FLICK","DELTA","BLEED","ARGUE","SWIRL","ERROR","AGREE",
        "OFFAL","FLUME","CRASS","PANEL","STOUT","BRIBE","DRAIN","YEARN","PRINT","SEEDY","IVORY","BELLY","STAND","FIRST","FORTH",
        "BOOBY","FLESH","UNMET","LINEN","MAXIM","POUND","MIMIC","SPIKE","CLUCK","CRATE","DIGIT","REPAY","SOWER","CRAZY","ADOBE",
        "OUTDO","TRAWL","WHELP","UNFED","PAPER","STAFF","CROAK","HELIX","FLOSS","PRIDE","BATTY","REACT","MARRY","ABASE","COLON",
        "STOOL","CRUST","FRESH","DEATH","MAJOR","FEIGN","ABATE","BENCH","QUIET","GRADE","STINK","KARMA","MODEL","DWARF","HEATH",
        "SERVE","NAVAL","EVADE","FOCAL","BLUSH","AWAKE","HUMPH","SISSY","REBUT","CIGAR"]

#computer_input = random.choice(a_lot)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
computer_input = random.choice(a_lot)
class UserInputForm(FlaskForm):
    text = StringField('enter your 5 letter word', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    global computer_input
    if request.args.get('reset') == '1':
        session.clear()
        computer_input = random.choice(a_lot)
        return redirect(url_for('index'))
    
    winning_points = 0
    attempt = session.get('attempt', 1)
    user_inputs = session.get('user_inputs', {})
    correct_letter = []
    temp_user_input = []
    letters = defaultdict(int)
    for i in computer_input:
            letters[i] += 1
   
    form = UserInputForm()
    if form.validate_on_submit():
        user_input = form.text.data.upper()
        form.text.data = ''
        
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
    if not temp_user_input == []:
        user_inputs[str(attempt)] = temp_user_input
        attempt += 1
    temp_user_input = []
    correct_letter = []
    
    letters = defaultdict(int)
    for i in computer_input:
            letters[i] += 1
    session['attempt'] = attempt
    session['user_inputs'] = user_inputs
    if winning_points == 5:
        return render_template('index.html',user_inputs=session.get('user_inputs'),answer=computer_input,message='you won',try_again=True)
    
    
    if attempt == 7:
        return render_template('index.html',user_inputs=session.get('user_inputs'),answer=computer_input,try_again=True,message='you lost')
    
    return render_template('index.html', form=form, user_inputs=session.get('user_inputs'), attempts=(7-attempt),computer_input=computer_input)


if __name__ == '__main__':
    app.run(debug=True)