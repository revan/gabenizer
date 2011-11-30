Flask on OpenShift Express
============================

This git repository helps you get up and running quickly w/ a Flask installation
on OpenShift Express.


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a wsgi-3.2 application

    rhc-create-app -a flask -t wsgi-3.2

Add this upstream flask repo

    cd flask
    git remote add upstream -m master git://github.com/openshift/flask-example.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://flask-$yournamespace.rhcloud.com

