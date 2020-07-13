# Adaptive-Deployment-of-Safety-Monitors-for-Autonomous-Systems
![alt text](https://www.materialhandling247.com/images/product/righthand-robotics-rightpick-robot-arm-3.jpg)
**Figure 1:** Robot arm picking an object [3]

Adaptive deployment of safety monitors for autonomous systems solves the problem of deploying safety critical software for an autonomous system. The software can be re-deployed by the robots autonomously at runtime that accounts for changing requirements urged by their task, platform and environment [1]. The problem is formulated as a Constraint Satisfaction Problem (CSP). Constraint Satisfaction Problems are mathematical questions defined as a set of objects whose state must satisfy a number of constraints or limitations [2]. It is achieved using a library called **[MiniZinc](https://www.minizinc.org/)**.

Minizinc is a free and open source constraint modeling language. It can be used to model constraint satisfaction and optimization problems in a higher level. 

# Dependencies:
 - Python (>= 3.6)
 - Minizinc (2.4.3)
 - Pandas (1.0.7)
 - Tabulate (0.8.7)
 
# Minizinc as an IDE:
Minizinc comes with a simple Integrated Development Environment (IDE), which makes it easier for developing and executing constraint models. It is user friendly.

Minizinc can be installed as bundled package that consists of Minizinc library, IDE, solvers and interfaces.

To install the bundled package, download it from [here](https://www.minizinc.org/software.html) 

OS specific downloads -
- Windows - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundled-setup-win64.exe)
- Linux - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundle-linux-x86_64.tgz)
- Mac OS - [Click Here](https://github.com/MiniZinc/MiniZincIDE/releases/download/2.4.3/MiniZincIDE-2.4.3-bundled.dmg)

For more information regarding installation, Visit [Minizinc Documentation.](https://www.minizinc.org/doc-2.4.3/en/installation.html)

# Minizinc Python:
It is a python package that allows accessing all of Minizinc's functionalities directly from Python. It provides an interface from Python to MiniZinc driver. It provides easy access to Minizinc using native Python structures.

# User Installation:
Use pip to install the Minizinc for Python -
```sh
pip install minizinc
```
For more information, Visit [PyPI.org](https://pypi.org/project/minizinc/)

The constraints are defined in the minizinc (.mzn) files. The .mzn files can be integrated with python using the python library for minizinc. The constraints can be solved using various solvers and it returns the best assignment or solution that satisfies the given constraints.

## How to use it:
**Files**
- The safety monitors, sensors and platforms are available as enumerations in **custom_dtypes.py**
- Constraints are defined in **platforms.mzn**. It consists of the CSP part and outputs the best suitable platform for deployment.
- The data for platforms.mzn to work is given in **platforms.dzn** which contains platform names and its properties. This file is used only used when the MiniZinc model is executed independently without getting called from the system (python code).
- **input.csv** contains the list of robot’s context at every intervals along with memory available at each platform. 
    - **Example**: The current context is (True, True) => (gripper_status “False = Closed or True-Open”, robot_in_motion “True = Not stationary or False = stationary”)
- The system is realized in **adaptive_deployment.py**

**Usage** 
- Clone the repository to the local machine using ```git clone.```
- Make sure Python 3 is installed followed by pandas,tabulate and minizinc packages.Pandas and tabulate can be installed using the following commands:
```sh
pip install pandas
pip install tabulate
```

- Execute adaptive_deployment.py file. Provide the path of the Minizn platform model as the command line argument.
```sh
python adaptive_deployment.py  --model mini_zn_model/platforms.mzn --input_data input.csv
```

# References:
[1]. Hochgeschwender, Nico. “Adaptive Deployment of Safety Monitors for Autonomous Systems.” International Conference on Computer Safety, Reliability, and Security, 2019, pp. 346–357. <br>
[2] https://en.wikipedia.org/wiki/Constraint_satisfaction_problem <br>
[3] https://www.materialhandling247.com/images/product/righthand-robotics-rightpick-robot-arm-3.jpg
