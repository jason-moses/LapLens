print("Select Mode:")
mode = input("Race Report or Race Replay:")

if mode == "Race Replay":
    from PlottingMachine import PlottingMachine
    plotting_machine = PlottingMachine()

if mode == "Race Report":
    from RaceReport import Report
    report = Report()
