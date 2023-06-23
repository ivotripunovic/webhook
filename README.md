# Webhook
Webhook to pull and run flask app on production server 


## Process
    - ssh into production,
    - stops flask app
    - pull new code from master
    - pip install -r requirements.txt
    - restart supervisor with gunicorn and flask app


## Requirements
- python 3.7
- Gunicorn 19.x
- Supervisor 3.x
- Nginx 1.14+



## Files
- webhook.py: the main application. Does the commands when the URL is requested.
- requirements.txt: all the modules needed by the app to run

## Setup
Clone repo and that's it.


# Gunicorn
Gunicorn is used to provide the layer/connection between the Flask app and Nginx

- Make sure the gunicorn script in .venv/bin/gunicorn is executable by the
  webhooks user.

## Setup
Gunicorn should be installed using a python virtual environment.
- Follow instructions like this to install python36u from the ius yum repo
    - https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7
- change to the Flask app directory
    - Create a virtual environment in the Flask app directory
    - `python3.9 -m venv .venv` (the .venv can be any name)
- Activate the virtual environment
    - `source .venv/bin/activate`
- Install modules
    - `pip install -r requirements`

# Supervisor
Supervisor is a service that keeps Gunicorn running, even with system reboots

## Setup
See the documentation for webhook in Confluence for installing supervisor and config files.

- create a program config file at /etc/supervisord.d/webhooks.config
- 
    ```
      [program:webhooks]
    directory=/var/www/webhook.pufna.com
    chdir=/var/www/webhook.pufna.com
    command=/var/www/webhook.pufna.com/.venv/bin/gunicorn --log-level debug --bind 127.0.0.1:5050 webhooks:application --error-logfile '-' --timeout 240 --workers 1
    user=webhooks
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/supervisor/webhook.pufna.com.err.log
    stdout_logfile=/var/log/supervisor/webhook.pufna.com.out.log
    log_stderr=true
    logfile=/var/log/supervisor/webhook.pufna.com.log
    redirect_sterr=True
    ```

# Nginx
Nginx is the reverse proxy. It takes the initial request for the domain name, then passes it to Gunicorn.


- Create a new nginx config file
  - Make a new file at `/etc/nginx/conf.d/webhook.pufna.com.conf`
  ```
  server {
  listen 80;
  server_name webhook.pufna.com.;

  root /var/www/webhook.pufna.com.;
  index index.html;

  access_log /var/log/nginx/webhook.pufna.com.access.log;
  error_log /var/log/nginx/webhook.pufna.com.error.log;

  }
  ```
- Test and reload Nginx
  - `sudo service nginx configtest` To double check everything is good.
  - `sudo service nginx reload`
- Once all changes are made and tested by hand to work (run the update script
  manually), then restart supervisord
  - `sudo supervisorctl restart webhooks`
- Back on webhook, run certbot to generate the SSL certs
  - `sudo certbot-auto --nginx`
- Add the webhook to the GitHub repo. On the GitHub webiste, go to the repo,
  then Settings->Webhooks->Add webhook button.
  - Payload URL = http://webhook.pufna.com/DOMAIN_NAME (DOMAIN_NAME is
    the same as what you used in the webhook.py file for the route name)
  - Content Type = application/json
  - Secret
  - Just the push event
  - Active box checked
