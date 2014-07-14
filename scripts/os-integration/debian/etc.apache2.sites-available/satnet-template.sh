server_admin='satnet.calpoly@gmail.com'
server_certificates_dir='/etc/apache2/certificates'
server_certificate="$server_certificates_dir/marajota.calpoly.edu.crt"
server_key="$server_certificates_dir/marajota.calpoly.edu.key"
project_root_dir='/home/rtubio/repositories/satnet-release-1/WebServices'
public_html_dir="$project_root_dir/public_html"

echo '<VirtualHost *:443>' > $1
echo '' >> $1
echo "    ServerAdmin $server_admin" >> $1
echo '' >> $1
echo "    Alias /favicon.ico $public_html_dir/favicon.ico" >> $1
echo "    Alias /static $public_html_dir/static" >> $1
echo '' >> $1
echo '    GnuTLSEnable on' >> $1
echo '    GnuTLSPriorities NORMAL:!DHE-RSA:!DHE-DSS:!AES-256-CBC:%COMPAT' >> $1
echo "    GnuTLSCertificateFile $server_certificate" >> $1
echo "    GnuTLSKeyFile $server_key" >> $1
echo '' >> $1
echo "    WSGIScriptAlias / $project_root_dir/website/wsgi.py" >> $1
echo "    WSGIDaemonProcess satnet user=rtubio python-path=$project_root_dir:$project_root_dir/.venv/lib/python2.7/site-packages" >> $1
echo '' >> $1
echo "    <Directory $project_root_dir/>" >> $1
echo '        WSGIProcessGroup satnet' >> $1
echo '        Order deny,allow' >> $1
echo '        Allow from all' >> $1
echo '    </Directory>' >> $1
echo '' >> $1
echo "    CustomLog $project_root_dir/logs/access.log combined" >> $1
echo "    CustomLog $project_root_dir/logs/ssl_request.log \"%t %h %{SSL_PROTOCOL}s %{SSL_CIPHER}s \\\"%r\\\" %b\"" >> $1
echo "    ErrorLog $project_root_dir/logs/error.log" >> $1
echo '' >> $1
echo '</VirtualHost>' >> $1
