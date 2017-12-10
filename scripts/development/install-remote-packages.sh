#!/bin/bash
# ##############################################################################
# <install-remote-packages.sh>
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
# along with <install-remote-packages.sh>. If not, see
# <http://www.gnu.org/licenses/>.
# ##############################################################################

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

dry=false

[[ $# -eq 2 ]] && dry=true || {

    [[ $# -ne 1 ]] && {
        echo "[ERROR] Need to specify file with the URLs of the .deb packages"
        exit -1
    }

}

[[ ! -f $1 ]] && {
    echo "[ERROR] File <$1> does not exist"
    exit -1
}

TMP_DIR="/tmp"

urls_file=$1
file_index=0
tmp_file_basename="$TMP_DIR/package"

for url in $( cat $urls_file )
do

    filename="$tmp_file_basename-$file_index.deb"
    ((file_index++))

    echo "»»» Installing remote package from $url, filename = $filename"

    [[ "$dry" = false ]] && {
        bash install-remote-package.sh $url $filename
    } || {
        echo "»»» [DRY]"
    }

done
