import unittest

from tailor.versions import Version

class VersionTestSuite(unittest.TestCase):
    """Versions test cases."""

    def test_instantiate(self):
        Version()
        Version("0.1")
        Version("1.42")
        Version("2.005.23")
        Version("2.01-4.5")
        Version("2.21-5.alpha-7")

    def test_string_cast(self):
        self.assertEqual( str(Version()), "0" )

        for init in ('0.1','1.4','2.005.34','2.01-4.5','2.21-5.alpha-7'):
            self.assertEqual( str(Version(init)), init )
	
    def test_add_point(self):
        self.assertEqual( str(Version("1.56").point(5)), "1.56.5" )
        self.assertEqual( str(Version("2.210.0alpha").point("002")),"2.210.0alpha.002")
		
