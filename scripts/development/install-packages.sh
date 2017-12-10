#!/bin/bash
# ##############################################################################
# <install-packages.sh>
#
#  Created on: September 28, 2013
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
# along with <install-packages.sh>. If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################

PACKAGES_FILE='debian.packages'

[[ $# -ne 0 ]] && {
  PACKAGES_FILE=$1
}

[[ ! -f $PACKAGES_FILE ]] && {
  echo "File $PACKAGES_FILE does not exist, aborting..."
  exit -1
}

echo "Installing packages from file = $PACKAGES_FILE"

sudo apt -y install $(grep -vE "^\s*#" $PACKAGES_FILE | tr "\n" " ")
