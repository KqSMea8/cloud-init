#!/usr/bin/python
#
#    Fetch login credentials for EC2 
#    Copyright (C) 2008-2009 Canonical Ltd.
#
#    Author: Soren Hansen <soren@canonical.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import pwd
import sys

import ec2init

def setup_user_keys(keys, user, key_prefix):
    saved_umask = os.umask(077)

    pwent = pwd.getpwnam(user)

    ssh_dir = '%s/.ssh' % pwent.pw_dir
    if not os.path.exists(ssh_dir):
        os.mkdir(ssh_dir)
        os.chown(ssh_dir, pwent.pw_uid, pwent.pw_gid)

    authorized_keys = '%s/.ssh/authorized_keys' % pwent.pw_dir
    fp = open(authorized_keys, 'a')
    fp.write(''.join(['%s%s\n' % (key_prefix, key) for key in keys]))
    fp.close()

    os.chown(authorized_keys, pwent.pw_uid, pwent.pw_gid)

    os.umask(saved_umask)

def main():
    ec2 = ec2init.EC2Init()

    user = ec2.get_cfg_option_str('user')
    disable_root = ec2.get_cfg_option_bool('disable_root', True)

    try:
        keys = ec2.get_ssh_keys()
    except Exception, e:
        sys.exit(1)

    if user:
        setup_user_keys(keys, user, '')
     
    if disable_root:
        key_prefix = 'command="echo \'Please login as the ubuntu user rather than root user.\';echo;sleep 10" ' 
    else:
        key_prefix = ''

    setup_user_keys(keys, 'root', key_prefix)

if __name__ == '__main__':
    main()
