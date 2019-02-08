
import math

class Probe(object):
	def __init__(self, line):

		self.sampleID, self.dateTime, self.sourceCode, self.latitude, self.longitude, self.altitude, self.speed, self.heading = line.split(',')
		self.assigned_street  = None
	
	def haversine(lon1, lat1, lon2, lat2):
     
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

	
	def point_line(self,point, startpt, endpt):
 
			x,y = startpt
			X,Y = endpt
			line_vect = (X-x, Y-y)
			m,n = startpt
			M,N = point
			point_vect = (M-m, N-n)		
			x,y = line_vect		
			line_len = math.sqrt(x*x + y*y)		
			a,b = line_vect		
			line_unitvect = (a/line_len, b/line_len)	

			l,m = point_vect
			t = 1.0/line_len
			point_vect_scaled = (x * t, y * t)
		
			e,f = line_unitvect
			E,F = point_vect_scaled
			x = e*E + f*F   
			if x < 0.0:
				x = 0.0
			elif x > 1.0:
				x = 1.0
			
			p,r = line_vect
			nearest = (p * x, r * x)		
			c,d = nearest
			C,D = point_vect
			line_vect1 = (C-c, D-d)		
			j,k = line_vect1	
			dist = math.sqrt(j*j + k*k)	
		
			g,h = nearest
			G,H = startpt
			nearest = (g+G, h+H)
			return (dist, nearest)
		
	
		
