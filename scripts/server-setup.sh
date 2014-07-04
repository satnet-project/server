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

    apt-get install apache2 phpmyadmin
    apt-get install mysql-server libmysqlclient-dev
    apt-get install python python-virtualenv python-pip python-dev python-mysqldb 
    apt-get install binutils libproj-dev gdal-bin

    apt-get clean

    pip install virtualenvwrapper

}

configure_mysql()
{

    echo "GRANT USAGE ON *.* TO '$django_user'@'localhost' IDENTIFIED BY '$django_user_password';" \
        > $__mysql_batch
    #echo "CREATE USER '$django_user'@'localhost' IDENTIFIED BY '$django_user_password';" \
    #    > $__mysql_batch
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

# ### Method that configures a Python virtual environment 

create_virtualenv()
{

    virtualenv "$project_path/$venv"

    # ### starts virtual environment
    # the virtual environment must be activated before installing the required
    # packages since these should now be installed in the local directories
    # hierarchy within the created environment
    source $venv_activate && echo 'VENV_ACTIVATED!!!!'

    #pip install django==1.5.2
    #pip install eventlog==0.6.2
    #pip install django-jsonfield==0.8.12
    #pip install django-registration==1.0
    #pip install mysql-python==1.2.3
    
    pip install django==1.5.4
    pip install eventlog==0.6.2
    pip install django-jsonfield==0.8.12
    pip install django-registration==1.0
    pip install mysql-python==1.2.3
    pip install rpc4django
    pip install pytz

    pip install distribute --upgrade

    pip install django
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
    pip install twisted
    pip install txJSON-RPC
    # ### testing packages
    pip install django-selenium
    pip install selenium
    pip install six
    pip install unittest-data-provider
    pip install datadiff

    pip install git+https://github.com/hzdg/django-periodically.git#egg=django-periodically

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
    #crontab_task=$( "*/5 * * * * python $MANAGE_PY runtasks" )
    echo '#!/bin/sh' > $__crontab_conf
    echo "source $venv_activate" >> $__crontab_conf
    echo "python $MANAGE_PY runtasks" >> $__crontab_conf
    chmod +x $__crontab_conf
}

# ### TODO Configuration of system dependencies by GeoDjango.

# configure_geodjango()
# {
#     
# }

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

configure_pinax_repository()
{

    pinax_template_url='https://github.com/pinax/pinax-project-account/zipball/master'
    satnet_web_services_dir='WebServices'

    django-admin.py startproject\
        --template=$pinax_template_url $satnet_web_services_dir
    cd $satnet_web_services_dir
    sudo pip install -r requirements.txt

}

# ### Examples of HOW TO call this script

usage() { 

    echo "Please, use ONLY ONE ARGUMENT at a time:"
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
venv='__v_env'
venv_activate="$project_path/$venv/bin/activate"

################################################################################
# ### Main execution loop


if [ $OPTIND -gt 1 ] ; then
    usage
fi

while getopts ":div" o; do
    case "${o}" in
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
            echo 'This process is not unattended, user interaction is required. Press any key to continue...'
            read
            #install_packages
            #add_crontab_django_periodically
            echo 'DONE'

            echo 'Configuring virtualenv...'
            create_virtualenv $*
            configure_mysql
            echo 'DONE'
            exit 1;

            ;;
        v)
            echo 'Configuring virtualenv...'
            create_virtualenv $*
            configure_mysql
            echo 'DONE'
            exit 1;
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

exit 1