
###   Requiements ###

Python 2.7

###  How to Run ###

$ python Runner.py

###  Assumptions ###
1. considered that it is a sand alone engine to process signal wrote it as a plain python project. Otherwise would have used flask or django to receive signals and process.
2. Each signal can have multiple rules and even if one fails print signal name on output.
3. considered only the given three value types.
4. Assuming the input as a file in json format, otherwise would design the Runner.py in a different way.


###  Approach ###
1. Should be more dynamic to add more rules and data type.
2. keept rules as a separate file with comma separated values and '#' as comment line.
3. it help to add new rules and data types easily.
4. using dictionary mapping so that new rules can be added easily.


###  Trade off ###
1. loading whole file in memory takes a lot of memory should follow another approach to pass signal.


###  Time Complexity ###

Complexity of this approach in O(n) as it only goes through each signal once with 'n' rules.


###  Run time performance ###

For the given sample input it takes 0.001545 seconds on mac book pro(2013)

###  Bottlenecks ###

With increase in signal file size memory usage increases but only at runner end, can be easily solved by streaming signals via socket.


###  Improvements to be done in order of priority ###

1. convert to django or flask project and stream the signals through sockets.
2. Would write Py units to tests the whole project(took 3hours for this thing)
3. A nice dashborad to see the signals that got failed in real time using html and jquery.


