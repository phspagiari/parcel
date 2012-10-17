import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.contrib.files import sed

class Hg(object):
    def __init__(self,path):
        self.path = path

    @property
    def branch(self):
        with lcd(self.path):
            return local('hg branch',capture=True).strip()

    @property
    def log(self):
        with lcd(self.path):
            return dict([
                (a.strip(),b.strip()) 
                for a,b in [
                    line.split(':',1) for line in local('hg log | head -4', capture=True).splitlines()
                ]
            ])
		
    @property
    def logs(self):
        with lcd(self.path):
            logs = local('hg log', capture=True).split("\n\n")
            return [
                dict([
                    (a.strip(),b.strip()) 
                    for a,b in [
                        line.split(':',1) for line in chunk.split('\n')
                    ]
                ]) for chunk in logs
            ]
	
    @property
    def pull(self):
        with lcd(self.path):
            return local('hg pull',capture=True).splitlines()
    
    @property
    def update(self):
        with lcd(self.path):
            return dict([
                (cat,int(num))
                for num,cat in [
                    str.split(' files ') 
                    for str in local('hg update',capture=True).split(', ')
                ]
            ])

class Git(object):
    def __init(self,path):
        self.path = path

def repo(path):
    content = os.listdir(path)
    if '.hg' in content:
        return Hg(path)
    if '.git' in content:
        return Git(path)
    return repo(os.path.realpath(path+'/..'))			# recurse back a directory
