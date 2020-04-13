# Lazor_project
Description:
This project finds the solution for different levels of the game "Lazor" in which square blocks are used to reflect and refract a lazor to hit specific targets.  The board configuration and laser information of a specific level is read from a .bff file.       

Modules needed: PIL, itertools, copy, termcolor, unittest, time

Installation: Download code from Github.

Executing the program:
- download bff files
- replace 'filename' with desired Lazor board bff file
- png file of solution is saved automatically

Optional challenge:
In the first version of this project, we use random sampling method to find a potential game board. If one arrangement doesn't work, it will be appended to history list and next arrangement will be re-sampled. This method works but sometimes it's pretty slow: when the game board is big and the history list becomes very long, it will be slower and slower to find a random sample not in history list. Considering the amount of usable blocks are usually not too big, method of exhaustion could be more efficient: all permutations of available slots are calculated and stored in a list. When a new arrangement is needed, one slot permutation will be poped out from the list and blocks will be filled accordingly. This method is faster but still improvable: usable blocks usually contain duplicate categories, like in mad_7.bff, all blocks are reflective. Within all slot permutations, a large portion could be considered
identical.In this final release, we use an improved method of exhaustion for potential game board generation. All combinations of available slots and all permuatations of usable blocks are calculated first. Then every block permuatation is added into a set to combine repeated items. Finnaly every slot combination is paired with each block permutation to form a dictionary and being added to the  arrangement list. By using this method, all .bff files can be solved with 1 minute. Once a potential game board is generated, the playthrough of laser path could be very intuitive: when a laser passes through a new point, its exit angle and next point could be calculated given the entry angle and category of surrounding blocks. The laser will continue to genrate its path until it reaches the boarder of the map. It's worth mentioning that in some rare cases a laser may form a loop and will never end inside the map. Since we use the method of exhaustion to generate the potential board, when the map is big enough, there's a good chance that this happens before a solution is found.  Fortunately this is not the case in all maps of this project, but we still add a funtion to check if a loop has formed at the end of each path generating cycle.


Authors:
Zhezhi Chen
Imaan Amlani
