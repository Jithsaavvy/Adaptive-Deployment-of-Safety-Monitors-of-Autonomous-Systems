#General Skeleton for Adaptive Deployment of Safety Monitors 

from abc import ABC,abstractmethod
from custom_dtypes import *
from minizinc import Instance, Model, Solver
import argparse

#Provide the contextual information needed for selection and deployment.
class Context_Monitor:
    def __init__(self,repo_image):
        #Initially the robot's context monitor is null
        self.__gripper_status = False
        self.__robot_in_motion = False
        self.__time_stamp = 0.0
        self.__repo_image=repo_image

    def get_robot_status(self):
        #Robot senses the current state of its environment
        #Initially the sensed data is provided explicitly
        self.__gripper_status=True
        self.__robot_in_motion=True

    def update_info_to_repo(self):
        #Updates the current state of the robot to the repository
        self.__repo_image.update_context(self.__gripper_status,self.__robot_in_motion)


#Repository contains information for deployment. It is the central component in the architecture. Every components updates the information to the repository. 
class Repository():
    def __init__(self, active_safety_monitor = SafetyMonitor.NO_SELECTION, active_sensor = Sensors.NO_SELECTION,
                 current_context = [False, False],fixed_deployment = True,
                 safety_monitor_platform = Platforms.NO_SELECTION):

        self.__active_safety_monitor = active_safety_monitor
        self.__active_sensor = active_sensor
        self.__safety_monitor_platform = safety_monitor_platform
        self.__current_context = current_context
        self.__fixed_deployment = fixed_deployment
        self.min_force_sensor_count = 1
        self.min_tactile_sensor_count = 100
        self.min_memory_fused = 400
        self.np = 4
        self.platforms = set([1,2,3,4])

    #Setter methods for updating current context, safety monitor and platform information for deployment from other componenents
    def update_context(self,gripper_status:bool,robot_motion:bool):
        self.__current_context = gripper_status,robot_motion

    def update_current_safety_monitor(self,current_safety_monitor):
        self.__active_safety_monitor = current_safety_monitor
        print("Selected safety monitor:",self.__active_safety_monitor)

    def update_platform_status(self,safety_monitor_platform):
        self.__safety_monitor_platform = safety_monitor_platform
        print("\nSelected platform to deploy {0}: PF{1} ".format(self.__active_safety_monitor,self.__safety_monitor_platform))

    #Getter methods for obtaining current context and safety monitor information from other componenents
    def get_active_safety_monitor(self):
        return self.__active_safety_monitor

    def get_current_context(self):
        return self.__current_context

    def __notify_changes(self):
        pass


#Interface for querying and updating repository and acts as a communicator between repository and other components of the system 
class Selector(ABC):
    @abstractmethod
    def query_repository(self):
        pass

    @abstractmethod
    def update_repository(self):
        pass

#Contains definition for selecting the safety monitor based on the current context. The selected safety monitor information is updated in the repository.
class Safety_Monitor_Selector(Selector):
    def __init__(self,repo_image):
        #Initially the attributes are set to null and no safety monitor is selected by default.
        self.__current_context = (False,False)
        self.__selected_safety_monitor=SafetyMonitor.NO_SELECTION
        self.__repo_image=repo_image
    
    def query_repository(self):
        self.__current_context=self.__repo_image.get_current_context()

    def select_safety_monitor(self):
        if(self.__current_context==(True,True)):
            self.__selected_safety_monitor=SafetyMonitor.FORCE_SLIP

        elif(self.__current_context==(True,False)):
            self.__selected_safety_monitor=SafetyMonitor.TACTILE_SLIP

        else:
            self.__selected_safety_monitor=SafetyMonitor.FUSED_SLIP
 
    def update_repository(self):
        self.__repo_image.update_current_safety_monitor(self.__selected_safety_monitor)

    #Method for returning the selected safety monitor for performing unit test
    def get_safety_monitor_unittest(self):
        return self.__selected_safety_monitor


#Contains definition for selecting the platform based on the selected safety monitor. The selected platform information is updated in the repository.
#Checks and returns the platforms that satisfy the given requirements.
#It is achieved by solving Constraint Satisfaction Problem (CSP). CSP is implemented using MiniZinc(mzn) library.
#The requirements are formulated into suitable constraints and platforms that satisfy the given constraints will be selected.
class Platform_Selector(Selector):
    def __init__(self, repo_image, minizinc_model):
        #Initially the attributes are set to null and no safety monitor and platform is selected by default.
        self.__current_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = repo_image
        self.__platform = Platforms.NO_SELECTION
        self.__minizinc_model = minizinc_model
        self._selected_platform = None

    def query_repository(self):
        self.__current_safety_monitor = self.__repo_image.get_active_safety_monitor()

    def select_deployment_platform(self):
        #Obtains output from minizinc regarding the selected platform 
        self._selected_platform = self.__platform_selected()
        if self.__current_safety_monitor == SafetyMonitor.FORCE_SLIP:
            self.__platform = self._selected_platform[0][0]
        elif self.__current_safety_monitor == SafetyMonitor.TACTILE_SLIP:
            self.__platform = self._selected_platform[1][0]
        else:
            self.__platform = self._selected_platform[2][0]
    
    def update_repository(self):
        self.__repo_image.update_platform_status(self.__platform)
        
    #Returns the selected platform from minizinc that solves CSP
    def __platform_selected(self):
        #Load platfroms model from file
        minizinc_file = "./"+str(self.__minizinc_model)
        platforms = Model(minizinc_file)
        #Find the MiniZinc solver configuration for Gecode
        gecode = Solver.lookup("gecode")
        # # Create an Instance of the platforms model for Gecode
        instance = Instance(gecode, platforms)
        instance["min_force_sensor_count"] = self.__repo_image.min_force_sensor_count
        instance["min_tactile_sensor_count"] = self.__repo_image.min_tactile_sensor_count
        instance["min_memory_fused"] = self.__repo_image.min_memory_fused
        instance["np"] = self.__repo_image.np
        instance["platforms"] = self.__repo_image.platforms
        # solve to get the general solution
        result_general = instance.solve()
        # solve to find the intermediate solution
        result_intermediate = instance.solve(intermediate_solutions=True)
        platform_solutions = []
        for i in result_intermediate:
            platform_solutions.append(i.force_platform)
            platform_solutions.append(i.tactile_platform)
            platform_solutions.append(i.fused_platform)

        return platform_solutions


if __name__ == '__main__':
    
    args = argparse.ArgumentParser("Desciption: Please include the constraint satisfaction minizn solver file ")
    args.add_argument("--model",required = True, help = "Provide the name of the Minizn platform model and make sure the file is in main code folder")
    minizinc_model = vars(args.parse_args())
    
    repo_obj=Repository()
    #The instance of repository id is passed to context monitor, so that the information from context monitor can be updated to the repository
    context_monitor_obj=Context_Monitor(repo_obj)
    context_monitor_obj.get_robot_status()
    context_monitor_obj.update_info_to_repo()

    #The safety monitor selector receives current context info from repository and selects safety monitor ans updates them in the repository.
    safety_monitor_obj=Safety_Monitor_Selector(repo_obj)
    safety_monitor_obj.query_repository()
    safety_monitor_obj.select_safety_monitor()
    safety_monitor_obj.update_repository()

    #The platform selector receives selected safety monitor info from repository and selects safety suitable platform using minizinc and updates them in the repository.
    platform_selector_obj=Platform_Selector(repo_obj,minizinc_model["model"])
    platform_selector_obj.query_repository()
    platform_selector_obj.select_deployment_platform()
    platform_selector_obj.update_repository()

