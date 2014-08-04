#!/bin/bash

__load_default_config=false
__output_file='satnet-ssl'

if [ $# -gt 0 ]
then
    if [ ! -f $1 ]
    then
        echo "File <$1> does not exist!"
        __load_default_config=true
    else
        echo "Loading custom configuration from <$1>..."
        source $1
    fi
else
    echo "No custom configuration provided, loading defaults..."
    __load_default_config=true
fi

if [ "$__load_default_config" = true ]
then
    echo 'Loading default configuration...'
    user='rtubiopa'
    server_name='satnet.aero.calpoly.edu'
    server_admin='satnet.calpoly@gmail.com'
    server_certificates_dir='/etc/apache2/certificates'
    server_certificate="$server_certificates_dir/satnet.aero.calpoly.edu.crt"
    server_key="$server_certificates_dir/satnet.aero.calpoly.edu.key"
    project_root_dir='/home/rtubiopa/repositories/satnet-release-1/WebServices'
    logs_dir="$project_root_dir/logs"
    public_html_dir="$project_root_dir/public_html"
    static_dir="$public_html_dir/static"
    document_root="$static_dir"
fi

echo '<VirtualHost *:443>' > $__output_file
echo '' >> $__output_file
echo "	  ServerName $server_name" >> $__output_file
echo "    ServerAdmin $server_admin" >> $__output_file
echo "	  DocumentRoot $static_dir" >> $__output_file
echo '' >> $__output_file
echo "    Alias /favicon.ico $public_html_dir/favicon.ico" >> $__output_file
echo "    Alias /static $static_dir" >> $__output_file
echo '' >> $__output_file
echo '    GnuTLSEnable on' >> $__output_file
echo '    GnuTLSPriorities NORMAL:!DHE-RSA:!DHE-DSS:!AES-256-CBC:%COMPAT' >> $__output_file
echo "    GnuTLSCertificateFile $server_certificate" >> $__output_file
echo "    GnuTLSKeyFile $server_key" >> $__output_file
echo '' >> $__output_file
echo "    WSGIScriptAlias / $project_root_dir/website/wsgi.py" >> $__output_file
echo "    WSGIDaemonProcess satnet user=$user python-path=$project_root_dir:$project_root_dir/.venv/lib/python2.7/site-packages" >> $__output_file
echo '' >> $__output_file
echo "    <Directory $project_root_dir/>" >> $__output_file
echo '        WSGIProcessGroup satnet' >> $__output_file
echo '        Order deny,allow' >> $__output_file
echo '        Allow from all' >> $__output_file
echo '    </Directory>' >> $__output_file
echo '' >> $__output_file
echo "    CustomLog $logs_dir/access.log combined" >> $__output_file
echo "    CustomLog $logs_dir/ssl_request.log \"%t %h %{SSL_PROTOCOL}s %{SSL_CIPHER}s \\\"%r\\\" %b\"" >> $__output_file
echo "    ErrorLog $logs_dir/error.log" >> $__output_file
echo '' >> $__output_file
echo '</VirtualHost>' >> $__output_file
