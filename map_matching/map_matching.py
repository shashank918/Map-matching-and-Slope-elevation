
from linkdata import Link
from probedata import Probe
import argparse

if __name__ == "__main__":
	# https://docs.python.org/2/library/argparse.html
	# Here we are building argument parsers and splitting into arguments
	a = argparse.ArgumentParser()
	a.add_argument("-ld", "--Link_directory", default = "Partition6467LinkData.csv",
		help = "Directory's path consisting of Link Data")
	a.add_argument("-pd", "--Probe_directory", default = "test_file.csv",
		help = "Directory's path consisting of Probe Data")
	a.add_argument("-rd", "--Result_directory", default="Output/Partition6467MatchedPoints.csv",
		help = "Directory's path consisting of Resultant Data")
		#  vars returns a dictionary that represents a symbol table
	b = vars(a.parse_args())

	# This is to initialize a list of link data and a probe file line count  
	linkdata = []; file_Count = 0 
	
   # Reading the data from link file, storing  them into Link objects and appending them to list
	with open(b["Link_directory"]) as street_data_collection:
		for c in street_data_collection:
			d = Link(c)			
			linkdata.append(d)
	
	# Previous content is erased by clearing out Result Directory
	Output_data = open(b["Result_directory"],'w'); Output_data.close()
	
	# Command to open probe data file
	with open(b["Probe_directory"]) as prb_data:
		Output_data = open(b["Result_directory"],'w+')
		header = '''sampleID,	
		            dateTime,	
		            sourceCode,	
		            latitude,	
		            longitude,	
		            altitude,	
		            speed,		
		            heading,		
		            linkPVID,	
		            direction,	
		            distFromRef,	
		            distFromLink'''
		header = header.replace(" ", "")		
		header = header.replace("\n", "")		
		header = header.replace("\t", "")		
		Output_data.write(header+"\n")
		print ("Time consumption is calculated..")
		s=0
		for e in prb_data:
			print(s)
			s=s+1
			prb = Probe(e)
			point = map(float, [prb.latitude, prb.longitude])
			Least_Dist = 0
			pos_Edge_Index = 0
			distFromRef = 0

			# For every probe point, find the nearest link and distance from ref. node by taking into account all the edges of link
			for f in linkdata:
				
				distanceto_part = []
				
				h = f.getShapeInfo()
				nodes = h.split("|")   
				partsOfStreet = []
				for i in range(0, len(nodes)-1):
					lati_1, long_1, elev_1 = nodes[i].split('/')
					lati_2, long_2, elev_2 = nodes[i+1].split('/')
					start = map(float, [lati_1, long_1])
					end   = map(float, [lati_2, long_2])
					partsOfStreet.append((start,end))
				
				for z in partsOfStreet:
					start, end = z
					distance_TomapMatchedPoint, map_MatchedPoint = prb.point_line(point, start, end)
					distance_TomapMatchedPoint = distance_TomapMatchedPoint*1000
					distanceto_part.append(distance_TomapMatchedPoint)			  
				Current_Dist = min(distanceto_part)
				if f is linkdata[0]:
					Least_Dist = Current_Dist
					Nearest_Link = f.linkPVID
					pos_Edge_Index = distanceto_part.index(Current_Dist)
					distFromRef = f.getDistFromRef(pos_Edge_Index, map_MatchedPoint)
				elif Current_Dist<Least_Dist:
					Least_Dist = Current_Dist
					Nearest_Link = f.linkPVID
					pos_Edge_Index = distanceto_part.index(Current_Dist)
					distFromRef = f.getDistFromRef(pos_Edge_Index, map_MatchedPoint)

			# Leave out those probe points as unmatched which cannot find a nearest link with specified threshold distance
			if Least_Dist > 15:  #Converting km to m
				continue
			
			
			if file_Count == 0:
				prev_Distance = distFromRef
				prev_LinkId = Nearest_Link
				direction = 'X'
				prev_SampleID = prb.sampleID
			else:
				if prb.sampleID == prev_SampleID and prev_LinkId == Nearest_Link:
					if distFromRef < prev_Distance:
						direction = 'T'
					elif distFromRef > prev_Distance:
						direction = 'F'
					else:
						direction = 'X'
				else:
					direction = 'X'
				prev_Distance = distFromRef
				prev_LinkId = Nearest_Link
				prev_SampleID = prb.sampleID
			
							
			data = 	 prb.sampleID+","			\
					+prb.dateTime+","         \
					+prb.sourceCode+","       \
					+str(prb.latitude)+","    \
					+str(prb.longitude)+","   \
					+prb.altitude+","         \
					+prb.speed+","            \
					+prb.heading+","          \
					+Nearest_Link+","            \
					+direction+","              \
					+str(distFromRef)+","       \
					+str(Least_Dist)
			data = data.replace("\n","")
			Output_data.write(data+"\n");
			file_Count += 1 
			Output_data.flush()
		Output_data.close(); 
			
