from math import radians, cos, sin, asin, sqrt
class ANode:
    
    def __init__(self, line_id, to_node_id, parentNode, gCost=0, hCost=0):
        self.to_node_id = to_node_id
        self.line_id = line_id
        self.parentNode = parentNode
        self.gCost = gCost
        self.hCost = hCost
    #@end method Constructor
    
    def getLine_id(self):
        return self.line_id
    #@end method getLine_id
    
    def getTo_node_id(self):
        return self.to_node_id
    #@end method getTo_node_id
    
    def getArcId(self):
        return self.arcId
    #@ ebd method getArcId
    
    def getParentNode(self):
        return self.parentNode
    #@end method getParentNode
    
    def getGCost(self):
        return self.gCost
    #@end method getGCost
    
    def getHCost(self):
        return self.hCost
    #@end method getHCost
    
    def getEvalCost(self):
        return self.gCost + self.hCost
        
    def hasParentNode(self):
        return self.parentNode != None
    #@end method hasParentNode
    
    def __str__(self):
        return "Node(g=%f, h=%f)" % (self.gCost, self.hCost)

class minDistanceSearch:
    def __init__(self,node_table,line_table):
        self.node_table=node_table
        self.line_table=line_table

    def findNodeWithMinCost(self, nodeList):
        nodeWithMinCost = nodeList[0]
        minIndex = 0
        for i in range(1,len(nodeList)):
            if nodeWithMinCost.getEvalCost() > nodeList[i].getEvalCost():
                nodeWithMinCost = nodeList[i]
                minIndex = i
        return (nodeWithMinCost, minIndex)
        
    def findPath(self, node):   #return path from start to goal #node:Node()
        path = []
        path.insert(0, (node.getLine_id(), node.getTo_node_id()))
        while node.hasParentNode():
            path.insert(0, (node.getParentNode().getLine_id(), node.getParentNode().getTo_node_id()))
            node = node.getParentNode()
        return path     #[(line_id, to_node_id), ...]
    #@end method findPath
    
    def calShortestPathHCost(self,startId,goalId):
        lat1=self.node_table[startId][1]
        lon1=self.node_table[startId][2]
        lat2=self.node_table[goalId][2]
        lon2=self.node_table[goalId][2]
        
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r


    def calShortestPathGCost(self,currentPath):
        distance = 0
        for i in range(2, len(currentPath)):
            #line = self.line_table[ currentPath[i][0] ]
            #length = line[1]
            #length = self.calShortestPathHCost(currentPath[i-1][1],currentPath[i][1])
            #distance += length
            if currentPath[i][0] != currentPath[i-1][0]:
                distance+=1
        return distance
        
        
    def shortestPathSearch(self, startId, goalId):
            queue = []
            gCost = 0
            hCost = self.calShortestPathHCost(startId, goalId)
            queue.append(ANode(None, startId, None, gCost, hCost))
            closedList = []
            found = False
            currentPath=[]
            while len(queue) > 0:
                
                (currentNode, minIndex) = self.findNodeWithMinCost(queue)
                del queue[minIndex]
                
                closedList.append(currentNode.getTo_node_id())
                currentPath = self.findPath(currentNode)
                print(currentPath)
                if currentNode.getTo_node_id() == goalId:
                    found = True
                    break
                else:
                    adjIdList = []
                    if currentNode.getTo_node_id() in self.node_table:
                        adjIdList = self.node_table[currentNode.getTo_node_id()][3]
                    for i in range(len(adjIdList)):
                        if not adjIdList[i][1] in closedList:
                            gCost = self.calShortestPathGCost( currentPath + [adjIdList[i]] )#* 
                            hCost = self.calShortestPathHCost( adjIdList[i][1], goalId )  
                            #self.addToOpen(ANode(adjIdList[i][0], adjIdList[i][1], currentNode, gCost, hCost), queue)  
                            queue.append(ANode(adjIdList[i][0], adjIdList[i][1], currentNode, gCost, hCost))
                

            if not found:   
                print ('Empty Queue!:shortestPath')
                return []
            else:
                walk = self.findPath(currentNode)
                return walk
lines = {1 : ["Bakerloo", 23.2],
        2 : ["Central", 74],
        3 : ["Circle", 27.2],
        6 : ["Jubilee", 36.2],
        8 : ["Northern", 58],
        9 : ["Piccadilly", 71],
        10 : ["Victoria", 21]
         }

