#!/bin/bash
# ##############################################################################
# <setup.sh>
#
#  Created on: December 11th, 2017
#      Author: Ricardo Tubío (rtpardavila[at]gmail.com)
#
# This file is part of the toolbox suite of automated scripts.
# <install-packages.sh> script is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# <install-packages.sh> is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with <setup.sh>. If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################

# This script aims at simplifying the process for setting up the development
# environment of this project in a Debian environment.

configure_variables()
{

    # This function simply configures all the variables for executing the
    # different parts of the script.

    _ROOT_=$( pwd )

    ETC_DIR='/etc'
    ETC_DEFAULT_DIR="$ETC_DIR/default"
    ETC_OS_RELEASE="$ETC_DIR/os-release"
    . $ETC_OS_RELEASE

    SCRIPTS_DEV_DIR="$_ROOT_/scripts/development"
    INSTALL_DEB_BIN="$SCRIPTS_DEV_DIR/install-packages.sh"
    INSTALL_REMOTE_BIN="$SCRIPTS_DEV_DIR/install-remote-packages.sh"
    PKGS_DIR="$SCRIPTS_DEV_DIR/packages"
    CURRENT_DEB_PKGS="debian.$VERSION_ID.packages"
    DEB_PKGS="$PKGS_DIR/$CURRENT_DEB_PKGS"
    REMOTE_PKGS="$PKGS_DIR/debian.$VERSION_ID.remote"

    [[ ! -f $DEB_PKGS ]] && {
        echo "»»» [ERROR] »»» Debian $VERSION_ID is not supported"
        exit -1
    }

    REMOTE_PKGS="$PKGS_DIR/"

    PY_VENV_NAME='.server'
    PY_VENV_DIR="$_ROOT_/$PY_VENV_NAME"
    PY_VENV_ACTIVATE="$PY_VENV_DIR/bin/activate"
    PY_VENV_DEACTIVATE="$PY_VENV_DIR/bin/deactivate"
    PY_REQUIREMENTS="$_ROOT_/requirements.txt"

}


install_python_environment()
{

    # This function creates the python environment for development and installs
    # all the required packages.

    [[ ! -d $PY_VENV_DIR ]] && {
        printf "\t* Python virtual environment does not exist, craeting...\n"
        virtualenv --python=python3.5 $PY_VENV_DIR
    }

    source $PY_VENV_ACTIVATE
    pip install -r $PY_REQUIREMENTS

}

###############################################################################
# ### Main execution loop
###############################################################################

# (0) configure script variables
configure_variables

# (1) install Debian packages
clear && echo "»»» Installing Debian packages..."
bash $INSTALL_DEB_BIN $DEB_PKGS

# (2) install remote packages
clear && echo "»»» Installing remote packages..."
bash $INSTALL_REMOTE_BIN $REMOTE_PKGS

# (3) install Python packages
clear && echo "»»» Installing Python packages..."
install_python_environment
