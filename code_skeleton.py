#General Skeleton for Adaptive Deployment of Safety Monitors 

#Repository contains knowledge for deployment. It is the central component in the architecture. 
#It detects the safety monitors and transfers information to other components for deployment 
class Repository():
    #Create an entry in the repository when safety monitor is detected
    def create_entry(self):
        slip_detector='Force_slip_detector'
        if(slip_detector==""):
            print("None detected")
        return slip_detector

    def display_entry(self):
        print("New information is created in the repository")

    #Updates and notifies about the changes in repository to all other components in the system.
    def notify(self):
        print("Notified to all components in the repository")

#Contains definition for selecting the safety monitor and finding the suitable platform to deploy.
class Safety_monitor():
    #Selection of relevant safety monitor
    def selection(self):
        
        #The detected information is passed to this component from repository 
        obj=Repository()
        detected_info=obj.create_entry()
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
    repo_obj=Repository()
    #Repository detects the detector information
    dep=repo_obj.create_entry()
    #Information about the detected is displayed 
    repo_obj.display_entry()
    
    Safety_monitor_obj=Safety_monitor()
    #The safety monitor is selected using the detected information from the repository
    selected_detector=Safety_monitor_obj.selection()
    #Acceptable platform that meets the requirements is obtained and deployed
    acceptable_platform=Safety_monitor_obj.get_acceptable_platform(selected_detector)

    Safety_monitor_obj.deploy(selected_detector,acceptable_platform)
    
    #The repository notifies all the components in the system
    repo_obj.notify()

