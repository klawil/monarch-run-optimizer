from ortools.sat.python import cp_model

possible_runs = {
  'Pioneer': [
    'KC Cutoff',
    'Sleepy Hollow',
    'Roundabout',
    'Tango',
    'Romp',
    'Short Circuit',
    'Powderline',
  ],
  'Garfield': [
    'Sleepy Hollow',
    'Roundabout',
    'Tango',
    'Romp',
    'Short Circuit',
    'Powderline',
    'Kanonen',
    'Cleanzer',
    'Ajax',
    'Examiner',
    'Lobo',
    'No Name',
    'Christmas Tree',
  ],
  'Panorama': [
    'Skywalker',
    'Curecanti',
    'Quickdraw',
    'Short N Sweet',
    'Turbo',
    'Mirage',
    'Sheer Rocko',
    'High Anxiety',
    'Great Divide',
    'JRs',
    'Zipper',
    'Dire Straits',
    'Ticaboo',
    'Picante',
  ],
  'Breezeway': [
    'Outback',
    'Shagnasty',
    'Bs Bash',
    'Upper Halls Alley',
    'Docs Run',
    'Little Mo',
    'Ramble On',
    'Genos Meadow',
    # 'Southbound',
    # 'Mirkwood Bowl',
    # 'Orcs',
    # 'Elation Ridge',
    # 'Mirkwood Trees',
    # 'Staircase',
    # 'East Trees',
    # 'Lodgeview',
  ],
  'Caterpillar': [
    'Snowflake',
    'Butterfly',
  ],
  'Tumbelina': [
    'Little Joe',
    'Beeline',
    'Rookie',
  ],
  'Roundabout': [
    'Sidewinder',
    'Drifter',
    'Liberty',
    # 'North Forty',
    # 'Tele Alley',
    # 'Gunbarrel',
  ],
  'Powderline': [
    'Drifter',
    'Liberty',
    # 'North Forty',
    # 'Tele Alley',
    # 'Gunbarrel',
  ],
  'Short Circuit': [
    'Drifter',
    'Liberty',
    # 'North Forty',
    # 'Tele Alley',
    # 'Gunbarrel',
  ],
  'Romp': [
    'Sidewinder',
    'Toddler',
    'Drifter',
    'Liberty',
    'North Forty',
    'Tele Alley',
    'Gunbarrel',
  ],
  'Toddler': [
    'Lower Tango',
  ],
  'Tango': [
    'Lower Tango',
  ],
  'Kanonen': [
    'Lower Tango',
  ],
  'Sidewinder': [
    'Lower Tango',
  ],
  'Curecanti': [
    'Powderline',
  ],
  'Lobo': [
    'Lower No Name',
  ],
  'No Name': [
    'Lower No Name',
  ],
  'Christmas Tree': [
    'Freeway',
  ],
  'KC Cutoff': [
    'Pinball',
    'Serendipity',
    'Tenderfoot',
    'Glade',
    'Rookie',
    'Beeline',
    'Little Joe',
    'Freeway',
  ],
  'Sleepy Hollow': [
    'Rookie',
    'Beeline',
    'Little Joe',
    'Freeway',
  ],
  'Skywalker': [
    'KC Cutoff',
    'Sleepy Hollow',
  ],
  'Quickdraw': [
    'Pinball',
    'Serendipity',
    'Tenderfoot',
    'Glade',
    'Rookie',
    'Beeline',
    'Little Joe',
    'Freeway',
  ],
  'Short N Sweet': [
    'Pinball',
    'Serendipity',
    'Tenderfoot',
    'Glade',
    'Rookie',
    'Beeline',
    'Little Joe',
    'Freeway',
  ],
  'Turbo': [
    'Pinball',
    'Serendipity',
    'Tenderfoot',
    'Glade',
    'Rookie',
    'Beeline',
    'Little Joe',
    'Freeway',
  ],
  'Great Divide': [
    'Snowburn',
  ],
  'Upper Halls Alley': [
    'Lower Halls Alley',
  ],
  # 'Southbound': [
  #   'Genos Meadow',
  # ],
}

lifts = [
  'Pioneer',
  'Garfield',
  'Caterpillar',
  'Tumbelina',
  'Breezeway',
  'Panorama',
]
all_runs = []

for start_run in possible_runs:
  if start_run not in all_runs and start_run not in lifts:
    all_runs.append(start_run)

  for next_run in possible_runs[start_run]:
    if next_run not in all_runs:
      all_runs.append(next_run)

all_runs.sort()
# for run in all_runs:
#   print(run)
# print(all_runs)

# A class for printing the variables while searching for an optimal solution
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__solution_count = 0

  def on_solution_callback(self):
    self.__solution_count += 1

  def solution_count(self):
    return self.__solution_count

# Create all the possible runs
lift_runs = []
def getNextRuns(base, last):
  global lift_runs
  if not last in possible_runs:
    lift_runs.append(base)
    return
  
  for next_run in possible_runs[last]:
    new_base = base.copy()
    new_base.append(next_run)
    getNextRuns(new_base, next_run)

for lift in lifts:
  for start in possible_runs[lift]:
    base = [
      # lift,
      start,
    ]
    getNextRuns(base, start)

# Create the modal
model = cp_model.CpModel()

# Create variables for each lift ride
run_implications = {}
lift_run_bools = []
used_lift_runs = []
for lr in lift_runs:
  lift_run_name = "_".join(lr)
  if lift_run_name in used_lift_runs:
    continue
  used_lift_runs.append(lift_run_name)
  local_lift_run = model.NewBoolVar(lift_run_name)
  lift_run_bools.append(local_lift_run)
  for run in lr:
    if run not in run_implications:
      run_implications[run] = []
    run_implications[run].append(local_lift_run)

# Create a variable for each run
run_bools = {}
run_ints = {}
run_counts = {}
# num_runs_done = model.NewIntVar(0, len(all_runs), "num_runs_done")
for r in all_runs:
  run_bools[r] = model.NewBoolVar(f"run_{r}")
  model.AddBoolOr(run_implications[r])
  run_counts[r] = model.NewIntVar(0, 5, f"run_{r}")
  model.Add(run_counts[r] == sum(run_implications[r]))
excess_runs = model.NewIntVar(0, len(all_runs * 10), "excess_runs")
model.Add(excess_runs == sum([(run_counts[rc] - 1) * 2 for rc in run_counts]))
# model.Add(num_runs_done == sum(run_bools[rb] for rb in run_bools))
# model.Add(num_runs_done == len(all_runs))

# Set the optimization to reduce the number of runs
num_lift_rides = model.NewIntVar(0, len(lift_runs), "num_lift_runs")
model.Add(num_lift_rides == sum(lift_run_bools))

optimize = model.NewIntVar(0, len(lift_runs) * 50, "optimized")
model.Add(optimize == num_lift_rides + excess_runs)

model.Minimize(optimize)
# model.Minimize(num_lift_rides)

# Create the solution progress output class showing all the ratios
solution_printer = VarArraySolutionPrinter()

# Solve the problem
solver = cp_model.CpSolver()
status = solver.Solve(model, solution_printer)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
  print(f"Num lift rides: {solver.Value(num_lift_rides)}")
  # print(f"Num runs: {solver.Value(num_runs_done)}")
  print("")
  print("Lift Rides:")
  for lrb in lift_run_bools:
    if solver.Value(lrb):
      print(lrb)

  print("")
  print("Repeated Runs:")
  for run in run_counts:
    if solver.Value(run_counts[run]) > 1:
      print(run_counts[run], solver.Value(run_counts[run]))
else:
  print("No optimal solution found")
# print(len(all_runs))
