import os
from flask import Flask, render_template
app = Flask(__name__, template_folder=os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'wsgi','templates')

@app.route("/")
def main():
	print 'debug'
	try:
		images=os.listdir(os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'pics'))
		print images
		render_template('main.html', images=images)
	except:
		return 'An error has occurred.'

if __name__ == "__main__":
	app.config['PROPAGATE_EXCEPTIONS'] = True
	app.run()
