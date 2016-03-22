# Dockerized RequestBin
_Forked from a Runscope community project, [requestbin](https://github.com/Runscope/requestbin)_

This fork is being customized to run in a Docker container and to run in a subdirectory rather than as root. I don't anticipate that these changes would be accepted by the main RequestBin project, so there will be no pull requests from this project unless asked. Feel free to fork this project and bring the changes you like back to RequestBin if you like.

**TODO** I'm also going to add some "security" in the form of a required header and check for a required value for the header, and I will do some general cleanup to make this less project refer less to RequestBin (except to give credit for the code).

# License
MIT

## Running Locally with Docker
In the first version, you should run with only one worker and use the debug mode with in-memory bins.

**TODO** I will expand this to use a separate Redis container and so allow multiple workers.

    # edit requestbin/config.py to set configuration, then ... 
    docker build -t requestbin .
    docker run --name rbin -d -e PORT=8080 -p 9999:8080
    # Note rbin, 8080, and 9999 are just examples.

## Running on Heroku
## Deploy your own instance using Heroku
Create a Heroku account if you haven't, then grab the RequestBin source using git:

`$ git clone git://github.com/Runscope/requestbin.git`

From the project directory, create a Heroku application:

`$ heroku create`

Add Heroku's redis addon:

`$ heroku addons:add heroku-redis`

Set an environment variable to indicate production:

`$ heroku config:set REALM=prod`

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.


Contributors
------------
 * Barry Carlyon <barry@barrycarlyon.co.uk>
 * Jeff Lindsay <progrium@gmail.com>
 * Andy Rothfusz <github@devsupport.net>
