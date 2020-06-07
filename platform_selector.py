from selector import Selector
from custom_dtypes import *
# print(driver.platform_selected())

# class Platform_Selector(Selector):
class Platform_Selector(Selector):

    def __init__(self, Repository):
        self.__current_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = Repository
        self.__platform = SafetyMonitor.NO_SELECTION

    def query_repository(self,):
        self.__current_safety_monitor = self.__repo_image.get_active_safety_monitor()

    def update_repository(self,):

        self.__repo_image.update_current_safety_monitor(self.platform)

    def select_deployment_platform(self, ):
        minizn_output = self.platform_selected()
        if self.__current_safety_monitor == 1:
                self.__platform = minizn_output[0][0]
        elif self.__current_safety_monitor == 2:
                self.__platform = minizn_output[1][0]
        else:
                self.__platform = minizn_output[2][0]
        print("Selected platform:",self.__platform)
        

    def platform_selected(self):
        # Load platfroms model from file
        platforms = Model("./platforms.mzn")

        # # Find the MiniZinc solver configuration for Gecode
        gecode = Solver.lookup("gecode")
        # # Create an Instance of the platforms model for Gecode
        instance = Instance(gecode, platforms)
        # Assign 4 to n
        instance["name"] = 1
        instance["min_force_sensor_count"] = 1
        instance["min_tactile_sensor_count"] = 100
        instance["min_memory_fused"] = 400
        instance["np"] = 4
        instance["platforms"] = set([1,2,3,4])
        # solve to get the general solution
        result_general = instance.solve()
        # solve to find the intermediate solution
        result_intermediate = instance.solve(intermediate_solutions=True)

        u = []
        for i in result_intermediate:
            # print(i)
            # print(i.force_platform)
            u.append(i.force_platform)
            # print(i.tactile_platform)
            u.append(i.tactile_platform)
            # print(i.fused_platform)
            u.append(i.fused_platform)

        return u