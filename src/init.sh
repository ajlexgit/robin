#!/bin/sh
echo "Creating database..."
su postgres -c "dropdb --if-exists $1; dropuser --if-exists $2"
su postgres -c "createuser $2; createdb -O $2 $1"
su postgres -c "psql --quiet -c \"ALTER USER $2 WITH password '$3'\""
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