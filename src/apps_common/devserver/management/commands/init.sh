#!/bin/sh
echo "Creating database..."
su postgres -c "dropdb --if-exists project; dropuser --if-exists project"
su postgres -c "createuser project; createdb -O project project"
su postgres -c "psql --quiet -c \"ALTER USER project WITH password 'password'\""
echo "OK\n"

echo "Fix pip..."
wget --quiet https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm -f get-pip.py
echo "OK\n"

echo "alias py=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc
echo "alias pm=\"python3 manage.py\"" >> ~/.bashrc

echo "Install IPython..."
pip3 --quiet install ipython
echo "OK\n"