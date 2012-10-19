# -*- coding: utf-8 -*-
from distutils.version import LooseVersion

class Version:
    def __init__(self, version):
        if version is None or version == "":
            self.version = "0.0.0"
        else:
            self.version = str(version)

    def __str__(self):
        return self.version

    def next(self):
        """Returns the next version by finding rightmost number in version string and incrementing by 1"""

        new_version = self.version

        # get right most digits
        rmd = self.right_most_digits(new_version)

        if rmd is not None:
            # split string on rightmost digit and rejoin with rmd+1
            new_version = str(rmd+1).join(self.version.rsplit(str(rmd),1))
        else:
            new_version = self.version + "1"

        assert LooseVersion(new_version) > LooseVersion(self.version)

        return Version(new_version)

    def right_most_digits(self, version):

        v = LooseVersion(version)
        for x in reversed(v.version):
            if isinstance(x, int):
                return x
        
        return None        
