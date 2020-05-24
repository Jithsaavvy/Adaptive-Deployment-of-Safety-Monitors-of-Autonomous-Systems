from minizinc import Instance, Model, Solver

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
instance["min_memory_fused"] = 1000
instance["np"] = 4
instance["x"] = 1
instance["platforms"] = set([1,2,3,4])
# solve to get the general solution
result_general = instance.solve()
# solve to find the intermediate solution
result_intermediate = instance.solve(intermediate_solutions=True)
# solve to find all the solutions
result_all = instance.solve(all_solutions=True)

print(result_general)
print(type(result_general))
if result_general == None:
    print("hello")
print("----------------")
print("Intermediate solutions are listed below:\n")
u = []
for i in result_intermediate:
    print(i)
    print(i.force_platform)
    u.append(i.force_platform)
    print(i.tactile_platform)
    u.append(i.tactile_platform)
    print(i.fused_platform)
    u.append(i.fused_platform)

print("----------------")
print("All solutions are listed below:\n")

for i in result_all:
    print(i)
    print(i.force_platform)
    print(i.tactile_platform)
    print(i.fused_platform)

print("----------------")

if len(u) == 0:
    platforms = Model("./None_case_handler.mzn")

    # # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # # Create an Instance of the platforms model for Gecode
    instance = Instance(gecode, platforms)
    # Assign 4 to n
    instance["name"] = 1
    instance["min_force_sensor_count"] = 1
    instance["min_tactile_sensor_count"] = 100
    instance["min_memory_fused"] = 1000
    instance["np"] = 4
    instance["x"] = 1
    instance["platforms"] = set([1,2,3,4])
    # solve to get the general solution
    result_general = instance.solve()
    print("No_case_handling_solution:\n")
    print(result_general)