#!/bin/bash
# ##############################################################################
# <install-tarballs.sh>
#
#  Created on: December 11th, 2017
#      Author: Ricardo Tubío (rtpardavila[at]gmail.com)
#
# This file is part of the toolbox suite of automated scripts.
# <install-tarballs.sh> script is free software: you can redistribute it
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
# along with <install-tarballs.sh>. If not, see
# <http://www.gnu.org/licenses/>.
# ##############################################################################

run_checks()
{

    [[ $( whoami ) == 'root' ]] || {
        printf "\t * [ERROR]: Need to be <root>, exiting...\n"
        exit -1
    }

    [[ $# -ne 2 ]] && {
        echo "[ERROR] Wrong call: no_params = $#"
        echo "[ERROR] Usage: $0 <tarballs_file> <destination_dir>"
        exit -1
    }

    [[ ! -d $DEST_DIR ]] && {
        printf "\t* Creating destination directory <$DEST_DIR> ..."
        mkdir -p $DEST_DIR
        printf ' done!\n'
    }

}



RUN_DRY=true
TARBALL_PKS_FILE="$1"
DEST_DIR="$2"

echo "»»» Checking script's execution environment"
run_checks
