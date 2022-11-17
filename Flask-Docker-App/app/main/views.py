from flask import Flask

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return '<h1> Flask + Docker </h1>'

@main.route('/xyza', methods=['GET', 'POST'])
def aaa():
    return '<h1> Flask + Docker </h1>'