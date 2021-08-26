#!/usr/bin/env bash
# 0. Prepare your web servers

# Install Nginx
if ! command -v nginx &> /dev/null
then
  sudo apt-get -y update
  sudo apt-get --yes install nginx
fi

# create folders
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# permissions
sudo chown -R ubuntu /data/
sudo chmod -R 755 /data/

# Creating html file
touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# create symbolic link
ln -s -f /data/web_static/releases/test/ /data/web_static/current

#  Nginx configuration to serve the content
sudo sed -i '/server_name _;/a location /hbnb_static {\n\talias /data/web_static/current/;\n}' /etc/nginx/sites-enabled/default

# restart
sudo service nginx restart
