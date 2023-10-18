import flask

app = flask.Flask(__name__)

@app.route('/')
def index(req,):#msg='defaultmessage'):
    asd[3] = 'asd'
    return f'hello {msg}'
    return 'helklo2'

app.run('0.0.0.0', debug=True)

