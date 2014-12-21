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

# ### Installs the packages necessary for the Debian operating system.
install_packages()
{

    sudo apt-get update
    sudo apt-get dist-upgrade

    sudo apt-get install apache2
    sudo apt-get install libapache2-mod-wsgi libapache2-mod-gnutls
    sudo apt-get install postgresql postgresql-contrib phppgadmin
    sudo apt-get install postgresql-server-dev-all
    sudo apt-get install python python-virtualenv python-pip python-dev
    sudo apt-get install binutils libproj-dev gdal-bin
    sudo apt-get install build-essential libssl-dev libffi-dev

    # TODO :: Nodejs, bower and grunt install
    sudo apt-get install ruby rubygem-integration
    sudo gem install sass
    sudo gem install compass

    sudo apt-get install yui-compressor

    sudo apt-get clean

    pip install virtualenvwrapper

}

APACHE_2_CERTIFICATES_DIR='/etc/apache2/certificates'
CERTIFICATE_NAME='marajota.calpoly.edu.crt'
KEY_NAME='marajota.calpoly.edu.key'
__tmp_cert="/tmp/tmp.crt"
__tmp_csr="/tmp/tmp.csr"
__tmp_key="/tmp/tmp.key"
__original_tmp_key="/tmp/tmp.key.original"
# ### This function creates a new self signed certificate and key to be used by
# the Apache2 server and installs them in the correct directory.
create_apache_keys()
{
    # 1: Generate a Private Key
    openssl genrsa -des3 -out $__tmp_key 1024
    # 2: Generate a CSR (Certificate Signing Request)
    openssl req -new -key $__tmp_key -out $__tmp_csr
    # 3: Remove Passphrase from Key
    mv -f $__tmp_key $__original_tmp_key
    openssl rsa -in $__original_tmp_key -out $__tmp_key
    # 4: Generating a Self-Signed Certificate
    openssl x509 -req -days 365 -in $__tmp_csr -signkey $__tmp_key -out $__tmp_cert

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
__apache_document_root="$webservices_static_dir"
__apache_rotate_logs="/usr/local/apache/bin/rotatelogs"
__phppgadmin_apache_config='/etc/apache2/conf.d/phppgadmin'
__phppgadmin_config_file='/etc/phppgadmin/config.inc.php'
# ### This function configures the apache2 server.
configure_apache()
{

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
    echo '    SSLSessionCache         shmcb:${APACHE_RUN_DIR}/ssl_scache(512000)' | sudo tee -a $__satnet_apache_ssl_conf
    echo '    SSLSessionCacheTimeout  300' | sudo tee -a $__satnet_apache_ssl_conf
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
    echo "    WSGIDaemonProcess satnet python-path=$webservices_dir:$webservices_dir/.venv/lib/python2.7/site-packages" | sudo tee -a $__satnet_apache_conf
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

    # default 80 ports are disabled (TLS access only!)
    sudo sed -i -e 's/NameVirtualHost \*\:80/# NameVirtualHost \*\:80/g' -e 's/Listen 80/# Listen 80/g' $__apache_server_ports

    create_apache_keys

    sudo a2dismod gnutls
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
django_user='satnet'
django_user_password='satnet'
# ### Configures a PostgreSQL server with a database for the SATNET system.
configure_postgresql()
{

    # ### Uncomment the following lines if you want to reset default user's
    # password.
    #echo 'User <postgres> grants access through <phppgadmin>'
    #echo 'Configure password for user <postgres>.'
    #echo "\password postgres" > $__pgsql_batch
    #sudo -u postgres psql -f $__pgsql_batch

    if [[ $( sudo -u postgres psql -l | grep $django_db | wc -l ) -eq 0 ]]
    then
        echo ">>>> Creating postgres database, name = <$django_db>"
        sudo -u postgres createdb $django_db
    else
        echo ">>>> Database db = $django_db already exists, skipping..."
    fi

    if [[ ! $( sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$django_user'" ) -eq 1 ]]
    then
        echo ">>>> Creating postgres user = <$django_user>"
        sudo -u postgres createuser -r -l -S -E -P -d $django_user
        echo "GRANT ALL PRIVILEGES ON DATABASE $django_db TO $django_user;" > $__pgsql_batch
        sudo -u postgres psql -f $__pgsql_batch
    else
        echo ">>>> Postgres user = <$django_user> already exists, skipping..."
    fi

}

# ### Deletes all the database configuration required for the SATNET system.
remove_postgresql()
{
    sudo -u postgres dropdb $django_db
    sudo -u postgres dropuser $django_user
}


__secret_key_file='secret.key'
# ### Method that creates the <secrets> directory and initializes it with the
# passwords for accessing to the database and to the email account.
create_secrets()
{
    mkdir -p $webservices_secrets_dir
    [[ -e $webservices_secrets_init ]] || touch $webservices_secrets_init

    __secret_key=$( ./django-secret-key-generator.py )
    echo ">>> Generating django's SECRET_KEY=$__secret_key"
    echo "SECRET_KEY='$__secret_key'" > $webservices_secrets_auth

    echo '>>> Generating database access configuration file...'
    echo ">>> $webservices_secrets_database should be updated in case the user/password for the database change."
    echo 'Press any key to continue...'
    read

    echo 'DATABASES = {' > $webservices_secrets_database
    echo "    'default': {" >> $webservices_secrets_database
    echo "        'ENGINE': 'django.db.backends.postgresql_psycopg2'," >> $webservices_secrets_database
    echo "        'NAME': '$django_db'," >> $webservices_secrets_database
    echo "        'USER': '$django_user'," >> $webservices_secrets_database
    echo "        'PASSWORD': '$django_user_password'," >> $webservices_secrets_database
    echo "        'HOST': 'localhost'," >> $webservices_secrets_database
    echo "        'PORT': ''," >> $webservices_secrets_database
    echo "    }" >> $webservices_secrets_database
    echo "}" >> $webservices_secrets_database

    echo ">>> Generating email configuration file..."
    echo ">>> $webservices_secrets_email should be updated with the correct email account information."
    echo 'Press any key to continue...'
    read

    echo "EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'" > $webservices_secrets_email
    echo "EMAIL_HOST='smtp.gmail.com'" >> $webservices_secrets_email
    echo "EMAIL_PORT=587" >> $webservices_secrets_email
    echo "EMAIL_HOST_USER='XXXXXX@gmail.com'" >> $webservices_secrets_email
    echo "EMAIL_HOST_PASSWORD='XXXXXXXX'" >> $webservices_secrets_email
    echo "EMAIL_USE_TLS=True" >> $webservices_secrets_email
}

# ### Method that configures a given root with the virtualenvirment required,
# all the pip packages and the directories.
configure_root()
{
    mkdir -p $webservices_logs_dir
    mkdir -p $webservices_public_html_dir

    [[ -f "$webservices_venv_activate" ]] && rm -Rf $webservices_venv_activate
    virtualenv $webservices_venv_dir
    [[ ! -f "$webservices_venv_activate" ]] && {
        echo 'Virtual environment activation failed... exiting!'
        exit -1
    }

    [[ ! -d "$webservices_secrets_dir" ]] && create_secrets

    clear && echo '>>>>> Installing Angular dependencies...'
    install_bower

    clear && echo '>>>>> Activating virtual environment...'
    cd $webservices_dir
    source $webservices_venv_activate

    pip install -r "$webservices_requirements_txt"
    pip install -r "$protocol_requirements_txt"    
    python manage.py syncdb
    python manage.py collectstatic

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

    --directory-prefix
    __celestrak_command="wget -r --level=1 --no-parent --directory-prefix=$__wget_dir $__celestrak_url"
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

    # sudo apt-get install python g++ make checkinstall
    # cd $node_js_root_dir
    # sudo wget -N http://nodejs.org/dist/node-latest.tar.gz
    # sudo tar xzvf node-latest.tar.gz && cd node-v*
    # sudo ./configure
    # ### IMPORTANT
    # echo 'In the next menu that will be prompted, the <v> letter from the'
    # echo 'version number must be erased. For doing that, select <Choice 3>'
    # echo 'and erase the <v> letter leaving the rest of the version number'
    # echo 'intact.'
    # sudo checkinstall -D
    # sudo dpkg -i node_*
    sudo apt-get install nodejs npm
    sudo npm install -g bower
    cd $ng_app_dir
    sudo npm install -g
    bower install
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
    echo "Usage: $0 [-o] #Configures Crontab for django-periodically"
    echo "Usage: $0 [-v] #Configure virtualenv"
    echo "Usage: $0 [-x] #Configures Apache web server"

    1>&2;
    exit 1;
}

################################################################################
# ### Main variables and parameters
script_path="$( cd "$( dirname "$0" )" && pwd )"
project_path=$( readlink -e "$script_path/.." )
webservices_dir="$project_path/WebServices"
protocol_dir="$project_path/Protocol"
webservices_secrets_dir="$webservices_dir/website/secrets"
webservices_requirements_txt="$webservices_dir/requirements.txt"
protocol_requirements_txt="$protocol_dir/requirements.txt"
webservices_secrets_init="$webservices_secrets_dir/__init__.py"
webservices_secrets_auth="$webservices_secrets_dir/auth.py"
webservices_secrets_database="$webservices_secrets_dir/database.py"
webservices_secrets_email="$webservices_secrets_dir/email.py"
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
echo "script_path = $script_path"
echo "project_path = $project_path"
echo "webservices_path = $webservices_dir"

if [ $# -lt 1 ] ; then
    usage
    exit 0
fi

while getopts ":abcikprsovx" opt; do
    case $opt in
        a)
            echo 'This process is not unattended, user interaction is required.'
            echo 'Press any key to continue...'
            read

            echo 'Installing Debian packages...'
            install_packages
            clear && echo '>>>>>>> Configuring PostgreSQL...'
            configure_postgresql
            clear && echo '>>>>>>> Configuring Crontab...'
            configure_crontab
            clear && echo '>>>>>>> Configuring virtualenv...'
            configure_root
            clear && echo '>>>>>>> Configuring Apache...'
            configure_apache
            echo 'DONE'
            exit 1
            ;;
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
            echo 'Installing Debian packages...'
            echo 'This process is not unattended, user interaction is required.'
            echo 'Press any key to continue...'
            read
            install_packages
            echo 'DONE'
            ;;
        k)
            echo 'Creating keys and certificates for Apache...'
            create_apache_keys
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
        s)
            echo 'Creating <secrets>...'
            create_secrets
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
        x)
            echo 'Configuring Apache...'
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
