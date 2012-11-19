import os
import errno

from parcel.tools import dl

class FileCache(object):
    cache_dir="/tmp/parcel-cache"
    
    def __init__(self,cachedir=None):
        if cachedir:
            self.cache_dir=cachedir
        
        try:
            os.makedirs(self.cache_dir)
        except OSError, ose:
            if ose.errno==errno.EEXIST:
                pass
            else:
                raise ose
        
    def download(self,url):
        filename=url.rsplit('/',1)[-1]
        dl(url,os.path.join(self.cache_dir,filename))
        
    def is_cached(self,filename):
        return filename in os.listdir(self.cache_dir)
        
    def get(self,url):
        filename = url.rsplit('/',1)[-1]
        
        if self.is_cached(filename):
            return os.path.join(self.cache_dir,filename)
            
        self.download(url)
        return os.path.join(self.cache_dir,filename)

cache = FileCache()
