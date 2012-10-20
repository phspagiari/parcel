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
