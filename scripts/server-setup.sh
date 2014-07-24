#!/bin/bash

# Copyright 2013 Ricardo Tubio-Pardavila (rtpardavila@gmail.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################################
# Autor: rtpardavila[at]gmail.com
# Autor: xabicrespog[at]gmail.com
# Description: configures a Debian server for the SATNet project.
################################################################################

# mysql-server, admin password: _805Mysql
# phpmyadmin user:password for database: phpmyadmin:_805Phpmyadmin

install_packages()
{

    apt-get update
    apt-get dist-upgrade

    apt-get install apache2
    apt-get install libapache2-mod-wsgi libapache2-mod-gnutls
    apt-get install mysql-server libmysqlclient-dev phpmyadmin
    apt-get install python python-virtualenv python-pip python-dev
    apt-get install python-mysqldb 
    apt-get install binutils libproj-dev gdal-bin

    apt-get clean

    pip install virtualenvwrapper

}

APACHE_2_CERTIFICATES_DIR='/etc/apache2/certificates'
CERTIFICATE_NAME='marajota.calpoly.edu'
KEY_NAME='marajota.calpoly.edu'

# ### This function creates a new self signed certificate and key to be used by
# the Apache2 server and installs them in the correct directory.
create_self_signed_cert()
{
    # 1: Generate a Private Key
    openssl genrsa -des3 -out s.key 1024
    # 2: Generate a CSR (Certificate Signing Request) 
    openssl req -new -key s.key -out s.csr
    # 3: Remove Passphrase from Key 
    cp s.key s.key.org
    openssl rsa -in s.key.org -out s.key
    # 4: Generating a Self-Signed Certificate 
    openssl x509 -req -days 365 -in s.csr -signkey s.key -out s.crt
    
    # 5: Certificates installation
    if [[ ! -d $APACHE_2_CERTIFICATES_DIR ]]
    then
        mkdir -p $APACHE_2_CERTIFICATES_DIR
    fi
    
    mv -f s.crt "$APACHE_2_CERTIFICATES_DIR/$CERTIFICATE_NAME.crt"
    mv -f s.key "$APACHE_2_CERTIFICATES_DIR/$KEY_NAME.key"
}

# ### This function configures the apache2 server.
configure_apache()
{
    a2enmod gnutls
    
    service apache2 reload
}

configure_mysql()
{

    echo "GRANT USAGE ON *.* TO '$django_user'@'localhost' IDENTIFIED BY '$django_user_password';" \
        > $__mysql_batch
    #echo "CREATE USER '$django_user'@'localhost' IDENTIFIED BY '$django_user_password';" \
    #    > $__mysql_batch
    # To run unittest
    # echo "GRANT ALL PRIVILEGES ON *.* TO '$django_user'@'localhost';" \
    #>> $__mysql_batch

    echo "CREATE DATABASE $django_db;" \
        >> $__mysql_batch
    echo "GRANT all privileges ON $django_db.* TO '$django_user'@'localhost';" \
        >> $__mysql_batch

    mysql -h localhost -u root -p < $__mysql_batch

    python $manage_py syncdb

}

delete_mysql_db()
{

    echo "DROP USER '$django_user'@'localhost';" \
        > $__mysql_batch
    echo "DROP DATABASE IF EXISTS $django_db;" \
        >> $__mysql_batch

    mysql -h localhost -u root -p < $__mysql_batch

}

configure_apache()
{
    a2ensite satnet
    a2enmod ssl
    /etc/init.d/apache2 restart
}

# ### Method that configures a given root with the virtualenvirment required,
# all the pip packages and the directories.
configure_root()
{
    mkdir -p logs
    mkdir -p public_html/static
    
    virtualenv .venv
    source $venv_activate && echo 'VENV_ACTIVATED!!!!'
    pip install -r "$project_path/scripts/requirements.txt"
}

# ### Method that configures a Python virtual environment 
create_virtualenv()
{

    virtualenv "$project_path/$venv"

    # ### starts virtual environment
    # the virtual environment must be activated before installing the required
    # packages since these should now be installed in the local directories
    # hierarchy within the created environment
    source $venv_activate && echo 'VENV_ACTIVATED!!!!'

    pip install distribute --upgrade

    pip install django
    pip install rpc4django
    pip install pytz
    pip install eventlog
    pip install django-jsonfield
    pip install django-registration
    pip install mysql-python
    pip install django_countries
    pip install django-passwords
    pip install django-jquery
    pip install django-session-security
    pip install django-jsonview
    pip install django-leaflet
    pip install python-dateutil
    pip install django-extensions
    pip install pyephem
    # ### testing packages
    pip install datadiff
    pip install django-periodically
    pip install django-allauth

    # ### TODO make it relocatable...
    # ### rellocatable virtual environment: --relocatable
    # virtualenv --relocatable $venv

}

# ### This function upgrades all the pip packages installed in the
# virtual environment
pip_upgrade_packages()
{
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
}


