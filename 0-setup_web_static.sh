#!/usr/bin/env bash
# A script that sets up our web servers for the deployment of web_Static.

# install/configure nginx
sudo apt -y update
sudo apt -y install nginx ufw
sudo ufw allow 'Nginx HTTP'

# create required folders
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# create fake HTML file... to test nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create symbolic link, delete if already existing
ln -sf /data/web_static/releases/test/ /data/web_static/current

# change ownership/group of /data/ to ubuntu
chown -R ubuntu:ubuntu /data/

# update nginx configuration
	# error page config
echo "Ceci n'est pas une page" | sudo tee /var/www/html/error-page.html
	# nginx config file
printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served-By \$hostname always;
	root /var/www/html;
	index index.html index.htm

	rewrite ^/redirect_me http://edoka.tech permanent;
	error_page 404 /error-page.html;

	location / {
		try_files \$uri \$uri/ =404;
	}

	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
}" > /etc/nginx/sites-available/default

# restarting nginx
sudo service nginx restart

