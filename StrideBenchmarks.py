#!/usr/bin/python

import sys, getopt,re

def usage():
	print "StrideBenchmarks.py -c/--config file with all the configuration.\n "


def main(argv):
	config=''
	try:
	   opts, args = getopt.getopt(sys.argv[1:],"c:h:v",["config","help","verbose"])
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
	   usage()
	   sys.exit(2)
	verbose=False   
	for opt, arg in opts:
	   if opt == '-h':
	      print 'test.py -i <inputfile> -o <outputfile>'
	      sys.exit()
	   elif opt in ("-c", "--config"):
	      config=arg
	      print "\n\t Config file is "+str(config)+"\n";
           else:
   		usage()

	# If execution has come until this point, the script should have already identified the config file.
	ConfigHandle=open(config)
	ConfigContents=ConfigHandle.readlines()
	ConfigHandle.close()
	
	# At this point the config should be read completely.
	ConfigParams={}
	ConfigParams['size']=[]
	ConfigParams['stride']=[]
	ConfigParams['alloc']=[]		
	LineCount=0;
	DimNotFound=1;
	SizeNotFound=1;
	StrideNotFound=1;
	AllocNotFound=1;
	ThisArray=[]
	# Tabs: 1
	for CurrLine in ConfigContents:
		LineCount+=1;
		LineNotProcessed=1
		# Tabs: 2
		if DimNotFound:
			MatchObj=re.match(r'\s*\#dims',CurrLine)
			if MatchObj:
				DimsLine=re.match(r'\s*\#dims\s*(\d+)*',CurrLine)
				if DimsLine:
					Dims=int(DimsLine.group(1))
					print "\n\t Number of dims is "+str(Dims)+"\n"	
					LineNotProcessed=0
					DimNotFound=0
		else:
			if SizeNotFound:
				MatchObj=re.match(r'\s*\#size',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Sizes=re.split(',',tmp[1])
					if Sizes:
						SizeNotFound=0;
						LineNotProcessed=0
						CurrDim=0;
						for CurrSize in Sizes:
							ConfigParams['size'].append( CurrSize);
							CurrDim+=1				
							print "\n\t Size for dim "+str(CurrDim)+" is "+str(CurrSize)+"\n" 
						if(CurrDim != Dims):
							print "\n\t The size parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(Dims)+"\n";
							sys.exit(0)

			if StrideNotFound:
				MatchObj=re.match(r'\s*\#stride',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Strides=re.split(',',tmp[1])
					if Strides:
						StrideNotFound=0
						LineNotProcessed=0
						CurrDim=0;
						for CurrStride in Strides:
							ConfigParams['stride'].append( CurrStride);
							CurrDim+=1				
							print "\n\t Stride for dim "+str(CurrDim)+" is "+str(CurrStride)+"\n" 
						if(CurrDim != Dims):
							print "\n\t The size parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(Dims)+"\n";
							sys.exit(0)	

			if AllocNotFound:
				MatchObj=re.match(r'\s*\#alloc',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Allocs=re.split(',',tmp[1])
					if Allocs:
						AllocNotFound=0
						LineNotProcessed=0
						CurrDim=0;
						for CurrAlloc in Allocs:
							ConfigParams['alloc'].append( CurrAlloc);
							CurrDim+=1				
							print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrAlloc)+"\n" 					
						if(CurrDim != Dims):
							print "\n\t The size parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(Dims)+"\n";
							sys.exit(0)		
		if LineNotProcessed:
			print "\n\t Info is not processed in line: "+str(LineCount)+"\n";
		
		
			
	if(~(DimNotFound and SizeNotFound and StrideNotFound and AllocNotFound)):
		print "\n\t The config file has all the required info: #dims, size and allocation for all the dimensions"	
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
					



if __name__ == "__main__":
   main(sys.argv[1:])
