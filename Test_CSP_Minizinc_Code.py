import unittest
from CSP_Minizinc_Code import *

class Test_Safety_Monitor(unittest.TestCase):
    
    repo=Repository()
    context_monitor=Context_Monitor(repo)
    context_monitor.get_robot_status()
    context_monitor.update_info_to_repo()
    safety_monitor=Safety_Monitor_Selector(repo)
    safety_monitor.query_repository()
    safety_monitor.select_safety_monitor()
    current_safety_monitor=str(safety_monitor.get_safety_monitor_unittest())
 

    def test_select_safety_monitor(self):
        safety_monitor_list=['SafetyMonitor.FUSED_SLIP','SafetyMonitor.FORCE_SLIP','SafetyMonitor.TACTILE_SLIP']
        result = any(i in self.current_safety_monitor for i in safety_monitor_list) 
        self.assertTrue(result)
        

if __name__ == '__main__':
   unittest.main()
   