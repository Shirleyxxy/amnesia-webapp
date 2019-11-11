# run the application using the flask command in development mode.
# run the command in the top-level directory, not the flaskr package.

$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run

# The default flask server listens at port 5000. We need the address of
# the machine (our local host and the port) to contact the server: 127.0.0.1:5000

# commands to list the processes running on port 5000 and kill them using PID
# in case we forgot to terminate the processes.
$ lsof -i :5000
$ kill -9 <PID>
