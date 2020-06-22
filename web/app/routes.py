from app import app
from flask import request,jsonify,abort, render_template, flash, redirect, url_for, send_from_directory
from flask_login import login_required,current_user, login_user,logout_user
from werkzeug.urls import url_parse
from . import db
from sqlalchemy.exc import IntegrityError
import json as jsn

@app.route('/index')
def show_index():
    return render_template('base.html')
