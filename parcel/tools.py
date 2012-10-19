# helper utils

import requests

def dl(url,filename):
    """download a url from the net and saves it as filename.
    
    Data is streamed so large files can be saved without exhausting memory
    """
    r=requests.get(url)
    assert r.status_code==200
    
    with open(filename,'wb') as fh:
        for data in r.iter_content(8192):
            fh.write(data)
        
    
    
