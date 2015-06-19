#!/bin/bash

################################################################################
# Copyright 2013 Ricardo Tubio-Pardavila (rtpardavila@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
# Author: rtpardavila[at]gmail.com
# Author: xabicrespog[at]gmail.com
# Description: configures a Debian server for the SATNet project.
################################################################################

etc_apt_sources='/etc/apt/sources.list'
backports='deb http://http.debian.net/debian wheezy-backports main contrib non-free'
# ### Installs the packages necessary for the Debian operating system.
install_packages()
{

    [[ $linux_dist == 'Debian' ]] && {

        yell '>>> Activating <contrib> and <non-free> repositories...'
        try sudo sed -i -e 's/ main *$/ main contrib non-free/g' $etc_apt_sources

        [[ $debian_version -eq '7' ]] && {
            echo '>>> Debian 7 detected, activating backports...'
            [[ -z $( cat $etc_apt_sources | grep 'wheezy-backports' ) ]] && {
                echo $backports | sudo tee -a $etc_apt_sources
                echo '>>> Backports activated, press any key to continue...'
            } || {
                echo '>>> Backports already activated, press any key to continue...'
            }
        }
    }

    try sudo aptitude update && sudo aptitude dist-upgrade -y
    try sudo aptitude install $( cat "$linux_packages" ) -y
    try sudo aptitude clean
    try sudo pip install virtualenvwrapper

    # ### ######################################################################
    # ### PATCHED: no longer required since JS dependencies are managed from
    # within satnet-ng project
    # [[ ! $(whihc sass)]] && try sudo gem install sass
    # [[ ! $(whihc compass)]] && try sudo gem install compass
    # ### ######################################################################

}

APACHE_2_CERTIFICATES_DIR='/etc/apache2/certificates'
#CERTIFICATE_NAME='marajota.calpoly.edu.crt'
#KEY_NAME='marajota.calpoly.edu.key'
__tmp_cert="/tmp/tmp.crt"
__tmp_csr="/tmp/tmp.csr"
__tmp_key="/tmp/tmp.key"
__original_tmp_key="/tmp/tmp.key.original"
CERTIFICATE_NAME="tmp.crt"
KEY_NAME="tmp.key"

# ### This function creates a new self signed certificate and key to be used by
# the Apache2 server and installs them in the correct directory.
create_apache_keys()
{
    # In case keys from previous installations exist, we remove them...
    sudo rm -f $__tmp_cert $__tmp_csr $__tmp_key

    # 1: Generate a Private Key
    echo '>>> STEP 1: generate privakte RSA key:'
    openssl genrsa -des3 -out $__tmp_key 1024
    # 2: Generate a CSR (Certificate Signing Request)
    echo '>>> STEP 2: Generate Signing Request:'
    openssl req -new -key $__tmp_key -out $__tmp_csr
    # 3: Remove Passphrase from Key
    echo '>>> STEP 3: Removing passphrase from key'
    mv -f $__tmp_key $__original_tmp_key
    openssl rsa -in $__original_tmp_key -out $__tmp_key
    echo '>>> STEP 4: Generating self-signed certificate without passphrase:'
    # 4: Generating a Self-Signed Certificate
    openssl x509 -req -days 365 -in $__tmp_csr -signkey $__tmp_key -out $__tmp_cert

    echo '>>> STEP 5: certificates installation:'
    # 5: Certificates installation
    [[ ! -d $APACHE_2_CERTIFICATES_DIR ]] &&\
        sudo mkdir -p $APACHE_2_CERTIFICATES_DIR
    sudo mv -f $__tmp_cert "$APACHE_2_CERTIFICATES_DIR/$CERTIFICATE_NAME"
    sudo mv -f $__tmp_key "$APACHE_2_CERTIFICATES_DIR/$KEY_NAME"
    sudo chmod -R o-w $APACHE_2_CERTIFICATES_DIR
}

