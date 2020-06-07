#General Skeleton for Adaptive Deployment of Safety Monitors 

from abc import ABC,abstractmethod
from custom_dtypes import SafetyMonitor,Sensors,Platforms
from minizinc import Instance, Model, Solver

#Provide the contextual information needed for selection and deployment.
class Context_Monitor:
    def __init__(self,repo_image):
        #Initially the robot's context monitor is null
        self.__gripper_status = None
        self.__robot_in_motion = None
        self.__finger_open = None
        self.__time_stamp = None
        self.__repo_image=repo_image

    def get_robot_status(self):
        #Robot senses the current state of its environment
        #Initially the sensed data is provided explicitly
        self.__gripper_status=True
        self.__robot_in_motion=False
        self.__finger_open=True

    def update_info_to_repo(self):
        #Updates the current state of the robot to the repository
        self.__repo_image.update_context(self.__gripper_status,self.__robot_in_motion,self.__finger_open)


#Repository contains information for deployment. It is the central component in the architecture. Every components updates the information to the repository. 
class Repository():
    def __init__(self, active_safety_monitor = SafetyMonitor.NO_SELECTION, active_sensor = Sensors.NO_SELECTION,
                 current_context = [False, False, False],fixed_deployment = True,
                 safety_monitor_platform = Platforms.NO_SELECTION):

        self.__active_safety_monitor = active_safety_monitor
        self.__active_sensor = active_sensor
        self.__safety_monitor_platform = safety_monitor_platform
        self.__current_context = current_context
        self.__fixed_deployment = fixed_deployment

    #Setter methods for updating current context, safety monitor and platform information for deployment from other componenents
    def update_context(self,gripper_status:bool,robot_motion:bool,finger_open=bool):
        self.__current_context = gripper_status,robot_motion,finger_open

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
        self.__current_context = None
        self.__selected_safety_monitor=SafetyMonitor.NO_SELECTION
        self.__repo_image=repo_image
    
    def query_repository(self):
        self.__current_context=self.__repo_image.get_current_context()

    def select_safety_monitor(self):
        if(self.__current_context==(True,False,True)):
            self.__selected_safety_monitor=SafetyMonitor.FORCE_SLIP

        elif(self.__current_context==(False,True,False)):
            self.__selected_safety_monitor=SafetyMonitor.TACTILE_SLIP

        else:
            self.__selected_safety_monitor=SafetyMonitor.FUSED_SLIP
 
    def update_repository(self):
        self.__repo_image.update_current_safety_monitor(self.__selected_safety_monitor)


#Contains definition for selecting the platform based on the selected safety monitor. The selected platform information is updated in the repository.
#Checks and returns the platforms that satisfy the given requirements.
#It is achieved by solving Constraint Satisfaction Problem (CSP). CSP is implemented using MiniZinc(mzn) library.
#The requirements are formulated into suitable constraints and platforms that satisfy the given constraints will be selected.
class Platform_Selector(Selector):
    def __init__(self, repo_image):
        #Initially the attributes are set to null and no safety monitor and platform is selected by default.
        self.__current_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = repo_image
        self.__platform = SafetyMonitor.NO_SELECTION

    def query_repository(self):
        self.__current_safety_monitor = self.__repo_image.get_active_safety_monitor()

    def select_deployment_platform(self):
        #Obtains output from minizinc regarding the selected platform 
        selected_platform = self.platform_selected()
        if self.__current_safety_monitor == SafetyMonitor.FORCE_SLIP:
            self.__platform = selected_platform[0][0]
        elif self.__current_safety_monitor == SafetyMonitor.TACTILE_SLIP:
            self.__platform = selected_platform[1][0]
        else:
            self.__platform = selected_platform[2][0]

    def update_repository(self):
        self.__repo_image.update_platform_status(self.__platform)
        
    #Returns the selected platform from minizinc that solves CSP
    def platform_selected(self):
        #Load platfroms model from file
        platforms = Model("./platforms.mzn")
        #Find the MiniZinc solver configuration for Gecode
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
        platform_solutions = []
        for i in result_intermediate:
            platform_solutions.append(i.force_platform)
            platform_solutions.append(i.tactile_platform)
            platform_solutions.append(i.fused_platform)

        return platform_solutions


if __name__ == '__main__':
    
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
    platform_selector_obj=Platform_Selector(repo_obj)
    platform_selector_obj.query_repository()
    platform_selector_obj.select_deployment_platform()
    platform_selector_obj.update_repository()







