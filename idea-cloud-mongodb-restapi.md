
I talked with Steve from OpenShift (RedHat) on how we could solve the problem of the local queries timing out with a cloud based file or database.

Here's his reply --

They can certainly query against a cloud based file but a Flask or Bottle API would be much more freedom in the future. In this way they can ditch the file at some point and go to a DB but the API consumers would never know.

In OpenShift I would tell them to make a cron job that queries pub med and throws teh data into a data store, mongoDB or Postgresql or MySQL.

Then put a bottle or flask (or django if they are already using it) REST API in front of the DB to let people query out the data any way they want.

here is a little example where I take a flat JSON file, push it into Mongo, and then use Flask to create an API

https://github.com/openshift/openshift-mongo-flask-example

I will be at the pyramid session tomorrow.