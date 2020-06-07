import unittest
from Code_sdp import *

class TestContext_Monitor(unittest.TestCase):
    def test_getrobot_status(self):
        # Test get robot status when self.gripper_status, self.robot_in_motion, self.finger_open and self.time_stamp
        image_repo = Context_Monitor(Repository())
        image_repo.get_robot_status()
        self.assertEqual(image_repo.gripper_status,True)
        self.assertEqual(image_repo.robot_in_motion,False)
        self.assertEqual(image_repo.finger_open,True)
        self.assertEqual(image_repo.time_stamp,None)

if __name__ == '__main__':
   unittest.main()