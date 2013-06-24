rer
===

# Abstract
Ultra-light display for rer (Paris urban transportation) live schedule.

# Description
This script get the live schedule data from the ratp or sncf website in order to provide light information about :
- schedule ;
- delay ;
- number of train in front of your train ;
- ...

At this time it works only for the north part of the RER B.

# Usage
To use this script you need an internet connection and python 3.3.2. Then you use the script with the command : 
$ python rerWaitingRoom.py
The script must then display a graphic scheme of the RER B line with the current train and their priority order in Gare du Nord. 
The script update this display by doing request station after station (the last station updated is shown by a star.

# Next step
The next step is to : 
- improve the position of the train using the time to destination ;
- complete the B-line and add other line ;
- provide a more complete (but still light) webpage ; 
- put the script on a server (in order to use it from my smartphone) ;
- add the train position in a map with live update (wahoo if i do that i will be very happy) ;
- ... 
