#!/bin/bash
# ##############################################################################
# <install-remote-package.sh>
#
#  Created on: October 31, 2017
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
# along with <install-remote-package.sh>. If not, see
# <http://www.gnu.org/licenses/>.
# ##############################################################################

[[ $( whoami ) == 'root' ]] ||\
	{ echo 'Need to be <root>, exiting...'; exit -1; }

TMP_DIR="/tmp"
PKG_FIELD='Package'
filename='package-tmp.deb'
tmp_file="$TMP_DIR/$filename"
attempts=3
tmp_file_given=false

[[ $# -eq 2 ]] && {
  tmp_file=$2
  tmp_file_given=true
  echo "Using <$tmp_file> as the name for the temporal_file"
} || {
  [[ $# -ne 1 ]] && {
    echo "Wrong call, need to specify the URL of the tarball package"
    exit -1
  }
}

url="$1"
wget_args="-t $attempts -c -O $tmp_file"

echo $"»»» * url = $url"
echo $"»»» * filename = $filename"

[[ "$tmp_file_given" = false ]] && [[ -e $tmp_file ]] && {
    echo "»»» [WARN] <$tmp_file> exists, removing"
    rm -f $tmp_file
}

echo "»»» Downloading package from $url"
wget $wget_args $url

name=$( dpkg --info $tmp_file | grep $PKG_FIELD | sed -r 's/\s\w+:\s//g' )
echo "»»» Package name: $name"

[[ ! -z $( dpkg --list $name ) ]] && {
    echo "»»» [SKIP] $name is already installed"
} || {
    echo "»»» [INFO] $name is going to be installed"
    dpkg -i $tmp_file
}

apt --fix-broken install
