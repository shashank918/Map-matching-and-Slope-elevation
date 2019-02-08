
# Getting Link and Probe classes to store data in a structured manner
# Arg parse is to parse commandline arguments
from linkdata import Link
from probedata import Probe 
import argparse
import math

if __name__ == "__main__":
	#https://docs.python.org/2/library/argparse.html
	# Here we are building argument parsers and splitting into arguments
	x = argparse.ArgumentParser()
	x.add_argument("-ld", "--Link_directory", default = "Partition6467LinkData.csv",
		help = "Directory's path consisting of link data")
	x.add_argument("-pd", "--Probe_directory", default = "Partition6467MatchedPoints.csv",
		help = "Directory's path consisting of probe points")
	x.add_argument("-rd", "--Result_directory", default="Output/",
		help = "Directory's path consisting of resultant data")
	#  vars returns a dictionary that represents a symbol table
	y = vars(x.parse_args())

	# This is to initialize a list of link data and a probe file line count 
	Link_data = []; file_Count = 0 
	
	# Reading the data from link file, storing  them into Link objects and appending them to list
	#print "Generation of Link objects"; 	
	with open(y["Link_directory"]) as street_data_collection:
		for b in street_data_collection:
			lnk = Link(b)			
			Link_data.append(lnk)
			
	# Previous content is erased by clearing out Result Directory
	elevation_data = open(y["Result_directory"]+"Elevation.csv",'w'); elevation_data.close()
	slopeOutputdata = open(y["Result_directory"]+"SlopeOutput.csv",'w'); slopeOutputdata.close()
	
	# Command to open probe data file
	with open(y["Probe_directory"]) as probe_data:
		elevation_data = open(y["Result_directory"]+"Elevation.csv",'w+')
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
		            distFromLink,
					slope'''
		header = header.replace(" ", "")		
		header = header.replace("\n", "")		
		header = header.replace("\t", "")
		elevation_data.write(header+"\n")
		
		previous_probe = None
		#print "Generation of the slope at each map matched point"; 		
		print "Time consumption is calculated.."; 		
		for c in probe_data:
			prb = Probe(c)
			if not previous_probe:
				prb.slope = 'X'
			elif prb.linkPVID != previous_probe.linkPVID:
				prb.slope = 'X'
			else:
				
				#                 SLOPE OF LINK IS CALCULATED AS                #

				opposite = float(prb.altitude) - float(previous_probe.altitude)
				start = map(float, [prb.longitude, prb.latitude])
				end = map(float, [previous_probe.longitude, previous_probe.latitude])
				#import pdb;pdb.set_trace()
				hypotenuse = prb.haversine(start[0],start[1],end[0],end[1])/1000
				
				prb.slope = math.atan(opposite/hypotenuse)# formula to calculate slope
				prb.slope = (2*math.pi*prb.slope)/360			

				for lnk in Link_data:
					if prb.linkPVID == lnk.linkPVID and lnk.slopeInfo != '':
						lnk.ProbePoints.append(prb)    
						break
				
					
			data = 	 prb.sampleID+","			\
					+prb.dateTime+","         \
					+prb.sourceCode+","       \
					+str(prb.latitude)+","    \
					+str(prb.longitude)+","   \
					+prb.altitude+","         \
					+prb.speed+","            \
					+prb.heading+","          \
					+prb.linkPVID+","      \
					+prb.direction+","        \
					+str(prb.distFromRef)+"," \
					+str(prb.distFromLink)+","   \
					+str(prb.slope)
			f = data.replace("\n","")
			elevation_data.write(data+"\n");
			file_Count += 1 # Increment line number
			elevation_data.flush()
			previous_probe = prb
		elevation_data.close(); 

	#print "Lets use the slopes at diffferent probe points to calculate slope of the link"; 
        print "To calculate slope of the link,slopes at different probe points are used";
	# Iterate over link data to consolidate slope derived from probe points
	slopeOutputdata= 'linkPVID,  GivenMeanSlope, CalculatedMeanSlope'
	slopeOutputdata_data = open(y["Result_directory"]+"SlopeOutput.csv",'a') 
	slopeOutputdata_data.write(slopeOutputdata+"\n");
	m=0
	for a in Link_data:
		# If link has some map matched points, find the mean and cumulative slope of all those points, provided 
		# they don't have undefined slope. Also negate slope, if probe direction is away from ref node
		if len(a.ProbePoints) > 0:
			Sum_Value = 0.0; nonZeroProbe_Count = 0
			given_Slope = []; g_SlopeSum = 0.0
			calMean_Slope = 0.0; g_MeanSlope = []
			for d in a.ProbePoints:
				if d.direction == "T":
					d.slope = -d.slope
					
				if d.slope != "X" and d.slope != 0:
					Sum_Value = Sum_Value + d.slope
					nonZeroProbe_Count += 1	
			
			if nonZeroProbe_Count != 0:
				calMean_Slope = Sum_Value/nonZeroProbe_Count
				calCumSlope = Sum_Value
			else:
				calMean_Slope = 0

			# Mean of given slope info for the link
			given_Slope = a.slopeInfo.strip().split('|')	
			for e in given_Slope:
				g_SlopeSum += float(e.strip().split('/')[1])

			g_MeanSlope = g_SlopeSum/len(given_Slope)  	
			
			print (m)
			m=m+1
			# given and calculated slope values are written to output file
			# slopeOutputdata =  "For linkID %s, given mean slope is %f; Calculated mean slope is %f" %(a.linkPVID,g_MeanSlope,calMean_Slope)
			# print slopeOutputdata
			slopeOutputdata = "%s, %f, %f" % (a.linkPVID,  g_MeanSlope, calMean_Slope)
			slopeOutputdata_data.write(slopeOutputdata+"\n");
	slopeOutputdata_data.close();
			
