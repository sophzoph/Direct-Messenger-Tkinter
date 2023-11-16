import unittest
import Profile

"""
Unittest module to test all classes and functions
inside of the profile module.
"""

class profile_tester(unittest.TestCase):
    """
    Contains functions to test every function used for the
    storing of profile information using the Profile class.
    """

    def test_save_profile(self):
        """
        Test that saving a profile will correctly save
        a newly created Profile object.
        """
        pass


    def test_load_profile(self):
        """
        Test that loading a profile will allow changing 
        and getting information about the loaded Profile 
        object.
        """
        pass

if __name__ == "__main__":
    unittest.main()