from flask import * 
import os 
app = Flask(__name__)  

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success(): 
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, 'filename') 
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)

        return render_template("success.html", name = f.filename)  
  
if __name__ == '__main__':  
    app.run(debug = True)  