#
# Cookbook Name:: requirements
# Recipe:: default
#

execute "pip3 install setuptools==25.1.2"
execute "pip3 install --upgrade -r /vagrant/requirements/common.txt"
