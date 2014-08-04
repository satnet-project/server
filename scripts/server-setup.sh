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

# ### Installs the packages necessary for the Debian operating system.
install_packages()
{

    apt-get update
    apt-get dist-upgrade

    apt-get install apache2
    apt-get install libapache2-mod-wsgi libapache2-mod-gnutls
    apt-get install postgresql postgresql-contrib phppgadmin
    apt-get install postgresql-server-all
    apt-get install python python-virtualenv python-pip python-dev
    apt-get install binutils libproj-dev gdal-bin
    apt-get install build-essential libssl-dev libffi-dev

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

# ### This function configures the operating system with the required users,
# permissions and directories necessary.
__username=''
configure_os()
{
    usermod -aG adm $__username
}


# ### This function configures the apache2 server.
configure_apache()
{
    a2enmod gnutls
    service apache2 reload
}

__pgsql_batch='/tmp/__pgsql_batch'
__pgsql_user='postgres'
__pgsql_password='pg805sql'     # Must be entered manually (interactive mode).
__phppgadmin_config_file='/etc/phppgadmin/config.inc.php'
django_db='satnet_db'
django_user='satnet_django'
django_user_password='_805Django'
# ### Configures a PostgreSQL server with a database for the SATNET system.
configure_postgresql()
{
    
    # ### Uncomment the following lines if you want to reset default user's
    # password.
    #echo 'User <postgres> grants access through <phppgadmin>'
    #echo 'Configure password for user <postgres>.'
    #echo "\password postgres" > $__pgsql_batch
    #sudo -u postgres psql -f $__pgsql_batch

    sudo -u postgres createdb $django_db
    echo "User <$django_user> is about to be created, insert password..."
    sudo -u postgres createuser -r -l -S -E -P -d $django_user
    
    #echo "CREATE USER $django_user PASSWORD $django_user_password" > $__pgsql_batch
    echo "GRANT ALL PRIVILEGES ON DATABASE $django_db TO $django_user;" > $__pgsql_batch
    sudo -u postgres psql -f $__pgsql_batch
    
    # ### Extra login security can be disabled for local access only by
    # uncommenting the following <sed> command. This permits the access to
    # <phppgadmin> by using <root> or <postgres>.
    # If this level of security is necessary and, thus, this mechanism has to
    # be enabled again, an additional user for access through <phppgadmin> has
    # to be created and configured.
    #sed -e "s/extra_login_security'] = true;/extra_login_security'] = false;/g" -i $__phppgadmin_config_file

}

# ### Deletes all the database configuration required for the SATNET system.
remove_postgresql()
{
    sudo -u postgres dropdb $django_db
    sudo -u postgres dropuser $django_user
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
    pip install psycopg2
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


__crontab_conf='/etc/cron.d/satnet'
__crontab_user='root'
__crontab_shell='/bin/bash'
__crontab_path='/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin'

# ### This is the function utilized for adding the crontab task required by
# django-periodically for executing periodic maintenance tasks of the web
# applications
configure_crontab()
{
    __django_runtasks="python $webservices_manage_py runtasks"
    __crontab_command="source $webservices_venv_activate && $__django_runtasks"
    __crontab_task="30 23 * * * $__crontab_user $__crontab_command"

    echo 'Adding crontab task for django-periodically...' > $__crontab_conf
    echo "SHELL=$__crontab_shell" >> $__crontab_conf
    echo "PATH=$__crontab_path" >> $__crontab_conf
    echo "$__crontab_task" >> $__crontab_conf
    #chmod +x $__crontab_conf
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
    echo "Usage: $0 [-p] #Configures PostgreSQL" 
    echo "Usage: $0 [-r] #Removes specific PostgreSQL configuration for SATNET." 
    echo "Usage: $0 [-o] #Configures Crontab for django-periodically"
    echo "Usage: $0 [-i] #Install required packages <root>" 
    echo "Usage: $0 [-v] #Configure virtualenv" 

    1>&2;
    exit 1; 

}

################################################################################
# ### Main variables and parameters
project_path="$( cd "$( dirname "$0" )" && pwd )"
webservices_dir="$project_path/WebServices"
webservices_venv_dir="$webservices_dir/.venv"
webservices_venv_activate="$webservices_venv_dir/bin/activate"
webservices_manage_py="$webservices_dir/manage.py"
project_path="$project_path/.."

################################################################################
# ### Main execution loop
[[ $( whoami ) == 'root' ]] || \
    { echo 'Need to be <root>, exiting...'; exit -1; }

if [ $# -lt 1 ] ; then
    usage
    exit 0
fi

while getopts ":bciprov" opt; do
    case $opt in
        b)
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
        i)
            echo 'Installing required packages...'
            echo 'This process is not unattended, user interaction is required.'
            echo 'Press any key to continue...'
            read
            install_packages
            echo 'DONE'
            ;;
        p)
            echo 'Configuring PostgreSQL...'
            configure_postgresql
            echo 'DONE'
            exit 1
            ;;
        r)
            echo 'Removing PostgreSQL...'
            remove_postgresql
            echo 'DONE'
            exit 1;
            ;;
        o)
            echo 'Configuring Crontab...'
            configure_crontab
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
