#General Skeleton for Adaptive Deployment of Safety Monitors 

from abc import ABC,abstractmethod
from custom_dtypes import *
from minizinc import Instance, Model, Solver
import argparse


class Context_Monitor:
    """
    Provide the contextual information needed for selection and deployment.
    """
    def __init__(self,repo_image):
        self.__gripper_status = False
        self.__robot_in_motion = False
        self.__time_stamp = 0.0
        self.__repo_image=repo_image

    def get_robot_status(self):
    
        """
        Set the parameters of this variables.
        This method is used to set the status of the gripper and robot motion.
        Robot senses the current state of its environment. Initially the sensed data is provided explicitly 
        Parameters
        ----------
        **params : 
            None
        Returns
        -------
            None
        """

        self.__gripper_status=True
        self.__robot_in_motion=True

    def update_info_to_repo(self):
        """
        This method is used update the state of the robot in the repository method.
        Method takes the updated gripper and robot motion and updates. 
        Parameters
        ----------
        **params : 
            None
        Returns
        -------
            None
        """
        self.__repo_image.update_context(self.__gripper_status,self.__robot_in_motion)

 
class Repository():
    """
    Repository contains information for deployment. It is the central component in the architecture. Every components updates the information to the repository.
    """
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
        self.n_platforms = 4
        self.platforms = set([1,2,3,4])

    
    def update_context(self,gripper_status,robot_motion):
        """
        Setter methods for updating current context, safety monitor and platform information 
        for deployment from other componenents. 
        Parameters
        ----------
        gripper_status: bool
            The gripper has status either true or false that means gripper is open or closed condition.
        robot_motion:
            The robot motion has status either true or false that means robot is moving or stopped.
        Returns
        -------
            None
        """
        self.__current_context = gripper_status,robot_motion

    def update_current_safety_monitor(self,current_safety_monitor):
        """
        Setter methods for updating current active safety monitor and prints the selected safety monitor. 
        Parameters
        ----------
        current_safety_monitor: int
            The current_safety_monitor is the safety monitor that is currently active. 
            Each integer value represent unique safety monitor.
        Returns
        -------
            None
        """
        self.__active_safety_monitor = current_safety_monitor
        print("Selected safety monitor:",self.__active_safety_monitor)

    def update_platform_status(self,safety_monitor_platform):
        """
        Setter methods for updating current platform status and prints the selected safety monitor to deploy. 
        Parameters
        ----------
        safety_monitor_platform: int
            The safety_monitor_platform is the platform that needs to be deployed. 
            Each integer value represent unique platform.
        Returns
        -------
            None
        """
        self.__safety_monitor_platform = safety_monitor_platform
        print("\nSelected platform to deploy {0}: PF{1} ".format(self.__active_safety_monitor,self.__safety_monitor_platform))

    def get_active_safety_monitor(self):
        """
        Getter methods for obtaining active safety monitor . 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            current active safety monitor
        """
        return self.__active_safety_monitor

    def get_current_context(self):
        """
        Getter methods for obtaining current context. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            current context
        """
        return self.__current_context

    def __notify_changes(self):
        pass
 
class Selector(ABC):
    @abstractmethod
    def query_repository(self):
        """
        Query repository interface. 
        Interface for querying repository and acts as a communicator between repository and other components of the system.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        pass

    @abstractmethod
    def update_repository(self):
        """
        Query repository interface. 
        Interface for updating repository and acts as a communicator between repository and other components of the system.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        pass

