/home/rtubiopa/server_master/logs/*.log {
  weekly
  missingok
  rotate 7
  compress
  delaycompress
  notifempty
  sharedscripts
  postrotate
     /etc/init.d/apache2 restart
  endscript
}
