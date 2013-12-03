#! /usr/bin/python

####
#
#

import sys,re,math

def main():
	Max={}
	Min={}
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=2
	Min['Dims']=1
	Max['Stride']=2 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['d','s']	
	Init='index0*10+index0'
	DS='i'
	size=[10,20,10,100000];
	
	for NumVars in range(Min['Vars'],Max['Vars']+1):
		for NumDims in range(Min['Dims'],Max['Dims']+1):
			SizeString=''
			for i in range(NumDims-1):
				SizeString=','+str(size[Max['Dims']-1-i])+str(SizeString)
			if(NumDims==1):
				SizeString=str(size[Max['Dims']-1])
			else:
				SizeString=str(size[Max['Dims']-1])+str(SizeString)
			for BaseOfStride in range(Min['Stride'],Max['Stride']+1):
				Stride=2**BaseOfStride
				for CurrAlloc in Alloc:
					ConfigFile="Config_"+str(NumVars)+"vars_"+str(NumDims)+"dims_"+str(Stride)+"stride_alloc_"+str(CurrAlloc)+".txt"
					print "\n\t Config file: "+str(ConfigFile)
					f=open(ConfigFile,'w')
					f.write("\n\t #vars "+str(NumVars))
					f.write("\n\t #dims "+str(NumDims))
					f.write("\n\t #stride "+str(Stride))
					f.write("\n\t #size "+str(SizeString))
					f.write("\n\t #allocation "+str(CurrAlloc) )
					f.write("\n\t #init "+str(Init))
					f.write("\n\t #datastructure "+str(DS))
					f.close()
	
	




if __name__=="__main__":
	main() #sys.argv[1:])
