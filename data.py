'''
Here we define the basic data structure which is nodes of a mapping
graph. The nodes contain latitude, longitude, elevation, and node id. 
The ways contain node ids of the nodes in a way, and the way name.
In addition, each way contains a cost value function associated with an edge between
two adjacent nodes in the way. The cost value is calculated through the 
cost function and the heuristic distance function

'''

import math

# some constants about the earth
MPERLAT = 111000 # meters per degree of latitude, approximately
MPERLON = MPERLAT * math.cos(44*math.pi/180) # meters per degree longitude at 44N

'''
Node class
'''
class Node():
    def __init__(self, lat, lon, elev, nodeId):
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.id = nodeId
        self.paths = []

'''
Way class
'''
class Path():
    def __init__(self, pathId, name, listofNodes):
        self.name = name
        self.id = pathId
        self.nodes = []
        for node in listofNodes:
            self.nodes.append(node)

        
   


