%Inbuilt header file
include "table.mzn";

%Thresholds of properties
int: min_force_sensor_count;  
int: min_tactile_sensor_count; 
int: min_memory_fused;               


set of PLATFORMS: platforms;

%Indices of feature of every platform
set of int: FEATURES = 1..9;
int: name = 1;                                                              
int: force_sensor = 2;int: tactile_sensor = 3;int: memory_availability = 4; 
int: simple_pressure_sensor = 5; int: capacitive_and_resistive_flexible_force_sensor = 6; int: piezoelectric = 7; int: strain_gauge_based = 8; int:speed = 9; 
%Number of platforms
int: n_platforms;
set of int:PLATFORMS = 1..n_platforms;

%Array of platforms and properties
array[PLATFORMS] of string: n;       
array[PLATFORMS,FEATURES] of int: dd;

%Name of the platforms
n = ["nvidia_force","amd_tactile","intel_fused","nxp_force"];

%Platform properties
dd =  [| 1,   1,   50, 400, 1, 1, 0, 0, 10,   % PF1
       | 2,   0,  100, 100, 2, 2, 2, 2, 100,  % PF2
       | 3,   0,   10, 400, 2, 2, 2, 2, 1000,  % PF3
       | 4,   1,    0,  50, 0, 0, 1, 1, 10,|];  % PF4

array[FEATURES] of var int: force_platform; 
array[FEATURES] of var int: tactile_platform;
array[FEATURES] of var int: fused_platform;  


%Constraint of platform names to be in the provided table
constraint force_platform[name] in platforms;  
constraint tactile_platform[name] in platforms;
constraint fused_platform[name] in platforms;  


%Constraint that the values to be assigned to platform names are available in the table
constraint table(force_platform, dd);  
constraint table(tactile_platform, dd);
constraint table(fused_platform, dd);  

%Technical constraints
constraint ((force_platform[force_sensor] >= min_force_sensor_count) /\ (force_platform[simple_pressure_sensor] != 2) /\ (force_platform[capacitive_and_resistive_flexible_force_sensor] != 2) /\ (force_platform[piezoelectric] != 2) /\ (force_platform[strain_gauge_based] != 2)/\(force_platform[speed] >5)/\(force_platform[speed] <2000));
% constraint ((stationary == 1) /\ (gripper_value == 0));
% constraint force_platform[force_sensor] >= min_force_sensor_count;
constraint (tactile_platform[tactile_sensor] >= min_tactile_sensor_count /\ tactile_platform[speed] >5 /\ tactile_platform[speed] <2000);
constraint (fused_platform[memory_availability]>=min_memory_fused /\ fused_platform[speed] >5 /\ fused_platform[speed] <2000);
 

solve satisfy;

%Prints platform names
output["force_platform =",n[fix(force_platform[name])],"\n",
       "tactile_platform =",n[fix(tactile_platform[name])],"\n",
       "fused_platform = ",n[fix(fused_platform[name])],"\n"];

%Prints platform indices
output["force_platform_index =",show(force_platform[name]),"\n",
       "tactile_platform_index =",show(tactile_platform[name]),"\n",
       "fused_platform_index = ",show(fused_platform[name]),"\n"];
