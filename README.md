# VOCOWA


This is basic static trial using LIDAR
The program was compiled on python 2.7.13
Make sure u have following python modules installed : pygame, numpy, PIL

## Procedure
1. Clone 'pygame_arena.py' and 'VirtualBot.py' in a common folder
2. Execute former file - make a map by dragging mouse on the screen. The blue box is the bot. Close pygame screen to finish
3. This wil result in 'image.jpg' and 'map.jpg' files in same folder
4. Now execute latter file. When it prompts for continue, enter 'n'
5. This will result in 'result.jpg' file

Sample files are being provided for refernce
## Limitations
1. Static environment
2. Bot's currently not moving
3. I'm assuming small spaces to be empty - in order to create a polygon out of many coordinates
4. Bots dimensions ignored
5. Computation order is O(n^2). So large maps will be inefficient.
