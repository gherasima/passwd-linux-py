
"""
Utility to change/check shadow linux password
"""

import crypt
import spwd


def check(username, old_password):
    try:
        password_org_fulllist = spwd.getspnam(username)[1].split('$')
    except KeyError:
        #print('unknown_username')
        return 'unknown_username'
    try:
        password_org_hash = password_org_fulllist[1]
    except IndexError:
        return 'user_disabled'

    password_org_salt = password_org_fulllist[2]
    password_enq = crypt.crypt(old_password, '$' + password_org_hash + '$' + password_org_salt)

    if password_enq == spwd.getspnam(username)[1]:
        #print('old_password_correct')
        return 'old_password_correct'
    else:
        #print('old_password_incorrect')
        return 'old_password_incorrect'


def change(username, old_password, new_password):

        test_old_password = check(username, old_password)

        if test_old_password == 'old_password_correct':
            import subprocess

            password_org_fulllist = spwd.getspnam(username)[1].split('$')
            try:
                password_org_hash = password_org_fulllist[1]
            except IndexError:
                return 'user_disabled'

            password_new_enq = crypt.crypt(new_password, '$' + password_org_hash + '$' + crypt.mksalt().split('$')[2][:8])

            cmd = 'usermod -p ' + '\'' + password_new_enq + '\'' + ' ' + username
            return_code = subprocess.call(cmd, shell=True)

            if return_code == 0:
                #print('pass_change_success')
                return 'pass_change_success'
            else:
                #print('pass_change_error')
                return 'pass_change_error'
        elif test_old_password == 'old_password_incorrect':
            return 'old_password_incorrect'
        else:
            return 'unknown_username'
