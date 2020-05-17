% Planning a balanced meal
%Inbuilt header file
include "table.mzn";

%Thresholds of properties
int: min_force_sensor_count;  
int: min_tactile_sensor_count; 
int: min_memory_fused;               


set of PLATFORMS: platforms;

%Indices of feature of every platform
set of int: FEATURES = 1..4;
int: name = 1;                                                              
int: force_sensor = 2;int: tactile_sensor = 3;int: memory_availability = 4; 

%Number of platforms
int: np; % number of platforms
set of int:PLATFORMS = 1..np;

%array of platforms and properties
array[PLATFORMS] of string: n;       
array[PLATFORMS,FEATURES] of int: dd;

%Platforms to be assigned for every sensor
array[FEATURES] of var int: force_platform; 
array[FEATURES] of var int: tactile_platform;
array[FEATURES] of var int: fused_platform;  


%constraint of platform names to be in the provided table
constraint force_platform[name] in platforms;  
constraint tactile_platform[name] in platforms;
constraint fused_platform[name] in platforms;  


%constraint that the values to be assigned to platform names are available in the table
constraint table(force_platform, dd);  
constraint table(tactile_platform, dd);
constraint table(fused_platform, dd);  

%Technical constraints
constraint force_platform[force_sensor] >= min_force_sensor_count;
constraint tactile_platform[tactile_sensor] >= min_tactile_sensor_count;
constraint fused_platform[memory_availability]>=min_memory_fused;

solve satisfy;

output["force_platform =",n[fix(force_platform[name])],"\n",
       "tactile_platform =",n[fix(tactile_platform[name])],"\n",
       "fused_platform = ",n[fix(fused_platform[name])],"\n"];

%platform index required
%dealing with unavailable platforms
%ranking platforms and get the best platform

