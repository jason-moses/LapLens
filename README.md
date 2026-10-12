🏎️ **LapLens — Formula 1 Race Replay & Analysis**

Relive the race. Analyse the data. Understand the result.

LapLens is a Python-based Formula 1 analysis project built around the 2021 São Paulo Grand Prix, featuring an interactive-style race replay with a live telemetry HUD and a detailed analytical race report.

Built using Python, FastF1, Matplotlib, NumPy, SciPy, and object-oriented programming, LapLens transforms raw race telemetry into visualisations that help explain not just what happened during a race, but why it happened.


✨ **Features**

LapLens has two main modes:

1. 🎬 **Race Replay**

Relive the battle between Lewis Hamilton and Max Verstappen throughout the race.

The replay tracks both drivers and displays a telemetry HUD containing:

Speed — Monitor the car's speed throughout the lap.

Gear — Track gear changes as the driver navigates the circuit.

Brake Indicator — Observe braking activity.

DRS — Track the DRS state.

Lap Number — Follow the race lap by lap.

Position — Monitor each driver's race position, such as P1 and P2.

The telemetry overlay brings together multiple data channels to recreate the feel of an F1 broadcast while allowing a closer look at the data behind the action.

2. 📊 **Race Report**

A detailed, graph-driven investigation of the 2021 São Paulo Grand Prix, exploring the race's key events, strategies, and decisive moments.

The report covers:

Race Overview — The background and context behind the Hamilton–Verstappen battle.

Sequence of Events — The key incidents and developments that shaped the race.

Tyre Strategy — Pit-stop timing, tyre compounds, and strategic decisions.

Tyre Degradation — Compare degradation trends and investigate unusual changes in lap times.

Telemetry Analysis — Use speed and engine RPM data to investigate differences in driving performance.

Track Map Comparisons — Identify circuit sections where one driver was faster than the other.

The Decisive Factor — Investigate why Verstappen lost to Hamilton, including the relationship between driving patterns, tyre degradation, and straight-line performance.

Rather than simply presenting race statistics, the report uses data visualisation to build an evidence-based narrative of the race.

🛠️ **Tech Stack & Concepts**

**Languages**

Python — Core programming language

**Libraries**

FastF1 — Retrieving Formula 1 timing and telemetry data

Matplotlib — Creating graphs, charts, and telemetry visualisations

NumPy — Numerical operations and data processing

SciPy — Supporting numerical analysis

**Techniques & Concepts**

Object-Oriented Programming (OOP) — Structuring code into reusable components

Interpolation — Aligning telemetry samples for driver comparisons and race replay

Linear Regression — Analysing trends in lap times and tyre degradation


🧠 **What I Learned**

Building LapLens brought together several areas of programming and data analysis:

Working with real-world telemetry: Processing time-series data from multiple cars and handling different telemetry channels.

Data interpolation: Aligning telemetry samples and handling continuous and discrete signals appropriately.

Data visualisation: Designing graphs and a custom telemetry HUD to make complex data easier to interpret.

Object-Oriented Programming: Organising a large project into maintainable components.

Scientific computing: Applying numerical and analytical techniques to investigate race performance.

Data-driven storytelling: Turning raw data into an explanation of the events and decisions that shaped a race.

With nearly 1,000 lines of code, LapLens was an opportunity to combine programming, engineering-style analysis, and my interest in Formula 1 into one complete project.


🏁 **The Race Behind the Project**

The 2021 São Paulo Grand Prix provided the perfect case study: Hamilton started tenth, Verstappen started first, and Hamilton ultimately won after a compelling battle between the two title contenders.

LapLens uses this race to explore how telemetry, tyre behaviour, strategy, and on-track performance can be combined to investigate the factors behind a result.


🔮 **Future Possibilities**

Web-Based Application — Extend LapLens into a web application, making its race replay and analytical reports more accessible to other F1 enthusiasts.

Machine Learning–Driven Lap Analysis — Develop a model to analyse the perfect lap and compare it against actual driver telemetry. Use the differences to generate additional graphs, performance metrics, 
and data-driven insights that can be compiled into an automated race analysis report.


👨‍💻 **Author**

Built as a personal Formula 1 data analysis capstone project using Python and scientific computing libraries.




https://github.com/user-attachments/assets/277d1353-ab6a-4cf4-82bb-cef6155f2dd7


<img width="1600" height="899" alt="Race Overview Slide" src="https://github.com/user-attachments/assets/11c7483c-96e8-4a95-9f62-a19569b2100a" />




LapLens — because every lap tells a story.
