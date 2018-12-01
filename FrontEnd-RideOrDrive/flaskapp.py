from flask import Flask, render_template
import os

app = Flask(__name__)
# template_dir = os.path.abspath('FrontEnd-RideOrDrive')

@app.route('/')
def index():
    return render_template('web/index.html')

@app.route('result/')
def result():
    return "LEL"

if __name__ == '__main__':
    app.run(debug=True)