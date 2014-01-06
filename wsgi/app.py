import os
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def main():
	images=os.listdir(os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'pics'))
	print images
	return render_template('main.html', images=images)

if __name__ == "__main__":
	app.config['PROPAGATE_EXCEPTIONS'] = True
	app.debug=True
	app.run()
