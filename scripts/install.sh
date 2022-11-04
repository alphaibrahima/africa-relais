#!/usr/bin/env bash
echo "***********************************************"
echo "***************** install *********************"
echo "***********************************************"

echo "***********************************************"
echo "---apt update e upgrade---"
echo "***********************************************"
apt-get -y update

echo "***********************************************"
echo "---OS dependencies---"
echo "***********************************************"
apt-get -y install python3-pip
apt-get -y install python3-dev python3-setuptools
apt-get -y install git
apt-get -y install supervisor
apt-get -y install virtualenv
# apt-get -y install pipenv

# .....
# .....
# .....
# .....

echo "***********************************************"
echo "---install dependencies (including django)  ---"
echo "***********************************************"
pip3 install --upgrade pip
pip3 install requests
# activate env
pip3 install -r requirements.txt
echo "***********************************************"
echo "--- Running the app  ---"
echo "***********************************************"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
