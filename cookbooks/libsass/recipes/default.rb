#
# Cookbook Name:: libsass
# Recipe:: default
#

bash 'install-libsass' do
    user 'root'
    cwd '/tmp'
    
    code <<-EOF
        git clone https://github.com/sass/libsass
        cd ./libsass
        make && make install
    EOF
end

bash 'install-sassc' do
    user 'root'
    cwd '/tmp'
    
    code <<-EOF
        export SASS_LIBSASS_PATH=/tmp/libsass
        git clone https://github.com/sass/sassc
        cd ./sassc
        make
        cp ./bin/sassc /usr/bin/
    EOF
end