class Safety_Monitor_Selector(Selector):
    """
    Contains definition for selecting the safety monitor based on the current context. The selected safety monitor information is updated in the repository.
    """
    def __init__(self,repo_image):
        """ 
        Initially the attributes are set to null and no safety monitor is selected by default.
        Current context contains gripper_status,robot_motion
        """
        self.__current_context = (False,False)
        self.__selected_safety_monitor=SafetyMonitor.NO_SELECTION
        self.__repo_image=repo_image
    
    def query_repository(self):
        """
        The query repository method update the current context by getting the current context from repository object. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__current_context=self.__repo_image.get_current_context()

    def select_safety_monitor(self):
        """
        The select safety monitor method checks the status of the current context of gripper and robot motion.
        Once the status has recieved appropriate safety monitor is passed onto the selected safety monitor variable. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        if(self.__current_context==(True,True)):
            self.__selected_safety_monitor=SafetyMonitor.FORCE_SLIP

        elif(self.__current_context==(True,False)):
            self.__selected_safety_monitor=SafetyMonitor.TACTILE_SLIP

        else:
            self.__selected_safety_monitor=SafetyMonitor.FUSED_SLIP
 
    def update_repository(self):
        """
        The update_repository method updates the current safety monitor by extracting the selected safety monitor. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__repo_image.update_current_safety_monitor(self.__selected_safety_monitor)

class Platform_Selector(Selector):
    """
    Contains definition for selecting the platform based on the selected safety monitor.
    The selected platform information is updated in the repository.
    Checks and returns the platforms that satisfy the given requirements.
    It is achieved by solving Constraint Satisfaction Problem (CSP). CSP is implemented using MiniZinc(mzn) library.
    The requirements are formulated into suitable constraints and platforms that satisfy the given constraints will be selected.
    
    """
    def __init__(self, repo_image, minizinc_model):
        """
        Initially the attributes are set to null and no safety monitor and platform is selected by default.
        
        """
        self.__current_safety_monitor = SafetyMonitor.NO_SELECTION
        self.__repo_image = repo_image
        self.__platform = Platforms.NO_SELECTION
        self.__minizinc_model = minizinc_model
        self.__selected_platform = None

    def query_repository(self):
        """
        The query_repository method get the active safety monitor and updates the current safety monitor. 
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__current_safety_monitor = self.__repo_image.get_active_safety_monitor()

    def select_deployment_platform(self): 
        """
        The select deployment platform method get the selected paltform by calling platform selected method. 
        Once the paltform selected is obtained is compared with the current safety monitor and appropriate safety monitor
        is updated to the platform.
        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__selected_platform = self.__platform_selected()
        if self.__current_safety_monitor == SafetyMonitor.FORCE_SLIP:
            self.__platform = self.__selected_platform[0][0]
        elif self.__current_safety_monitor == SafetyMonitor.TACTILE_SLIP:
            self.__platform = self.__selected_platform[1][0]
        else:
            self.__platform = self.__selected_platform[2][0]
    
    def update_repository(self):
        """
        The update repository method update the platform status by passing the paltform variable values. 

        Parameters
        ----------
        **params: 
            None

        Returns
        -------
            None
        """
        self.__repo_image.update_platform_status(self.__platform)
        
    def __platform_selected(self):
        """
        The paltform selected method intialises the solver, create a instance and pass appropriate varibles values.
        Insatnce is solved and results are appended to appropriate variable.
        Returns the selected platform from minizinc that solves CSP. 

        Parameters
        ----------
        **params: 
            None

        Returns
        -------
        platform_solutions: list
            Contains all the solution obtained from the CSP solver.
        """
        #Load platfroms model from file
        minizinc_file = "./"+str(self.__minizinc_model)
        platforms = Model(minizinc_file)
        #Find the MiniZinc solver configuration for Gecode
        gecode = Solver.lookup("gecode")
        # Create an Instance of the platforms model for Gecode
        instance = Instance(gecode, platforms)
        instance["min_force_sensor_count"] = self.__repo_image.min_force_sensor_count
        instance["min_tactile_sensor_count"] = self.__repo_image.min_tactile_sensor_count
        instance["min_memory_fused"] = self.__repo_image.min_memory_fused
        instance["n_platforms"] = self.__repo_image.n_platforms
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
    """
    minizinc model is loaded from the terminal 
    """
    args = argparse.ArgumentParser("Description: Please include the constraint satisfaction minizn solver file ")
    args.add_argument("--model",required = True, help = "Provide the name of the Minizn platform model and make sure the file is in main code folder")
    minizinc_model = vars(args.parse_args())
    
    repo_obj=Repository()
    """
    The instance of repository id is passed to context monitor, so that the information from context monitor can be updated to the repository
    """
    context_monitor_obj=Context_Monitor(repo_obj)
    context_monitor_obj.get_robot_status()
    context_monitor_obj.update_info_to_repo()

    """
    The safety monitor selector receives current context info from repository and selects safety monitor ans updates them in the repository.
    """
    safety_monitor_obj=Safety_Monitor_Selector(repo_obj)
    safety_monitor_obj.query_repository()
    safety_monitor_obj.select_safety_monitor()
    safety_monitor_obj.update_repository()

    """
    The platform selector receives selected safety monitor info from repository and selects safety suitable platform using minizinc and updates them in the repository.
    """
    platform_selector_obj=Platform_Selector(repo_obj,minizinc_model["model"])
    platform_selector_obj.query_repository()
    platform_selector_obj.select_deployment_platform()
    platform_selector_obj.update_repository()

