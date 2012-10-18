

class Version:
    def __init__(self,version="0"):
        self.version = version

    def __str__(self):
        return self.version

    def point(self,number):
        self.version = "%s.%s"%(self.version,number)

    def next(self):
        """return the next version"""
        # get the last chunk of numbers from the version string
        numbers = ''.join([c if c in '0123456789' else '-' for c in self.version]).split('-')[-1]

        # truncate string before 'numbers' changes number of digits
        prestring = self.version[:-len(numbers)]

        # the increment
        numbers = str( int(numbers)+1 )
		
        #the new version
        return Version(prestring+numbers)

