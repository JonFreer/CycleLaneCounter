## Setup

- Create a `.env` file using the `example.env` template:

      cp example.env .env

  You *will* need to fill in any missing fields, such as the OAuth scope stuff
  for both Twitter and the Vivacity API.

  For Twitter make sure your app has both read and write privileges.

- Run pip install to install the required depencencies

      pip install -r

- Install Chromium and make sure it is in the path. Chromium is used to take screenshots of the webpage. https://www.chromium.org/getting-involved/download-chromium/

## Run

We want to run this application in the background. This can be done by running the following

      nohup python3 cycle_tweeter.py &

## Stop 

In order to stop, first find the process id, and then kill the process.

    ps ax | grep cycle_tweeter.py
    kill -9 {pid}

## Pipeline

The bot executes a series of steps:
- First, it calls the vivacity API within a certain time range
- It then filters the returned json to remove None values
- It then aggregates the data in to hourly pools
- The hourly data is exported to  ```hourly.js``` along with the date of the data.
- Chromium takes a screenshot of index.html, which is a webpage displaying the graph and stats
- ```TwitterMedia``` is used to upload the screenshot returning a MediaID
- The tweet is then posted using ```Tweepy``` 

```Schedule``` is used to trigger the pipeline.
