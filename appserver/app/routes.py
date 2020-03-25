from app import app
from flask import render_template
from flask import Flask, flash, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from .objectdetection import copyImageToStorage, ObjectDetection
import json


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getParams(params):
    paramsD = params.to_dict(flat=False)
    data = {}
    if "messages" in paramsD:       
        eData= eval(paramsD["messages"][0])
        data = {"imginfo": "/img/outImages/" + eData["imginfo"].split("/")[-1]}
    return data

@app.route('/')
@app.route('/index')
def index():
    print("[ARG]",type(request.args),request.args)
    data = getParams(request.args)
    print("[DATA]",data)
    return render_template('index.html', data=data)


@app.route('/uploadpost', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            print("filename:",filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)

            copyImageToStorage(fullpath, app.config["STORAGE_PATH"])
            od = ObjectDetection()
            outfile, labels = od.process(app.config["STORAGE_PATH"] + filename)
            url_file = app.config["STORAGE_PATH_OUT"]+filename
            flash('Ubicación en el storage: '+url_file.replace("gs://","https://storage.cloud.google.com/"))
            flash('Objetos detectados en la imagen: ' + ", ".join(labels))
            messages = json.dumps({"imginfo":url_file})
            copyImageToStorage(fullpath.replace("inImages","outImages"), url_file)
            return redirect(url_for('.index', messages=messages))
        else:
            flash('Allowed file types are: png, jpg, jpeg, gif')
            return redirect('/')
    return "subido!"


#$ curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/bicileta.jpg", "outputImage":"gs://image-pool-falabella-test-out/bicileta.jpg"}' http://127.0.0.1:5000/falabella/api/v1.0/detectobjects
@app.route('/falabella/api/v1.0/detectobjects', methods=['POST'])
def create_task():
    if not request.json or not 'inputImage' in request.json or not 'outputImage' in request.json:
        resp = {
            "msg":"Make sure your are providing the 'inputImage' and 'outputImage' parameters"
        }
    else:
        data = request.json
        
        try:
            od = ObjectDetection()
            filename = data["inputImage"].split("/")[-1]
            outfile, labels = od.process(data["inputImage"])
            url_file = data["outputImage"]
            copyImageToStorage(outfile, url_file)
            
            resp = {
                "msg":"Objetos detectados en la imagen:" + ", ".join(labels),
                "bucket_output:": url_file.replace("gs://","https://storage.cloud.google.com/")
            }
        except Exception as e:
            return jsonify({'msg': 'Error, make sure you are specifiying an input image from a public bucket. Internal error:'+str(e)})
        
    return jsonify(resp)
