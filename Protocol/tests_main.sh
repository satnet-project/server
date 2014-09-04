#!/bin/bash


################################################################################
# ### Main variables and parameters
script_path="$( cd "$( dirname "$0" )" && pwd )"
project_path="$script_path/.."
webservices_dir="$project_path/WebServices"
webservices_manage_py="$webservices_dir/manage.py"
unittests="$script_path/unittests"

python $webservices_manage_py flush --noinput
python "$unittests/test_login_populateDB.py"
trial "$unittests/test_login_singleClient.py"

trial "$unittests/test_login_multipleClients.py"
