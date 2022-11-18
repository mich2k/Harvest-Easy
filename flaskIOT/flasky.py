#sample1
# first example
# see https://flask.palletsprojects.com/en/1.1.x/

from flask import Flask

#creo applicazione
appname = "IOT - SmartBin"
app = Flask(appname)

@app.route('/') 
def testoHTML():
    return '<h1>Smart Bin</h1>'

if __name__ == '__main__':
    app.run() 