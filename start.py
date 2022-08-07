import time

from flask import Flask, render_template, request, flash, redirect, url_for, make_response
import os
from PIL import Image
from main import final

app = Flask(__name__)
#bootstrap = Bootstrap(app)
UPLOAD_FOLDER = 'static/img_in'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'random string'
@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form['button']=="上传图片":
            info=None
            error=None
            # check if the post request has the file part
            if 'file' not in request.files:
                info='No Picture Upload'
                return render_template("upload.html",info=info,error=None,second=None)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                info='No file choosed'
                return render_template("upload.html",info=info,error=None,second=None)
            if file and allowed_file(file.filename):
                path=os.path.join(app.config['UPLOAD_FOLDER'],'in.jpg')
                file.save(path)
                flag=True
                info="Success!"
                return render_template("upload.html",info=info,filename='in.jpg',error=info,second=None,val1=time.time())
            else:
                info='The type is not right.Please upload jpg. or jpeg. or png.'
                return render_template("upload.html",info=info,error=None,second=None)
        if request.form['button']=="运行":
            type_pic=request.form['kind']
            final(type_pic)
            info="Success!"
            return render_template("upload.html",info=info,error=info,filename='in.jpg',second='qq',val1=time.time(),val2=time.time())
    return  render_template("upload.html",error=None,filename=" ",second=None)


@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(404)
def demo1(error):
    return '您访问的页面已经去浪迹天涯了'

@app.errorhandler(500)
def demo2(error):
    return '''
    <html>
    <body>
    <h1>抱歉，您所传输的格式不对或您忘了传图片哦</h1>
    <h3>接收的图片格式为'jpg', 'png','jpeg'</h3>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=2022,debug=True)