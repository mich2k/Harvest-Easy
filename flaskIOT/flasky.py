from flask import Flask, request
from config import Config
from app.database.database import database_blueprint,db

#creo applicazione
appname = "IOT - SmartBin"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

db.init_app(app)
app.register_blueprint(database_blueprint, url_prefix='/database')

@app.route('/') 
def testoHTML():
    return '<h1>Smart Bin</h1>'

@app.route('/esp', methods=['POST'])
def data():
    data = request.get_json()
    return 'Value: ' + data.get('temp', 'No name')

@app.route('/<string:name>&<int:id>')
def test(name, id):
    return '<h2> name:' + str(type(name)) + ' id:' + str(type(id)) + '</h2>'


#Testing
"""
if __name__ == '__main__':
    app.run('0.0.0.0',5000)
    """ 