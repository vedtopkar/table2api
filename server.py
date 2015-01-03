from flask import Flask, request, render_template
from flask import Flask, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
                                UserMixin, RoleMixin, login_required
import os
import pandas as pd

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'cool_beans'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
  return 'Welcome to Table2API! Create a new API from an excel file <a href="/new">here</a>'

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return 'Register here'
  elif request.method == 'POST':
    return 'Create new user'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return 'Username: <input type="text"/> Password: <input type="password"/>'
  elif request.method == 'POST':
    return 'Post method'

@app.route('/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename + ' has been uploaded. You can access a cell by visiting <b>/api/' + filename + '/{row index}/{column index}</b>'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/new" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/<filename>/<int:row>/<int:column>', methods=['GET'])
def access_cell(filename, row, column):
  df = pd.read_excel('uploads/' + filename, header=None)
  try:
    return str(df.iloc[row-1, column-1])
  except:
    return 'Index out of bounds'

if __name__ == "__main__":
  app.run(debug=True)
