import math

class Link(object):
	def __init__(self, line):
		self.linkPVID		  ,\
		self.refNodeID		  ,\
		self.nrefNodeID		  ,\
		self.length			  ,\
		self.functionalClass  ,\
		self.directionOfTravel,\
		self.speedCategory	  ,\
		self.fromRefSpeedLimit,\
		self.toRefSpeedLimit  ,\
		self.fromRefNumLanes  ,\
		self.toRefNumLanes	  ,\
		self.multiDigitized	  ,\
		self.urban			  ,\
		self.timeZone		  ,\
		self.shapeInfo		  ,\
		self.curvatureInfo	  ,\
		self.slopeInfo		  = line.strip().split(',')
		self.ReferenceNodeLat,self.ReferenceNodeLong,_  = self.shapeInfo.split('|')[0].split('/')
		self.ReferenceNode = map(float, (self.ReferenceNodeLat,self.ReferenceNodeLong))
		self.ProbePoints   = []
	def getShapeInfo(self):
		return self.shapeInfo
				
		
	def haversine(self,lon1, lat1, lon2, lat2):
     
		rlon1 = lon1 * (math.pi/180)
		rlat1 = lat1 * (math.pi/180)
		rlat2 = lat2 * (math.pi/180)
		rlon2 = lon2 * (math.pi/180)
    
    #haversine formula
		rlon = rlon2 - rlon1
		rlat = rlat2 - rlat1
	#h = (math.sin(rlat/2)*2) + (math.cos(rlat1)*math.cos(rlat2) math.sin(rlon/2)**2)
		h= math.sin(rlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(rlon/2)**2
		dist = 2 * 6371 * math.asin(math.sqrt(h))
		return dist

 
	
	def getDistFromRef(self, indexOfEdge, mapMatchedPoint):
	
		street = self.shapeInfo
		nodes = street.split("|")   
		partsOfStreet = []
		for i in range(0, len(nodes)-1):
			lat1, lon1, ele1 = nodes[i].split('/')
			lat2, lon2, ele2 = nodes[i+1].split('/')
			start = map(float, [lat1, lon1])
			end   = map(float, [lat2, lon2])
			partsOfStreet.append((start,end))
		
		distFromRef = 0
		for i in range(indexOfEdge-1):
			
			start = map(float, partsOfStreet[i][0])
			end = map(float, partsOfStreet[i][1])
				
			distFromRef += self.haversine(start[1],start[0],end[1],end[0])
		start1 = map(float, partsOfStreet[indexOfEdge][0])
		end1 = map(float, mapMatchedPoint)
		distFromRef += self.haversine(start1[1],start1[0],end1[1],end1[0])
		return distFromRef*1000
			
		
