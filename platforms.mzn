% Planning a balanced meal
%Inbuilt header file
include "table.mzn";

%Thresholds of properties
int: min_force_sensor_count;  
int: min_tactile_sensor_count; 
int: min_memory_fused;     
int: x;          

% min_force_sensor_count  = 1;
% min_tactile_sensor_count= 100;
% min_memory_fused= 400;
% np = 4; 

% platforms = {1,2,3,4};
n = ["nvidia_force","amd_tactile","intel_fused","nxp_force"];
dd =             [| 1,   1,   50, 400,    % PF1
                  | 2,   0,  100, 100,    % PF2
                  | 3,   0,   10, 400,    % PF3
                  | 4,   1,    0,  50|];  % PF4

set of PLATFORMS: platforms;

%Indices of feature of every platform
set of int: FEATURES = 1..4;
int: name;                                                              
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

%Inbuilt header file
% include "table.mzn";

% platforms = {1,2,3,4};
% %Thresholds of properties
% int: min_force_sensor_count;  
% int: min_tactile_sensor_count; 
% int: min_memory_fused;               

% set of PLATFORMS: platforms;

% %Indices of feature of every platform
% set of int: FEATURES = 1..4;
% int: name = 1;                                                              
% int: force_sensor = 2;int: tactile_sensor = 3;int: memory_availability = 4; 

% %Number of platforms
% int: np;
% set of int:PLATFORMS = 1..np;

% %Array of platforms and properties
% array[PLATFORMS] of string: n;       
% array[PLATFORMS,FEATURES] of int: dd;

% %Platforms to be assigned for every sensor
% array[FEATURES] of var int: force_platform; 
% array[FEATURES] of var int: tactile_platform;
% array[FEATURES] of var int: fused_platform;  


% %Constraint of platform names to be in the provided table
% constraint force_platform[name] in platforms;  
% constraint tactile_platform[name] in platforms;
% constraint fused_platform[name] in platforms;  


% %Constraint that the values to be assigned to platform names are available in the table
% constraint table(force_platform, dd);  
% constraint table(tactile_platform, dd);
% constraint table(fused_platform, dd);  

% %Technical constraints
% constraint force_platform[force_sensor] >= min_force_sensor_count;
% constraint tactile_platform[tactile_sensor] >= min_tactile_sensor_count;
% constraint fused_platform[memory_availability]>=min_memory_fused;

% solve satisfy;

% %Prints platform names
% output["force_platform =",n[fix(force_platform[name])],"\n",
%        "tactile_platform =",n[fix(tactile_platform[name])],"\n",
%        "fused_platform = ",n[fix(fused_platform[name])],"\n"];

% %Prints platform indices
% output["force_platform_index =",show(force_platform[name]),"\n",
%        "tactile_platform_index =",show(tactile_platform[name]),"\n",
%        "fused_platform_index = ",show(fused_platform[name]),"\n"];