stations = {1 : ["Notting Hill Gate", 51.509028, -0.1962847, [[2, 17], [3, 2]]],
            2 : ["High Street Kensington", 51.5003459144, -0.1923516640, [[3, 1], [3, 3]]],
            3 : ["Gloucester Road", 51.49408266, -0.17295341, [[3, 4],[3, 2], [9, 4]]],
            4 : ["South Kensington", 51.494066, -0.172791, [[3, 3], [3, 5], [9, 3], [9, 18]]],
            5 : ["Sloane Square", 51.49258474, -0.156090904, [[3, 4], [3, 6]]],
            6 : ["Victoria", 51.49662869, -0.14400853, [[3, 5], [3, 7], [10, 20]]],
            7 : ["St.James's Park", 51.49971, -0.13394, [[3, 6], [3, 8]]],
            8 : ["Westminster", 51.50121, -0.12489, [[3, 7], [3, 9], [6, 20]]],
            9 : ["Embankment", 51.50717, -0.12195, [[3, 8], [8, 10], [3, 39]]],
            10 : ["Charing Cross", 51.507108, -0.122963, [[8, 9], [8, 11], [1, 21], [1, 9]]],
            11 : ["Leicester Square", 51.51148, -0.12849, [[8, 10], [8, 12], [9, 21], [9, 46]]],
            12 : ["Tottenham Court Road", 51.51640, -0.13027, [[8, 11], [2, 13], [2, 44], [8, 42]]],
            13 : ["Oxford Circus", 51.51517, -0.14119, [[2, 12], [2, 14], [1, 21], [10, 20], [10, 41], [1, 40]]],
            14 : ["Bond Street", 51.51461, -0.14897, [[2, 13], [2, 15], [6, 20], [6, 24]]],
            15 : ["Marble Arch", 51.5135970, -0.15869195, [[2, 14], [2, 16]]],
            16 : ["Lancaster Gate", 51.512083, -0.175067, [[2, 15], [2, 17]]],
            17 : ["Queensway", 51.510484, -0.187050, [[2, 16], [2, 1]]],
            
            18 : ["Knightsbridge", 51.50169, -0.16030, [[9, 4], [9, 19]]],
            19 : ["Hyde Park Corner", 51.50313, -0.15278, [[9, 18], [9, 20]]],
            20 : ["Green Park", 51.50674, -0.14276, [[9, 19], [10, 6], [6, 8], [9, 21], [10, 13], [6, 14]]],
            21 : ["Piccadilly Circus", 51.51022, -0.13392, [[9, 20], [1, 10], [9, 11], [1, 13]]],

            22 : ["Bayswater", 51.51224, -0.187569, [[3, 23], [3, 1]]],
            23 : ["Edgware Road", 51.520195, -0.166986, [[3, 22], [3, 24]]],
            24 : ["Baker Street", 51.52265, -0.15704, [[3, 23], [1, 40], [3, 25], [6, 14]]],
            25 : ["Great Portland Street", 51.52391, -0.14397, [[3, 24], [3, 26]]],
            26 : ["Euston Square", 51.52584, -0.13570, [[3, 25], [3, 47]]],
            27 : ["Farringdon", 51.520362948, -0.105126482, [[3, 47], [3, 28]]],
            28 : ["Barbican", 51.520865, -0.097758, [[3, 27], [3, 29]]],
            29 : ["Moorgate", 51.51817, -0.08859, [[3, 28], [3, 30], [8, 33], [8, 32]]],
            30 : ["Liverpool Street", 51.517675, -0.0824580, [[2, 33], [3, 36], [3, 29]]],
            31 : ["Tower Hill", 51.509910, -0.076813, [[3, 30], [3, 32],[3,36]]],
            32 : ["Monument", 51.510165, -0.085991, [[3, 31], [3, 34], [2, 35], [2, 30], [8, 29]]],
            33 : ["Bank", 51.5134047, -0.08905843, [[3, 31], [3, 34], [2, 35], [2, 30], [8, 29]]],
            34 : ["Cannon Street", 51.51141, -0.09047, [[3, 32], [3, 37]]],
            35 : ["St.Paul's", 51.515285, -0.097598, [[2, 33], [2, 45]]],
            36 : ["Aldgate", 51.51394, -0.07537, [[3, 30], [3, 31]]],
            37 : ["Mansion House", 51.51256, -0.09397, [[3, 34], [3, 38]]],
            38 : ["Blackfriars", 51.5114403, -0.10419050, [[3, 37], [3, 39]]],
            39 : ["Temple", 51.51114, -0.11341, [[3, 38], [3, 9]]],
            40 : ["Regent's Park", 51.52344, -0.14713, [[1, 24], [1, 13]]],
            41 : ["Warran Street", 51.52450, -0.13810, [[8, 42], [10, 13]]],
            42 : ["Goodge Street", 51.52060, -0.13441, [[8, 12], [8, 41]]],
            43 : ["Russell Sqaure", 51.523243, -0.124336, [[9, 44], [9, 47]]],
            44 : ["Holborn", 51.51711, -0.12055, [[2, 12], [2, 45], [9, 47], [9, 46]]],
            45 : ["Chancery Lane", 51.51836, -0.11115, [[2, 44], [2, 35]]],
            46 : ["Covent Garden", 51.51308, -0.12427, [[9, 44], [9, 11]]],
            47 : ["King's Cross St.Pancras", 51.53057, -0.12399, [[9, 43], [3, 27]]]
            }

test=minDistanceSearch(stations,lines)
path=test.shortestPathSearch(7, 27)
print("from:",stations[path[0][1]][0])
for i in range (1,len(path)):
    print("("+str(i)+") Using:",lines[path[i][0]][0],"line to",stations[path[i][1]][0])
