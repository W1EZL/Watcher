import os

# checks if currently in afk mode, only returns true once
def get_afk_status(afk_active, timeout):
    if (is_afk(timeout)):
        return True
    elif returned_from_afk(afk_active, timeout):
        return True
    else:
        return False 

def returned_from_afk(afk_active, timeout):
    has_returned = (afk_active and not (is_afk(timeout)))
    return has_returned

def is_afk(timeout):
    afk_binary_path = '/usr/share/Watcher/afk_timer'
    timeout = timeout * 60 * 1000
    #If the AFK feature is installed
    if os.path.isfile(afk_binary_path):
        return (int((os.popen(afk_binary_path).read())) > timeout)
    return False
