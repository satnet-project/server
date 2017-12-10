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

    [[ ! -d $DEST_DIR ]] && {
        printf "\t* Creating destination directory <$DEST_DIR> ..."
        mkdir -p $DEST_DIR
        printf ' done!\n'
    }

}


dry_call()
{

    # This function executes a 'dry call' (or wet) to the given binary with
    # the given parameters

    BIN="$1"
    OPTS="$2"

    [[ "$RUN_DRY" = false ]] && {
        $BIN $OPTS
    } || {
        printf "\t* DRY ::: <%s>\n" "$BIN"
        printf "\t* DRY ::: <%s>\n" "$OPTS"
    }

}


download_tarball()
{

    # This function downloads the remote tarball, retrieving first the filename
    # of the tarball itself, in case there is an HTTP redirection.

    CURL_OPTS='-sIkL'
    SED_REGEX='/filename=/!d;s/.*filename=(.*)$/\1/'
    FILENAME="$( curl $CURL_OPTS $URL | sed -r $SED_REGEX | tr -d '\r' )"
    DEST_FILE="$DEST_DIR/$FILENAME"
    printf "\t* Remote tarball filename = %s\n" $FILENAME

    WGET_BIN='wget'
    WGET_OPTS_1="-t $ATTEMPTS -c -O $DEST_FILE "
    WGET_OPTS="-t $ATTEMPTS -c -O $DEST_FILE $URL"

    dry_call "$WGET_BIN" "$WGET_OPTS"

}


detect_type ()
{

    # This function reads out the directory structure and finds what type of
    # package it is.

    #   $1  Path to the root of the uncompressed tarball

    ROOT_DIR="$1"

    CMAKE_DIR="$ROOT_DIR/cmake"
    [[ -d $CMAKE_DIR ]] && {
        printf "\t* CMAKE detected, executing installation\n"
        install_cmake_tarball
        return
    } || {
        printf "\t* Not a CMAKE-type package\n"
    }

    CHECK_CONFIGURE_FILE="$ROOT_DIR/configure"
    echo "CHECK_CONFIGURE_FILE = $CHECK_CONFIGURE_FILE"
    [[ -f "$CHECK_CONFIGURE_FILE" ]] && {
        printf "\t* Configure detected, executing installation\n"
        return
    } || {
        printf "\t* Not a configure-type package\n"
    }

}


install_tarball()
{

    # This function decompresses the tarball package and detects what type of
    # package it is, in order to install it properly.

    TAR_BIN='tar'
    TAR_PARAMS='-xvzf'
    TAR_DEST="-C $DEST_DIR"
    TAR_OPTS="$TAR_PARAMS $DEST_FILE $TAR_DEST"

    dry_call "$TAR_BIN" "$TAR_OPTS"

    PKG_NAME=$( tar tvf $DEST_FILE | egrep -o "[^ ]+/$" | cut -d'/' -f1 | uniq )
    PKG_ROOT_DIR="$DEST_DIR/$PKG_NAME"

    detect_type $PKG_ROOT_DIR

}


install_cmake_tarball()
{

    # This function installs the given package following the CMAKE procedure:
    # (1) mkdir $ROOT_DIR/build
    # (2) cd $ROOT_DIR/build && cmake ../ && make

    CWD_DIR=$( pwd )
    CMAKE_BUILD_DIR="$PKG_ROOT_DIR/build"

    [[ -d "$CMAKE_BUILD_DIR" ]] && {
        printf "\t* <$CMAKE_BUILD_DIR> exists, replacing it...\n"

        RM_OPTS="-Rf \"$CMAKE_BUILD_DIR\""
        dry_call 'rm' "$RM_OPTS"

    }

    MKDIR_OPTS="-p \"$CMAKE_BUILD_DIR\""
    dry_call 'mkdir' "$MKDIR_OPTS"

    cd "$CMAKE_BUILD_DIR"

    CMAKE_OPTS="../"
    dry_call 'cmake' "$CMAKE_OPTS"

    dry_call 'make'

    cd "$CWD_DIR"

}


install_configure_tarball()
{
    # TODO # Finish this function whenever necessary

    CONFIGURE_BIN="$1/configure"
    BASH_BIN='bash'
    BASH_OPTS="$CONFIGURE_BIN"

    dry_call "$BASH_BIN" "$BASH_OPTS"

}


URL="$1"
RUN_DRY="$2"
DEST_DIR="$3"

ATTEMPTS=3

echo "»»» Checking script's execution environment"
run_checks

echo "»»» Downloading package from $URL"
download_tarball

echo "»»» Installing tarball package"
install_tarball