# ### This is the function utilized for adding the crontab task required by
# django-periodically for executing periodic maintenance tasks of the web
# applications
add_crontab_django_periodically()
{
    echo 'Adding crontab task for django-periodically...'
    crontab_task=$( "*/5 * * * * python $MANAGE_PY runtasks" )
    echo '#!/bin/sh' > $__crontab_conf
    echo "source $venv_activate" >> $__crontab_conf
    echo "python $MANAGE_PY runtasks" >> $__crontab_conf
    chmod +x $__crontab_conf
}

node_js_root_dir='/opt'

# ### This function installs bower together with Node.js, the vanilla version
# that can be downloaded from GitHub.
install_bower()
{
    apt-get install python g++ make checkinstall
    cd $node_js_root_dir
    wget -N http://nodejs.org/dist/node-latest.tar.gz
    tar xzvf node-latest.tar.gz && cd node-v*
    ./configure
    # ### IMPORTANT
    echo 'In the next menu that will be prompted, the <v> letter from the'
    echo 'version number must be erased. For doing that, select <Choice 3>'
    echo 'and erase the <v> letter leaving the rest of the version number'
    echo 'intact.'
    checkinstall -D
    dpkg -i node_*
    npm install -g bower
}

venv_wrapper_config='/usr/local/bin/virtualenvwrapper.sh'
bashrc_file="$HOME/.bashrc"
venv_workon="$HOME/.virtualenvs"
venv_projects="$HOME/repositories/satnet-release-1/WebServices"

# ### Configures an environment for using the virtualenvironment wrapper. This 
# is the full configuration, which might not be required in all cases.

configure_virtualenvwrapper()
{

    echo -e "\n# ### Virtualenv Wrapper" >> $bashrc_file
    echo "export WORKON_HOME=$venv_workon" >> $bashrc_file
    echo "export PROJECT_HOME=$venv_projects" >>  $bashrc_file
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> $bashrc_file

    bash
    
}

# ### Configures a given directory with the initial PINAX website template that
# uses django-user-accounts for user login and registration. It installs all
# the dependencies of the PINAX project through python-pip

pinax_template_url='https://github.com/pinax/pinax-project-account/zipball/master'
satnet_web_services_dir='WebServices'
    
configure_pinax_repository()
{

    django-admin.py startproject\
        --template=$pinax_template_url $satnet_web_services_dir
    cd $satnet_web_services_dir
    sudo pip install -r "$project_path/scripts/requirements.txt"

}

# ### Examples of HOW TO call this script

usage() { 

    echo "Please, use ONLY ONE ARGUMENT at a time:"
    echo "Usage: $0 [-b] #Install Node.js and Bower (from GitHub)"
    echo "Usage: $0 [-c] #Create and install self-signed certificates" 
    echo "Usage: $0 [-m] #Configures Django database" 
    echo "Usage: $0 [-d] #Delete Django databases" 
    echo "Usage: $0 [-i] #Install required packages <root>" 
    echo "Usage: $0 [-v] #Configure virtualenv" 

    1>&2;
    exit 1; 

}

################################################################################
# ### Main variables and parameters

__mysql_batch='/tmp/__mysql_batch'
__crontab_conf='/etc/cron.daily/satnet_periodically'

django_user='satnet_django'
django_user_password='_805Django'
django_db='satnet_db'

project_path="$( cd "$( dirname "$0" )" && pwd )"
project_path=$project_path"/.."
manage_py="$project_path/WebServices/manage.py"
venv='.venv'
venv_activate="$project_path/$venv/bin/activate"

################################################################################
# ### Main execution loop

if [ $# -lt 1 ] ; then
    usage
    exit 0
fi

while getopts ":bcdimv" opt; do
    case $opt in
        b)
            #Need to be root to install packages
            [[ $( whoami ) == 'root' ]] || \
                { echo 'Need to be <root>, exiting...'; exit -1; }

            echo 'Installing Bower and Node.js...'
            install_bower
            echo 'DONE'
            exit 1
            ;;
        c)
            echo 'Creating self-signed certificates...'
            create_self_signed_cert
            echo 'DONE'
            exit 1;
            ;;
        d)
            echo 'Deleting MYSQL Django databases...'
            delete_mysql_db
            echo 'DONE'
            exit 1;
            ;;
        i)
            #Need to be root to install packages
            [[ $( whoami ) == 'root' ]] || \
                { echo 'Need to be <root>, exiting...'; exit -1; }

            echo 'Installing required packages...'
            echo 'This process is not unattended, user interaction is required.'
            echo 'Press any key to continue...'
            read
            install_packages
            echo 'DONE'
            ;;
         m)
            echo 'Configuring MySQL...'
            configure_mysql
            add_crontab_django_periodically
            echo 'DONE'
            exit 1
            ;;
        v)
            echo 'Configuring virtualenv...'
            configure_root
            echo 'DONE'
            exit 1;
            ;;
        *)
            usage
            ;;
    esac
    
    shift $((OPTIND-1))

done

exit 1
