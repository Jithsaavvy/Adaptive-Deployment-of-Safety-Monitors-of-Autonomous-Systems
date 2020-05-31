#General Skeleton for Adaptive Deployment of Safety Monitors 

import copy
from custom_dtypes import *
#Repository contains knowledge for deployment. It is the central component in the architecture. 
#It contains the information about the safety monitors and transfers information to other components for deployment 
class Repository():

    def __init__(self, active_safety_monitor = SafetyMonitor.NO_SELECTION, active_sensor = Sensors.NO_SELECTION,
                 current_context = [False, False, False],fixed_deployment = True,
                 safety_monitor_pltfrm = Platforms.NO_SELECTION):

        self.__active_safety_monitor = active_safety_monitor
        self.__active_sensor = active_sensor
        self.__safety_monitor_plfrm = safety_monitor_pltfrm
        self.__current_context = current_context
        self.__fixed_deployment = fixed_deployment

    def update_context(self,gripper_status:bool,robot_motion:bool,finger_open=bool):
        self.__current_context = gripper_status,robot_motion,finger_open

    def update_current_safety_monitor(self,current_safety_monitor):
        self.__active_safety_monitor = current_safety_monitor

    def update_platform_status(self,safety_monitor_platform):
        self.__safety_monitor_plfrm = safety_monitor_platform

    def get_active_safety_monitor(self):
        return self.__active_safety_monitor

    def get_current_context(self):
        return self.__current_context

    def __notify_changes(self):
        pass

#Contains definition for selecting the safety monitor and finding the suitable platform to deploy.
class Safety_monitor():
    #Returns the selection of relevant safety monitor
    def selection(self,detected_info):     
        #The information is passed to this component from repository 
        if(detected_info=="Force_slip_detector"):
            print("Force Slip Detector is selected")
            selected_safety_monitor=detected_info
        else:
            print("Tactile Slip Detector is selected")
            selected_safety_monitor=detected_info
        return selected_safety_monitor

    #Checks and returns the platforms that satisfy the given requirements. 
    #It is achieved using Constraint Satisfaction Problem (CSP). CSP is implemented using MiniZinc(mzn) library.
    #The requirements are formulated into suitable constraints and platforms that satisfy the given constraints will be selected. 
    def get_acceptable_platform(self,detector):
        if(detector=="Force_slip_detector"):
            platform='PF_1'
            print("The suitable platform is PF_1")
        elif(detector=="tactile slip detector"):
            platform='PF_2'
            print("The suitable platform is PF_2")
        else:
            print("No platforms meet the requirements")
        return platform

    #The safety monitor will be deployed in the selected platform
    def deploy(self,detector,platform):
        if(detector!='' or platform!=''):
            print('{0} is deployed succesfully in platform {1}'.format(detector,platform))


if __name__ == '__main__':
    repo_obj = Repository()
    #Entry is created in the repository and information is displayed 
    repo_obj.create_entry()
    
    #Repository pass the information to safety monitor for selection and deployment
    pass_info=repo_obj.pass_entry()
    detector_info=copy.copy(pass_info)
    Safety_monitor_obj=Safety_monitor()
    #The safety monitor is selected using the information obtained from the repository
    selected_detector=Safety_monitor_obj.selection(detector_info)
    #Acceptable platform that meets the requirements is obtained and deployed
    acceptable_platform=Safety_monitor_obj.get_acceptable_platform(selected_detector)
    Safety_monitor_obj.deploy(selected_detector,acceptable_platform)
    
    #The repository notifies all the components in the system
    repo_obj.notify()

