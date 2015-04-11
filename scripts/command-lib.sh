#!/bin/bash

################################################################################
# Copyright 2015 John Kugelman (john@kugelman.name)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
# Author: john@kugelman.name
# Open sourced by: rtpardavila@gmail.com
# Description: set of functions to invoke bash "steps" within a script.
################################################################################

# ### TODO In Red Hat, the LSB functions are placed in a different path
[[ $linux_dist == 'Red Hat' ]] && {
    . /etc/init.d/functions
}
# ### Although Debian and Ubuntu are likely to have the LSB functions within the
# same path, beforehand we will consider them as different cases.
[[ $linux_dist == 'Debian' ]] && {
    . /lib/lsb/init-functions
}
[[ $linux_dist == 'Ubuntu' ]] && {
    . /lib/lsb/init-functions
}

RET_OK=1
RET_ERR=0

# ### Function that asks for a password to the user. Includes: number of tries
# and password confirmation.
ask_password() {

    password_1=''
    password_2=''
    MAX_PASS_TRIES='3'
    PASS_TRIES='1'

    until [ $MAX_PASS_TRIES -lt $PASS_TRIES ]
    do

        password_1=''
        password_2=''

        read -s -p "Password:" password_1 && echo
        read -s -p "Repeat password:" password_2 && echo

        [[ $password_1 == $password_2 ]] && {
            __PASSWORD=$password_1
            return $RET_OK
        } || {
            echo 'Passwords do not match!'
            let "PASS_TRIES++"
            continue
        }

    done

    echo 'Maximum number of tries reached!!!'
    return $RET_ERR

}

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit $RET_ERR; }
try() { "$@" || die "cannot $*"; }
asuser() { sudo su - "$1" -c "${*:2}"; }

# Use step(), try(), and next() to perform a series of commands and print
# [  OK  ] or [FAILED] at the end. The step as a whole fails if any individual
# command fails.
#
# Example:
#     step "Remounting / and /boot as read-write:"
#     try mount -o remount,rw /
#     try mount -o remount,rw /boot
#     next

step() {
    echo -n "$@"

    STEP_OK=0
    [[ -w /tmp ]] && echo $STEP_OK > /tmp/step.$$
}

try() {
    # Check for `-b' argument to run command in the background.
    local BG=

    [[ $1 == -b ]] && { BG=1; shift; }
    [[ $1 == -- ]] && {       shift; }

    # Run the command.
    if [[ -z $BG ]]; then
        "$@"
    else
        "$@" &
    fi

    # Check if command failed and update $STEP_OK if so.
    local EXIT_CODE=$?

    if [[ $EXIT_CODE -ne 0 ]]; then
        STEP_OK=$EXIT_CODE
        [[ -w /tmp ]] && echo $STEP_OK > /tmp/step.$$

        if [[ -n $LOG_STEPS ]]; then
            local FILE=$(readlink -m "${BASH_SOURCE[1]}")
            local LINE=${BASH_LINENO[0]}

            echo "$FILE: line $LINE: Command \`$*' failed with exit code $EXIT_CODE." >> "$LOG_STEPS"
        fi
    fi

    return $EXIT_CODE
}

next() {
    [[ -f /tmp/step.$$ ]] && { STEP_OK=$(< /tmp/step.$$); rm -f /tmp/step.$$; }
    [[ $STEP_OK -eq 0 ]]  && log_success_msg || log_failure_msg
    echo

    return $STEP_OK
}
