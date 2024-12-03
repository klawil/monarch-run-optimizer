# Import the optimizations library from Google
from ortools.sat.python import cp_model

# For each run, which runs are you able to get to from the bottom of it?
# For each lift, which runs can you get to the top of from it
# e.g. from the Catepillar lift you can get to Snowflake and Butterfly
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

# Create all the possible runs
# Passes in a run or lift, retrieves all the runs that that run can
# lead to and adds it to the end of an array
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

# Starting with the lifts, build out the possible runs to get down
# the mountain
for lift in lifts:
  for start in possible_runs[lift]:
    # start is the a run you can get to from the top of the lift
    base = [
      # lift,
      start,
    ]
    getNextRuns(base, start)

# Initialize the modal
model = cp_model.CpModel()

# This holds an array of run names to the lift rides it's a part of
# boolean variables. i.e. if any of the lift rides in the array is used,
# that run will be completed
run_implications = {}

# This list holds all of the possible list run boolean variables. It is
# used to determine how many lift rides are needed to hit every ski run
lift_run_bools = []

# This holds the list of runs that have already been used so we don't get
# duplicate ways down the mountain
used_lift_runs = []

# Create variables for each potential lift ride
for lr in lift_runs:
  # Some runs you can get to from multiple lifts, so make sure
  # that we aren't re-using a potential way down
  lift_run_name = "_".join(lr)
  if lift_run_name in used_lift_runs:
    continue
  used_lift_runs.append(lift_run_name)

  # Make a boolean variable. If true, this way down off the lift is used
  local_lift_run = model.NewBoolVar(lift_run_name)

  # Save the boolean variable into a list that will be used to determine the
  # number of times you need to ride the lift
  lift_run_bools.append(local_lift_run)

  # Loop over each run in this way down the mountain
  for run in lr:
    # If this run doesn't already have an entry in the run_implications object,
    # create one as an empty list
    if run not in run_implications:
      run_implications[run] = []

    # Add the current lift ride to the array
    run_implications[run].append(local_lift_run)

# This object has a key of a run name and then an integer containing how many
# times the run will have been skied
run_counts = {}
# Loop over all of the run names
for r in all_runs:
  # This says that at least one of the ways down the mountain associated with
  # each run must be True. This will make sure that each run is skied at least
  # once
  model.AddBoolOr(run_implications[r])
  
  # Create an integer variable that is the number of ways down the mountain that
  # include this run are being used
  run_counts[r] = model.NewIntVar(0, 5, f"run_{r}")
  model.Add(run_counts[r] == sum(run_implications[r]))

# Create a variable that counts how many repeated runs there are
excess_runs = model.NewIntVar(0, len(all_runs * 10), "excess_runs")
model.Add(excess_runs == sum([(run_counts[rc] - 1) * 2 for rc in run_counts]))

# Create a variable that counts the number of times that the lift will need to be ridden
num_lift_rides = model.NewIntVar(0, len(lift_runs), "num_lift_runs")
model.Add(num_lift_rides == sum(lift_run_bools))

# Create an optimization variable (since we can only optimize to one) that is a sum
# of the number of lift rides AND the number of extra runs
optimize = model.NewIntVar(0, len(lift_runs) * 50, "optimized")
model.Add(optimize == num_lift_rides + excess_runs)

# Set the model to try to get the smallest number of the optimized variable
# so the model will prefer solutions that have the lowest number of lift rides
# plus the number of repeated runs
model.Minimize(optimize)

# Solve the problem
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Make sure we have an optimal (or at least feasible) solution
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
  # Number of times we need to ride the lifts
  print(f"Num lift rides: {solver.Value(num_lift_rides)}")
  print("")
  
  # The different paths we need to take to get down the mountain in this solution
  print("Lift Rides:")
  for lrb in lift_run_bools:
    if solver.Value(lrb):
      print(lrb)
  print("")
  
  # Which runs will be repeated and how many times?
  print("Repeated Runs:")
  for run in run_counts:
    if solver.Value(run_counts[run]) > 1:
      print(run_counts[run], solver.Value(run_counts[run]))
else:
  print("No optimal solution found")
