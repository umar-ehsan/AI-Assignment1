'''
python module to take openstreetmap data as well as the usgs explorer
data as input. It will parse the xml file (saved as 'map.osm') and 
extract the ways and nodes from the map data into a tree structure.
In additon, it will read the '.bil' digital elevation SRTM void-filled
data to build a corresponding elevation data. The entire data is used to
build a node and resulting graph

'''

import xml.etree.ElementTree as ET
import struct
import data as DT
import random

# data from bounds in osm file
minimumLat = 43.9153
maximumLat = 43.9428
minimumLon = -78.8207
maxumumLon = -78.8672

# data from the ".hdr" file accompanied by the .bil elevation file
numberofRows = 1200
numberofColumns = 1200

'''
heuristic function is using euclidian distance since it is permissible
'''
def heuristicFunction(startNode, endNode):
    latDist = (endNode.lat - startNode.lat)*MPERLON
    lonDist = (endNode.lon - startNode.lat)*MPERLAT
    return math.sqrt(latDist*latDist+lonDist*lonDist)

'''
calculate the cost of path from start to end depending on
the distance and elevation
'''
def calculateCost(startNode, endNode):
    distance = heuristicFunction(startNode, endNode)
    elevationDifference = endNode.elev - startNode.elev
    slope = elevationDifference / distance
    cost = slope * 2.5 + distance
    return cost      

''' 
finds the best path using the cost function and A* algorithm
'''
def findPath(starterNode, endNode):
    cost = 100000000
    newCost = 0
    nextNode = starterNode
    currentNode = starterNode
    junctionNode = starterNode
    while (nextNode != endNode):
        for path in currentNode.paths:
            forwardCost = 0
            backwardCost = 0
            currIndex = path.index(currentNode)
            while (currIndex < len(path.nodes)):
                if (currIndex + 1) < len(path.nodes):
                    forwardCost += calculateCost(currentNode, path.nodes[currIndex + 1])
                    currentNode = path.nodes[currenIndex + 1]
                    currIndex += 1
            currentNode = starterNode
            currIndex = path.index(currentNode)
            while (currIndex > 0):
                if currIndex > 0:
                    backwardCost += calculateCost(currentNode, path.nodes[currIndex + 1])
                    currIndex -= 1
            if forwardCost > backwardCost and len(path.nodes[len(path.nodes)-1].paths) > 1:
                nextNode = path.nodes[len(path.nodes)-1]
                newCost += forwardCost
            elif forwardCost < backwardCost and len(path.nodes[0].paths) > 1:
                nextNode = path.nodes[0]
                newCost += backwardCost
        if newCost < cost:
            cost = newCost
            junctionNode = nextNode
        nextNode = junctionNode
        currentNode = nextNode
    return cost
        
'''
reads the elevation data file in .bil format obtained from USGS Earth Explorer
and unpacks the 2-byte integers into elevation values in a 1D array
'''

def extractElevations(filename):   
    elevationFile = open(filename, "rb")
    elevStr = elevationFile.read()
    elevations = []
    for point in range(0,len(elevStr),2):
        # this magic builds a list of values (1-d, not 2-d!) and deals with the
        # fact that the data file is given in big-endian format which is unusual these days...
        # you may of course load this into some other data structure as you see best
        elevations.append(struct.unpack('<h',elevStr[point:point+2])[0])
    return elevations

'''
map the 1-D elevation array back to a 2D elevation data
'''
def elevationArray(elevationList):
    elevations = []
    for i in range(0,1200):
        elevations.append([])
        for j in range(0,1200):
            elevations[i].append(elevationList[i * numberofRows + j])
    return elevations
    

'''
parse_osm() prompts the user to input the openstreetmap osm filename for the file to be
parsed and stored. It uses the xml.etree library to parse the file.
'''

def parseOsm(osmFilename, bilFilename):  
    osmfile = ET.parse(osmFilename)   
    rootofTree = osmfile.getroot()
    elevations = extractElevations(bilFilename)
    elevation2D = elevationArray(elevations)
    # start extracting 'ways' and 'nodes'
    mapNodes = []
    paths = []
    pathname = ""
    for eachItem in rootofTree:
        isAPath = False
        if eachItem.tag == 'node':
            latitude = (float)(eachItem.get('lat'))
            longitude = (float)(eachItem.get('lon'))
            nodeId = (int)(eachItem.get('id'))
            # map the elevation data to the node in osm file
            elevation = elevation2D[(int)(44 - latitude) * (numberofRows)][(int)(longitude + 79) * (numberofColumns)]
            mapNodes.append(DT.Node(latitude, longitude, elevation, nodeId))

        elif eachItem.tag == 'way':
            pathList = []
            pathNodes = []
            pathName = "No Name"
            alreadyExists = False
            for subItem in eachItem:
               if subItem.tag == 'tag' and subItem.get('k') == 'highway':
                   isAPath = True 
               if subItem.tag == 'tag' and subItem.get('k') == 'access':
                   isAPath = False
            if isAPath == True:
               for subItem in eachItem:
                   if subItem.tag == 'tag' and subItem.get('k') == 'name':
                       pathName = subItem.get('v')
                   if subItem.tag == 'nd':
                       for point in mapNodes:
                          if point.id == (int)(subItem.get('ref')):
                              pathNodes.append(point)
                       pathList.append((int)(subItem.get('ref')))
               for walkPath in pathList:
                   for aNode in mapNodes:
                       if aNode.id == walkPath:
                           aNode.paths.append(DT.Path((int)(eachItem.get('id')), pathName, pathNodes))

               paths.append(DT.Path((int)(eachItem.get('id')), pathName, pathNodes))
    return mapNodes, paths
            



def main():
    nodes, paths = parseOsm('map.osm', 'elevation.bil')
    randomStarter = random.randint(0, len(nodes))
    randomEnd = random.randint(0, len(nodes))
    print("Starting from (" + (str)(nodes[randomStarter].lat) + ", " + (str)(nodes[randomStarter].lon) + ") to")
    print("(" + (str)(nodes[randomEnd].lat) + ", " + (str)(nodes[randomEnd].lon) + ")")
    cost = findPath(nodes[randomStarter], nodes[randomEnd])
    print("Lowest cost distance: " + (int)(cost))

    

main()