__satnet_apache_ssl_conf='/etc/apache2/mods-available/ssl.conf'
__satnet_apache_conf='/etc/apache2/sites-available/satnet_tls.conf'
__apache_user='www-data'
__apache_group='www-data'
__apache_redirect_url='https://localhost:8443'
__apache_server_name='localhost'
__apache_server_admin='satnet.calpoly@gmail.com'
__apache_server_ports='/etc/apache2/ports.conf'
__apache_server_certificates_dir='/etc/apache2/certificates'
__apache_server_certificate="$__apache_server_certificates_dir/$CERTIFICATE_NAME"
__apache_server_key="$__apache_server_certificates_dir/$KEY_NAME"
__apache_rotate_logs="/usr/local/apache/bin/rotatelogs"
__phppgadmin_apache_config='/etc/apache2/conf.d/phppgadmin'
__phppgadmin_config_file='/etc/phppgadmin/config.inc.php'

# ### This function configures the apache2 server.
configure_apache()
{

    __webservices_python_env_dir="$webservices_dir/.venv/lib/python2.7/site-packages"

    [[ $branch_name == 'development_3k' ]] && {
        echo ">>> branch: development_3k"
        # virtualenv --python=python3 $webservices_venv_dir
        __webservices_python_env_dir="$webservices_dir/.venv/lib/python3.4/site-packages"
        echo ">>> __webservices_python_env_dir = $__webservices_python_env_dir"
    } || {
        echo ">>> branch: NON dev_3k"
        # virtualenv $webservices_venv_dir
    }

    # ### For Debian Jessie (8), the file configuration for PHPPGADMIN has been
    # moved to '/etc/apache2/conf-available/phppgadmin.conf'
    [[ $debian_version -eq '8' ]] && {
        echo '>>> Debian 8 detected, phppgadmin moved to conf-available...'
        __phppgadmin_apache_config='/etc/apache2/conf-available/phppgadmin.conf'
        echo ">>> phppgadmin = $__phppgadmin_apache_config"
    }

    # ### CONFIGURATION OF THE SSL MODULE
    sudo rm -f $__satnet_apache_ssl_conf
    sudo touch $__satnet_apache_ssl_conf

    echo '<IfModule mod_ssl.c>' | sudo tee $__satnet_apache_ssl_conf
    echo '    SSLRandomSeed startup builtin' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLRandomSeed startup file:/dev/urandom 512' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLRandomSeed connect builtin' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLRandomSeed connect file:/dev/urandom 512' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    AddType application/x-x509-ca-cert .crt' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    AddType application/x-pkcs7-crl .crl' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLSessionCache shmcb:${APACHE_RUN_DIR}/ssl_scache(512000)' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLSessionCacheTimeout 300' | sudo tee -a $__satnet_apache_ssl_conf
    echo "    SSLCertificateFile $__apache_server_certificate" | sudo tee -a $__satnet_apache_ssl_conf
    echo "    SSLCertificateKeyFile $__apache_server_key" | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLHonorCipherOrder On' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLCipherSuite HIGH:!aNULL:!MD5' | sudo tee -a $__satnet_apache_ssl_conf
    echo '</IfModule>' | sudo tee -a $__satnet_apache_ssl_conf

    # ### CONFIGURATION FOR THE VIRTUALHOST
    echo '<VirtualHost *:80>'  | sudo tee $__satnet_apache_conf
    echo "	ServerName $__apache_server_name" | sudo tee -a $__satnet_apache_conf
    echo "	Redirect permanent / $__apache_redirect_url" | sudo tee -a $__satnet_apache_conf
    echo '</VirtualHost>' | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo '<VirtualHost *:443>' | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo "	  ServerName $__apache_server_name" | sudo tee -a $__satnet_apache_conf
    echo "    ServerAdmin $__apache_server_admin" | sudo tee -a $__satnet_apache_conf
    echo "	  DocumentRoot $webservices_static_dir" | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo "    Alias /favicon.ico $webservices_public_html_dir/favicon.ico" | sudo tee -a $__satnet_apache_conf
    echo "    Alias /static $webservices_static_dir" | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo '    SSLEngine On' | sudo tee -a $__satnet_apache_conf
    #echo '    GnuTLSEnable on' | sudo tee -a $__satnet_apache_conf
    #echo '    GnuTLSPriorities NORMAL:!DHE-RSA:!DHE-DSS:!AES-256-CBC:%COMPAT' | sudo tee -a $__satnet_apache_conf
    #echo "    GnuTLSCertificateFile $__apache_server_certificate" | sudo tee -a $__satnet_apache_conf
    #echo "    GnuTLSKeyFile $__apache_server_key" | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo "    WSGIScriptAlias / $webservices_dir/website/wsgi.py" | sudo tee -a $__satnet_apache_conf
    echo "    WSGIDaemonProcess satnet python-path=$webservices_dir:$__webservices_python_env_dir" | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo "    <Directory $webservices_dir/>" | sudo tee -a $__satnet_apache_conf
    echo "        WSGIProcessGroup satnet" | sudo tee -a $__satnet_apache_conf
    echo '	      <IfVersion < 2.3 >' | sudo tee -a $__satnet_apache_conf
    echo '        	Order deny,allow' | sudo tee -a $__satnet_apache_conf
    echo '        	Allow from all' | sudo tee -a $__satnet_apache_conf
    echo '	      </IfVersion>' | sudo tee -a $__satnet_apache_conf
    echo '	      <IfVersion >= 2.3>' | sudo tee -a $__satnet_apache_conf
    echo '		    Require all granted' | sudo tee -a $__satnet_apache_conf
    echo '	      </IfVersion>' | sudo tee -a $__satnet_apache_conf
    echo '    </Directory>' | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
# "||/usr/local/apache/bin/rotatelogs /var/log/access_log 86400"
    echo "    CustomLog $webservices_logs_dir/access.log combined" | sudo tee -a $__satnet_apache_conf
    echo "    CustomLog $webservices_logs_dir/ssl_request.log \"%t %h %{SSL_PROTOCOL}s %{SSL_CIPHER}s \\\"%r\\\" %b\"" | sudo tee -a $__satnet_apache_conf
    echo "    ErrorLog $webservices_logs_dir/error.log" | sudo tee -a $__satnet_apache_conf
    echo '' | sudo tee -a $__satnet_apache_conf
    echo '</VirtualHost>' | sudo tee -a $__satnet_apache_conf

    sudo sed -i -e 's/allow from 127/# allow from 127/g' -e 's/# allow from all/allow from all/g' $__phppgadmin_apache_config
    # ### Extra login security can be disabled for local access only by
    # uncommenting the following <sed> command. This permits the access to
    # <phppgadmin> by using <root> or <postgres>.
    # If this level of security is necessary and, thus, this mechanism has to
    # be enabled again, an additional user for access through <phppgadmin> has
    # to be created and configured.
    # sudo sed -i -e "s/extra_login_security'] = true;/extra_login_security'] = false;/g" $__phppgadmin_config_file

    # default 80 ports are disabled (SSL access only!)
    # sudo sed -i -e 's/^NameVirtualHost \*\:80/# NameVirtualHost \*\:80/g' -e 's/^Listen 80/# Listen 80/g' $__apache_server_ports

    create_apache_keys

    [[ $debian_version -eq '7' ]] && {
        sudo a2dismod gnutls # gnutls for apache not included in Jessie
    }

    sudo a2enmod wsgi
    sudo a2enmod ssl
    sudo a2enmod headers            # For enabling CORS
    sudo a2ensite satnet_tls        # ubuntu compatible
    sudo a2ensite satnet_tls.conf   # debian compatible
    sudo a2dissite 000-default
    sudo a2dissite default
    sudo a2dissite default-ssl
    sudo service apache2 reload
}

