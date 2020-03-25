from flask import Flask

#
#  export GOOGLE_APPLICATION_CREDENTIALS="/home/hrosmendez/falabella-sa-credentials.json"
#  export GOOGLE_APPLICATION_CREDENTIALS="/home/henry/Falabella/docker/falabella-sa-credentials.json"
#  export FLASK_APP=appserver.py
#  flask run

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

print(app.template_folder)
from app import routes

app.run(debug=True)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = '/var/www/appserver/app/static/img/inImages/'
#app.config['UPLOAD_FOLDER'] = '/home/henry/Falabella/docker/appserver/app/static/img/inImages/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['STORAGE_PATH'] = 'gs://image-pool-falabella-test/'
app.config['STORAGE_PATH_OUT'] = 'gs://image-pool-falabella-test-out/'
