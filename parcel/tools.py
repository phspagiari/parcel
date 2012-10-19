# helper utils
from fabric.api import env, local
import requests

BLOCK_SIZE = 8192

def dl(url,filename):
    """download a url from the net and saves it as filename.
    
    Data is streamed so large files can be saved without exhausting memory
    """
    r=requests.get(url)
    assert r.status_code==200
    
    with open(filename,'wb') as fh:
        for data in r.iter_content(BLOCK_SIZE):
            fh.write(data)

def rpush(local, remote):
    """recursively copy local to remote"""
    local("rsync -av '%s' %s@%s:'%s'"%(local,env.user,env.host,remote))
    
def rpull(remote, local):
    """recursively copy remote to local"""
    local("rsync -av %s@%s:'%s' '%s'"%(env.user,env.host,remote,local))
    

