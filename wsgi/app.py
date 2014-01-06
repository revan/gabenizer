import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html', images=listdir(os.path.join(
		os.environ['OPENSHIFT_DATA_DIR']
		,'pics')))

if __name__ == "__main__":
    app.run()