__pgsql_batch='/tmp/__pgsql_batch'
__pgsql_user='postgres'
django_db='satnet_db'
django_db_user='satnet'
# ### Configures a PostgreSQL server with a database for the SATNET system.
configure_postgresql()
{

    # ### Uncomment the following lines if you want to reset default user's
    # password.
    #echo 'User <postgres> grants access through <phppgadmin>'
    #echo 'Configure password for user <postgres>.'
    #echo "\password postgres" > $__pgsql_batch
    #sudo -u postgres psql -f $__pgsql_batch

    # ### 1) Create database:

    [[ ! $( sudo -u postgres psql -l | grep $django_db | wc -l ) -eq 0 ]] && {
        echo ">>>> Database db = $django_db already exists, removing..."
        try sudo -u postgres dropdb $django_db
    }

    echo ">>>> Creating postgres database, name = <$django_db>"
    try sudo -u postgres createdb $django_db

    # ### 2) Create user for accessing the database:

    [[ $( sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$django_db_user'" ) -eq 1 ]] && {
        echo ">>>> Postgres user = <$django_db_user> already exists, removing..."
        try sudo -u postgres dropuser $django_db_user
    }

    echo ">>>> Creating postgres user = <$django_db_user>"

    # ### ##################################################################
    # ### PATCH: originally the next command was executed as shown in the line below, with a password prompt
    # sudo -u postgres createuser -r -l -S -E -P -d $django_db_user
    try sudo -u postgres createuser -r -l -S -E -d $django_db_user
    try ask_password
    django_db_password=$__PASSWORD
    # ### ##################################################################

    try sudo -u postgres psql -U postgres -d postgres -c "alter user $django_db_user with password '$__PASSWORD';"
    echo "GRANT ALL PRIVILEGES ON DATABASE $django_db TO $django_db_user;" > $__pgsql_batch
    try sudo -u postgres psql -f $__pgsql_batch

}

# ### Deletes all the database configuration required for the SATNET system.
remove_postgresql()
{
    sudo -u postgres dropdb $django_db
    sudo -u postgres dropuser $django_db_user
}


__secret_key_file='secret.key'
# ### Method that creates the <secrets> directory and initializes it with the
# passwords for accessing to the database and to the email account.
create_secrets()
{
    mkdir -p $webservices_secrets_dir
    [[ -e $webservices_secrets_init ]] || touch $webservices_secrets_init

    __secret_key=$( "$django_keygen" )
    echo ">>> Generating django's SECRET_KEY=$__secret_key"
    echo "SECRET_KEY = '$__secret_key'" > $webservices_secrets_auth

    echo '>>> Generating database access configuration file...'
    echo ">>> $webservices_secrets_database should be updated in case the user/password for the database change."

    echo 'DATABASES = {' > $webservices_secrets_database
    echo "    'default': {" >> $webservices_secrets_database
    echo "        'ENGINE': 'django.db.backends.postgresql_psycopg2'," >> $webservices_secrets_database
    echo "        'NAME': '$django_db'," >> $webservices_secrets_database
    echo "        'USER': '$django_db_user'," >> $webservices_secrets_database
    echo "        'PASSWORD': '$django_db_password'," >> $webservices_secrets_database
    echo "        'HOST': 'localhost'," >> $webservices_secrets_database
    echo "        'PORT': ''," >> $webservices_secrets_database
    echo "    }" >> $webservices_secrets_database
    echo "}" >> $webservices_secrets_database

    echo ">>> Generating email configuration file..."
    echo ">>> $webservices_secrets_email should be updated with the correct email account information."

    echo ">>> Notifications TLS SMTP server account information:"
    try ask_visible 'server URL'
    smtp_url=$__INPUT_STRING
    try ask_visible 'server port'
    smtp_port=$__INPUT_STRING
    try ask_visible 'username'
    smtp_email=$__INPUT_STRING
    try ask_password
    smtp_password=$__PASSWORD

    echo "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'" > $webservices_secrets_email
    
    # ##########################################################################
    # ### PATCHED: SMTP FOR GMAIL
    #echo "EMAIL_HOST = 'smtp.gmail.com'" >> $webservices_secrets_email
    #echo "EMAIL_PORT = 587" >> $webservices_secrets_email
    #echo "EMAIL_HOST_USER = 'XXXXXX@gmail.com'" >> $webservices_secrets_email
    #echo "EMAIL_HOST_PASSWORD = 'XXXXXXXX'" >> $webservices_secrets_email
    # ##########################################################################

    echo "EMAIL_HOST = '$smtp_url'" >> $webservices_secrets_email
    echo "EMAIL_PORT = $smtp_port" >> $webservices_secrets_email
    echo "EMAIL_HOST_USER = '$smtp_email'" >> $webservices_secrets_email
    echo "EMAIL_HOST_PASSWORD = '$smtp_password'" >> $webservices_secrets_email

    echo "EMAIL_USE_TLS = True" >> $webservices_secrets_email
    echo "#EMAIL_FILE_PATH = 'tmp/email-messages/'" >> $webservices_secrets_email

    echo ">>> Generating pusher.com configuration file..."
    echo ">>> $webservices_secrets_pusher should be updated with the correct pusher.com account information."

    echo "PUSHER_APP_ID = '12345'" >> $webservices_secrets_pusher
    echo "PUSHER_APP_KEY = '07897sdfa09df78a'" >> $webservices_secrets_pusher
    echo "PUSHER_APP_SECRET = '07897sdfa09df78a'" >> $webservices_secrets_pusher

}

__secret_key_file='secret.key'
# ### Method that creates the <secrets> directory and initializes it with the
# passwords for accessing to the database and to the email account.
create_travis_secrets()
{
    mkdir -p $webservices_secrets_dir
    [[ -e $webservices_secrets_init ]] || touch $webservices_secrets_init

    __secret_key=$( "$django_keygen" )
    echo ">>> Generating django's SECRET_KEY=$__secret_key"
    echo "SECRET_KEY='$__secret_key'" > $webservices_secrets_auth

    echo 'DATABASES = {' > $webservices_secrets_database
    echo "    'default': {" >> $webservices_secrets_database
    echo "        'ENGINE': 'django.db.backends.postgresql_psycopg2'," >> $webservices_secrets_database
    echo "        'NAME': '$django_db'," >> $webservices_secrets_database
    echo "        'USER': 'postgres'," >> $webservices_secrets_database
    echo "        'PASSWORD': ''," >> $webservices_secrets_database
    echo "        'HOST': 'localhost'," >> $webservices_secrets_database
    echo "        'PORT': ''," >> $webservices_secrets_database
    echo "    }" >> $webservices_secrets_database
    echo "}" >> $webservices_secrets_database

    echo "EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'" > $webservices_secrets_email
    echo "EMAIL_FILE_PATH = 'tmp/email-messages/'" >> $webservices_secrets_email

    echo "PUSHER_APP_ID = '12345'" >> $webservices_secrets_pusher
    echo "PUSHER_APP_KEY = '07897sdfa09df78a'" >> $webservices_secrets_pusher
    echo "PUSHER_APP_SECRET = '07897sdfa09df78a'" >> $webservices_secrets_pusher

}

# ### Method that configures a given root with the virtualenvirment required,
# all the pip packages and the directories.
configure_root()
{

    [[ -d "$webservices_secrets_dir" ]] && rm -Rf $webservices_secrets_dir
    create_secrets

    mkdir -p $webservices_logs_dir
    mkdir -p $webservices_public_html_dir

    [[ -f "$webservices_venv_activate" ]] && rm -Rf $webservices_venv_dir

    [[ $branch_name == 'development_3k' ]] && {
        try virtualenv --python=python3 $webservices_venv_dir
    } || {
        try virtualenv $webservices_venv_dir
    }

    [[ ! -f "$webservices_venv_activate" ]] && {
        echo 'Virtual environment activation failed... exiting!'
        exit -1
    }

    clear && echo '>>>>> Activating virtual environment...'
    cd $webservices_dir
    try source $webservices_venv_activate

    try pip install -r "$webservices_requirements_txt"
    try pip install autobahn[asyncio,accelerate,compress,serialization]
    try python manage.py syncdb
    try python manage.py collectstatic

    deactivate
    cd $script_path
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

__wget_dir='/var/www/'

# ### This is the function utilized for adding the crontab task required by
# django-periodically for executing periodic maintenance tasks of the web
# applications
configure_crontab()
{
    __django_runtasks="python $webservices_manage_py runtasks"
    __crontab_command="source $webservices_venv_activate && $__django_runtasks"
    __crontab_task="30 23 * * * $__crontab_user $__crontab_command"

    #__celestrak_command="wget -r --level=1 --no-parent --directory-prefix=$__wget_dir $__celestrak_url"
    __celestrak_task="00 23 * * * $__crontab_user $__crontab_command"

    echo '# Adding crontab task for django-periodically...' | sudo tee $__crontab_conf
    echo "SHELL=$__crontab_shell" | sudo tee -a $__crontab_conf
    echo "PATH=$__crontab_path" | sudo tee -a $__crontab_conf
    echo "$__crontab_task" | sudo tee -a $__crontab_conf
}

node_js_root_dir='/opt'
# ### This function installs bower together with Node.js, the vanilla version
# that can be downloaded from GitHub.
install_bower()
{

    ng_app_dir="$webservices_dir/website/static/scripts/"

    sudo apt-get install python g++ make checkinstall
    cd $node_js_root_dir
    sudo wget -N http://nodejs.org/dist/node-latest.tar.gz
    sudo tar xzvf node-latest.tar.gz && cd node-v*
    sudo ./configure

    # ### IMPORTANT
    echo 'In the next menu that will be prompted, the <v> letter from the'
    echo 'version number must be erased. For doing that, select <Choice 3>'
    echo 'and erase the <v> letter leaving the rest of the version number'
    echo 'intact.'
    sudo checkinstall -D
    sudo dpkg -i node_*
    
    sudo npm install -g bower
    cd $ng_app_dir
    npm install
    bower install

}

last_instructions()
{
    clear && echo 'Congratulations, installation is complete.'
}

venv_wrapper_config='/usr/local/bin/virtualenvwrapper.sh'
bashrc_file="$HOME/.bashrc"
venv_workon="$HOME/.virtualenvs"
venv_projects="$HOME/repositories/satnet-release-1/WebServices"

# ### Examples of HOW TO call this script
usage()
{
    echo "Please, use ONLY ONE ARGUMENT at a time:"
    echo "Usage: $0 [-a] #Installs EVERYTHING."
    echo "Usage: $0 [-b] #Install Node.js and Bower (from GitHub)"
    echo "Usage: $0 [-c] #Create and install self-signed certificates"
    echo "Usage: $0 [-i] #Install Debian packages <root>"
    echo "Usage: $0 [-p] #Configures PostgreSQL"
    echo "Usage: $0 [-r] #Removes specific PostgreSQL configuration for SATNET."
    echo "Usage: $0 [-s] #Creates the <secrets> module with initial values."
    echo "Usage: $0 [-t] #Creates the <secrets> module with the cfg for TRAVIS."
    echo "Usage: $0 [-o] #Configures Crontab for django-periodically"
    echo "Usage: $0 [-v] #Configure virtualenv"
    echo "Usage: $0 [-x] #Configures Apache web server"

    1>&2;
    exit 1;
}

################################################################################
# ### Main variables and parameters
script_path="$( cd "$( dirname "$0" )" && pwd )"

branch_name=$( git branch | grep '*' | cut -d' ' -f2 )
linux_dist=$( cat /etc/issue.net | cut -d' ' -f1 )

[[ $linux_dist == 'Debian' ]] && {

    debian_version=$( cat /etc/issue.net | cut -d' ' -f3 )
    [[ $debian_version -eq '7' ]] && {
        linux_packages="$script_path/debian.$debian_version.packages"
    }
    [[ $debian_version -eq '8' ]] && {
        linux_packages="$script_path/debian.$debian_version.packages"
    }

}

[[ $linux_dist == 'Ubuntu' ]] && {
    ubuntu_version=$( cat /etc/issue.net | cut -d' '  -f2  | cut -d'.' -f1 )
    linux_packages="$script_path/ubuntu.$ubuntu_version.packages"
}

django_keygen="$script_path/django-secret-key-generator.py"
project_path=$( readlink -e "$script_path/.." )
webservices_dir="$project_path"
webservices_secrets_dir="$webservices_dir/website/secrets"
webservices_requirements_txt="$webservices_dir/requirements.txt"
webservices_secrets_init="$webservices_secrets_dir/__init__.py"
webservices_secrets_auth="$webservices_secrets_dir/auth.py"
webservices_secrets_database="$webservices_secrets_dir/database.py"
webservices_secrets_email="$webservices_secrets_dir/email.py"
webservices_secrets_pusher="$webservices_secrets_dir/pusher.py"
webservices_venv_dir="$webservices_dir/.venv"
webservices_venv_activate="$webservices_venv_dir/bin/activate"
webservices_manage_py="$webservices_dir/manage.py"
webservices_public_html_dir="$webservices_dir/public_html"
webservices_logs_dir="$webservices_dir/logs"
webservices_logs_dir="$webservices_dir/logs"
webservices_public_html_dir="$webservices_dir/public_html"
webservices_static_dir="$webservices_public_html_dir/static"

################################################################################
# ### Main execution loop
source ./command-lib.sh

echo ">>> The script installer is going to be executed within the following autodetected environment:"
echo "    * branch_name = $branch_name"
echo "    * linux_dist = $linux_dist"

[[ $linux_dist == 'Debian' ]] && {
    echo "    * debian_version = $debian_version"
}

[[ $linux_dist == 'Ubuntu' ]] && {
    echo "    * ubuntu_version = $ubuntu_version"
}

echo "    * packages_file = $linux_packages"
echo "    * script_path = $script_path"
echo "    * project_path = $project_path"
echo "    * webservices_path = $webservices_dir"

if [ $# -lt 1 ] ; then
    usage
    exit 0
fi

while getopts ":abcikprstovx" opt; do
    case $opt in
        a)
            clear && echo '>>>>>>> Installing OS native packages...'
            install_packages
            clear && echo '>>>>>>> Configuring PostgreSQL...'
            configure_postgresql
            clear && echo '>>>>>>> Configuring Crontab...'
            configure_crontab
            clear && echo '>>>>>>> Configuring Root...'
            configure_root
            clear && echo '>>>>>>> Configuring Apache...'
            configure_apache
            echo 'DONE'
            last_instructions
            exit 1
            ;;
        b)
            clear && echo 'Installing Bower and Node.js...'
            install_bower
            echo 'DONE'
            exit 1
            ;;
        c)
            clear && echo 'Creating self-signed certificates...'
            create_self_signed_cert
            echo 'DONE'
            exit 1;
            ;;
        i)
            clear && echo '>>>>>>> Installing OS native packages...'
            install_packages
            echo 'DONE'
            ;;
        k)
            clear && echo 'Creating keys and certificates for Apache...'
            create_apache_keys
            echo 'DONE'
            ;;
        p)
            clear && echo 'Configuring PostgreSQL...'
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
        s)
            clear && echo 'Creating <secrets>...'
            create_secrets
            echo 'DONE'
            exit 1;
            ;;
        t)
            clear && echo 'Creating TRAVIS <secrets>...'
            create_travis_secrets
            echo 'DONE'
            exit 0;
            ;;
        o)
            clear && echo 'Configuring Crontab...'
            configure_crontab
            echo 'DONE'
            exit 1
            ;;
        v)
            clear && echo 'Configuring Root...'
            configure_root
            echo 'DONE'
            exit 1;
            ;;
        x)
            clear && echo 'Configuring Apache...'
            configure_apache
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
