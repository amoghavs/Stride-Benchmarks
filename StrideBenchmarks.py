#!/usr/bin/python

#### Pending items:
# * To allocate stride*limit number of elements.
# * To write allocated elements into a file.
#

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
	ConfigParams['datastructure']=[]	
	ConfigParams['Dims']=''
	ConfigParams['NumVars']=''	
	LineCount=0;
	DimNotFound=1;
	SizeNotFound=1;
	StrideNotFound=1;
	AllocNotFound=1;
	DSNotFound=1;
	ThisArray=[]
	NumVars=0
	NumVarNotFound=1
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
					ConfigParams['Dims']=Dims
					LineNotProcessed=0
					DimNotFound=0
		if NumVarNotFound:
			MatchObj=re.match(r'\s*\#vars',CurrLine)
			if MatchObj:
				DimsLine=re.match(r'\s*\#vars\s*(\d+)*',CurrLine)
				if DimsLine:
					NumVars=int(DimsLine.group(1))
					ConfigParams['NumVars']=NumVars
					print "\n\t Number of variables is "+str(ConfigParams['NumVars'])+"\n"	
					LineNotProcessed=0
					NumVarNotFound=0			
								
		else:
			if SizeNotFound:
				MatchObj=re.match(r'\s*\#size',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Sizes=re.split(',',tmp[1])
					if Sizes:
						LineNotProcessed=0
						CurrDim=0;
						for CurrSize in Sizes:
							CheckSpace=re.match(r'^\s*$',CurrSize)
						        if(CheckSpace):
						       		print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)
						       	else:
								CurrSize=re.sub(r'^\s*','',CurrSize)
								CurrSize=re.sub(r'\s*$','',CurrSize)						       	
								ConfigParams['size'].append( CurrSize)
								CurrDim+=1				
								print "\n\t Size for dim "+str(CurrDim)+" is "+str(CurrSize)+"\n" 
						if(CurrDim != ConfigParams['Dims']):
							print "\n\t The size parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['Dims'])+"\n";
							sys.exit(0)
						else:
							SizeNotFound=0

			if StrideNotFound:
				MatchObj=re.match(r'\s*\#stride',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Strides=re.split(',',tmp[1])
					if Strides:
						LineNotProcessed=0
						CurrDim=0;
						for CurrStride in Strides:
							CheckSpace=re.match(r'^\s*$',CurrStride)
						        if(CheckSpace):
						       		print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								CurrStride=re.sub(r'^\s*','',CurrStride)
								CurrStride=re.sub(r'\s*$','',CurrStride)							
								ConfigParams['stride'].append( CurrStride);
								CurrDim+=1				
								print "\n\t Stride for dim "+str(CurrDim)+" is "+str(CurrStride)+"\n" 
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The stride parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							StrideNotFound=0	

			if AllocNotFound:
				MatchObj=re.match(r'\s*\#alloc',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Allocs=re.split(',',tmp[1])
					if Allocs:
						LineNotProcessed=0
						CurrDim=0;
						for CurrAlloc in Allocs:
							CheckSpace=re.match(r'^\s*$',CurrAlloc)
						        if(CheckSpace):
						       		print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:	
								CurrAlloc=re.sub(r'^\s*','',CurrAlloc)
								CurrAlloc=re.sub(r'\s*$','',CurrAlloc)					
								ConfigParams['alloc'].append(CurrAlloc);
								CurrDim+=1				
								print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrAlloc)+"\n" 					
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The allocation parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
							
						else:
							AllocNotFound=0	

			if DSNotFound:
				MatchObj=re.match(r'\s*\#datastructure',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					DS=re.split(',',tmp[1])
					if DS:
						LineNotProcessed=0
						CurrDim=0;
						for CurrDS in DS:
							CheckSpace=re.match(r'^\s*$',CurrDS)
						        if(CheckSpace):
						       		print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								CurrDS=re.sub(r'\s*$','',CurrDS)
								ConfigParams['datastructure'].append( CurrDS);
								CurrDim+=1				
								print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrDS)+"\n" 					
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The data structure parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							DSNotFound=0		


		if LineNotProcessed:
			print "\n\t Info is not processed in line: "+str(LineCount)+"\n";
		
		
	#Tabs: 1		
	if(~(NumVarNotFound and DimNotFound and SizeNotFound and StrideNotFound and AllocNotFound and DSNotFound)):
		print "\n\t The config file has all the required info: #dims, size and allocation for all the dimensions"	
		#SrcFileName='StrideBenchmarks_'+str(ConfigParams
		InitAlloc=[]
		indices=[]
		tmp='#include<stdio.h>'
		InitAlloc.append(tmp)
		tmp='#include<stdlib.h>'
		InitAlloc.append(tmp)		
		for i in range(ConfigParams['Dims']):
			indices.append('index'+str(i))
				
		tmp=' int '
		for i in range(ConfigParams['Dims']-1):
			tmp+=indices[i]+','	
		tmp+=indices[len(indices)-1]+';'
		print "\n\t This is how the indices will look: "+tmp+" \n";							
		InitAlloc.append(tmp);			
		for index in range(ConfigParams['NumVars']):
			VarDecl=''
			if(ConfigParams['datastructure'][index]=='f' or ConfigParams['datastructure'][index]=='float'):
				VarDecl='float' 
				print "\n\t Allocated float to variable "+str(index)
			elif(ConfigParams['datastructure'][index]=='d' or ConfigParams['datastructure'][index]=='double'):
				VarDecl='double' 
				print "\n\t Allocated double to variable "+str(index)				
			elif(ConfigParams['datastructure'][index]=='i' or ConfigParams['datastructure'][index]=='integer'):
				VarDecl='int' 
				print "\n\t Allocated integer to variable "+str(index)								
			else:
				print "\n\t Supported datastructure is only float, double, integer. Dimension "+str(index)+" requests one of the nonsupported datastructure: "+str(ConfigParams['datastructure'][index])+"\n"
				sys.exit(0)
				
			if( ConfigParams['alloc'][index]=='d' or ConfigParams['alloc'][index]=='dynamic'):
				datatype=VarDecl
				var=' Var'+str(index)
				prefix=''
				suffix=''
				for CurrDim in range(ConfigParams['Dims']):
				   prefix+='*'
				for CurrDim in range(ConfigParams['Dims']-1):
				   suffix+='*'				   
				VarDecl+=prefix+var
				#print "\n\t This is the prefix: "+str(prefix)+" and this is the suffix: "+str(suffix)+" and this'd be the variable declaration: "+str(VarDecl)+ "\n "
				DynAlloc=[]
				#if(Dims>1):
				tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][0]+' * sizeof('+datatype+suffix+'))'		
				DynAlloc.append(tmp);
				  		
				print "\n\t This is how the first malloc statement look: "+str(tmp)+"\n"

				
				if(ConfigParams['Dims']>1):
					NumForLoops=''
					for i in range(ConfigParams['Dims']-1):
						NumForLoops=i+1
						MallocLHS=var
						for j in range(NumForLoops):
							ThisForLoop='for('+str(indices[j])+'=0 ; '+	str(indices[j])+' < '+str(ConfigParams['size'][j])+' ; '+str(indices[j])+'+=1)'
							print "\n\t ThisForLoop: "+ThisForLoop+" and For-loop index: "+str(j)
							DynAlloc.append(ThisForLoop);
							MallocLHS+='['+str(indices[j])+']'
						prefix=''
						suffix=''
						for CurrDim in range(ConfigParams['Dims']-i-1):
						   prefix+='*'
						for CurrDim in range(ConfigParams['Dims']-i-2):
						   suffix+='*'	

						MallocEqn=MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][0]+' * sizeof('+datatype+suffix+'))'		
						DynAlloc.append(MallocEqn)
				   		print "\t The malloc equation is: "+str(MallocEqn)+"\n"
				
				
			else:
				VarDecl+=' Var'+str(index)
				for CurrDim in range(Dims):
					VarDecl+='['+str(ConfigParams['size'][CurrDim])+']'
				print "\n\t Variable declaration for variable "+str(index)+" is static and is as follows: "+str(VarDecl)+"\n"
				InitAlloc.append(VarDecl)
	
			#InitAlloc[index]=[]
		DynAllocLinesCount=0;
		for i in range(len(DynAlloc)):
			DynAllocLinesCount+=1
			print "\n\t Line: "+str(DynAllocLinesCount)+" contents: "+str(DynAlloc[i])
		
		InitAllocLinesCount=0;
		for i in range(len(InitAlloc)):
			InitAllocLinesCount+=1
			print "\n\t Line: "+str(InitAllocLinesCount)+" contents: "+str(InitAlloc[i])
			
						
	else:
		print "\n\t The config file has DOES NOT HAVE all the required info: #dims, size and allocation for all the dimensions. If this message is printed, there is a bug in the script, please report. "		
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
					



if __name__ == "__main__":
   main(sys.argv[1:])
