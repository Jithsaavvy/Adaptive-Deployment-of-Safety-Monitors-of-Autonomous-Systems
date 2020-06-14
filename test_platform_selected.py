import unittest
from Code_sdp import *
import argparse
from unittest.mock import MagicMock

class TestContext_Monitor(unittest.TestCase):
    def test_platform_selector(self):
        # Initialize the repository object
        repo_obj=Repository()
        # Create  platform selector class object 
        platform_selector_obj = Platform_Selector(repo_obj,"./platforms.mzn")
        # Create a mock dummy function
        platform_selector_obj._selected_platform = MagicMock(return_value = [[1, 1, 50, 400, 1, 1, 0, 0, 10], [2, 0, 100, 100, 2, 2, 2, 2, 100], [1, 1, 50, 400, 1, 1, 0, 0, 10]])
        #passing the values to dummy variable
        platforms = platform_selector_obj._selected_platform()
        # We have selected the deployment platform
        platform_selector_obj.select_deployment_platform()
        self.assertEqual(platforms[0][0],1)
        self.assertEqual(platforms[1][0],2)
        self.assertEqual(platforms[2][0],1)

if __name__ == '__main__':
    
    unittest.main()

    