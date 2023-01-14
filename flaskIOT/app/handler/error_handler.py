from flask import Blueprint, request, redirect, session

handler_blueprint = Blueprint('error', __name__)

@handler_blueprint.app_errorhandler(Exception)
def handler(error):
    session['last_url'] = request.url
    print(f"Warning! An error occured in: {request.url}<br>" + str(error))
    return redirect('http://127.0.0.1:5000/db')