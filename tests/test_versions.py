import unittest

from parcel.versions import Version

class VersionTestSuite(unittest.TestCase):
    """Versions test cases."""

    def test_instantiate(self):
        for v,nv in __TEST_DATA__:
            Version(v)

    def test_string_cast(self):
        for v,nv in __TEST_DATA__:
            self.assertEqual( str(Version(v)), v)

    def test_increments(self):
        for v,nv in __TEST_DATA__:
            self.assertEqual( Version(v).next().version, nv)
	
    def test_empty_initial_value(self):
        for v, nv in [(None,"0.0.1"), ("","0.0.1")]:
            self.assertEqual( str(Version(v)), "0.0.0")
            self.assertEqual( Version(v).next().version, nv)


# example versions from distutils.versions docs plus a few more
# (input, expected_outut)
__TEST_DATA__ = [
    ("0.4","0.5"),
    ("0.4.0","0.4.1"),
    ("0.4.1","0.4.2"),
    ("0.5a1","0.5a2"),
    ("0.5b3","0.5b4"),
    ("0.5","0.6"),
    ("0.9.6","0.9.7"),
    ("1.0","1.1"),
    ("1.0.4a3","1.0.4a4"),
    ("1.0.4b1","1.0.4b2"),
    ("1.0.4","1.0.5"),
    ("0","1"),
    ("0.1","0.2"),
    ("0.4","0.5"),
    ("1.42","1.43"),
    ("2.005.23","2.005.24"),
    ("2.01-4.5","2.01-4.6"),
    ("2.21-5.alpha-7","2.21-5.alpha-8"),
    ("1.5.1","1.5.2"),
    ("1.5.2b2","1.5.2b3"),
    ("161","162"),
    ("3.10a","3.11a"),
    ("8.02","8.03"),
    ("3.4j","3.5j"),
    ("1996.07.12","1996.07.13"), # TODO will eventually increment past valid date
    ("3.2.pl0","3.2.pl1"),
    ("3.1.1.6","3.1.1.7"),
    ("2g6","2g7"),
    ("11g","12g"),
    ("0.960923","0.960924"),
    ("2.2beta29","2.2beta30"),
    ("1.13++","1.14++"),
    ("5.5.kw","5.6.kw"),
    ("2.0b1pl0","2.0b1pl1"),
    ("package-1.2.1-1ubuntu2","package-1.2.1-1ubuntu3"),
    ("bob","bob1"),
    ("alice2", "alice3")
    ]
