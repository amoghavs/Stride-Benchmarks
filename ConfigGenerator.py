#! /usr/bin/python

####
#
#

import sys,re,math,commands

def main():
	Max={}
	Min={}
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=5
	Min['Dims']=1
	Max['Stride']=0 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['d']	
	Init='index0*10+index0'
	DS='i'
	SpatWindow=[8,16,32];
	MbyteSize=28 # 32Mbyte= 2^20[1M] * 2^5 [32] * 2^3[byte]
	MaxSize=2**MbyteSize
	Dim0Size=2**(MbyteSize-8)
	HigherDimSize= MaxSize/	Dim0Size
	for NumVars in range(Min['Vars'],Max['Vars']+1):
		for NumDims in range(Min['Dims'],Max['Dims']+1):

			
			#print "\n\t SizeString: "+str(SizeString)+" and SizeName: "+str(SizeName)
			for BaseOfStride in range(Min['Stride'],Max['Stride']+1):
				Stride=2**BaseOfStride
				SizeString=''
				SizeName=''				
				if (NumDims>1):
					ResolveBases=1
					IncrementLastDim=0
					while ResolveBases:
						EachDimBase=( math.log(float(HigherDimSize),2) - IncrementLastDim)/(NumDims-1)
						if(int(EachDimBase)==EachDimBase):
							ResolveBases=0
						else:
							IncrementLastDim+=1					
					
					print "\n\t NumDims: "+str(NumDims)+" Each Dim Base: "+str(EachDimBase)+" IncrementLastDim: "+str(IncrementLastDim)
					EachDimSize=int(2**EachDimBase)
					for i in range(NumDims-2):
						SizeString=str(EachDimSize)+','+str(SizeString)
						SizeName=str(EachDimSize)+'_'+str(SizeName)
					
					SizeString=str(SizeString)+str(int(EachDimSize*(2**IncrementLastDim)))+','+str(Dim0Size)
					SizeName=str(SizeName)+str(int(EachDimSize*(2**IncrementLastDim)))+'_'+str(Dim0Size)
					
				else:
					SizeString=MaxSize
					SizeName=MaxSize
				print "\n\t SizeName: "+str(SizeName)+" SizeString "+str(SizeString)
				
				for CurrAlloc in Alloc:
					UniqueID=str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_'+str(Stride)+"stride"
					Config="Config_"+UniqueID
					ConfigFile=str(Config)+'.txt'
					CMDConfigDir='mkdir '+str(Config)
					commands.getoutput(CMDConfigDir)
					print "\n\t Config file: "+str(ConfigFile)
					f=open(ConfigFile,'w')
					f.write("\n#vars "+str(NumVars))
					f.write("\n#dims "+str(NumDims))
					f.write("\n#stride "+str(Stride))
					f.write("\n#size "+str(SizeString))
					f.write("\n#allocation "+str(CurrAlloc) )
					f.write("\n#init "+str(Init))
					f.write("\n#datastructure "+str(DS))
					f.close()
					#CMDmvConfigFile='mv '+str(ConfigFile)+' '+str(Config) 
					#commands.getoutput(CMDmvConfigFile)					
					#CMDcpStrideBenchmarks='cp StrideBenchmarks.py '+str(Config)
					#commands.getoutput(CMDcpStrideBenchmarks)
					CMDrunStrideBenchmarks='python StrideBenchmarks.py -c '+str(ConfigFile)
					#print "\n\t Run: "+str(CMDrunStrideBenchmarks)
					commands.getoutput(CMDrunStrideBenchmarks)
					SRCCode='StrideBenchmarks_'+str(UniqueID)+'.c'
					EXE='StrideBenchmarks_'+str(UniqueID)
					#print "\n\t SRC: "+str(SRCCode)
					#CMDmvSRCCode='mv '+str(SRCCode)+' '+str(Config)
					#commands.getoutput(CMDmvSRCCode)
					CMDCompileSRC='gcc -g '+str(SRCCode)+' -o '+str(EXE)
					commands.getoutput(CMDCompileSRC)
					CMDPebilCompile='pebil --typ sim --inp SimInp.log --app '+str(EXE)
					commands.getoutput(CMDPebilCompile)
					
					for CurrSW in SpatWindow:
						CMDExportSW='export METASIM_SPATIAL_WINDOW='+str(CurrSW)
						#commands.getoutput(CMDExportSW)
						#
						SimInst=str(EXE)+'.siminst'
						CMDRunSiminst='./'+str(SimInst)
						CMDExportSW+=' |'+CMDRunSiminst
						commands.getoutput(CMDExportSW)
						#print "\n\t "+str(CMDExportSW)
						CMDRenameSpatial='mv *.spatial'+' SW_'+str(CurrSW)+'_'+str(Config)
						commands.getoutput(CMDRenameSpatial)
					
					CMDMvAll='mv *.c SW* *siminst* '+str(ConfigFile)+' '+str(EXE)+' '+str(Config)
					print "\n\t Mv command: "+str(CMDMvAll)
					commands.getoutput(CMDMvAll)
					CMDRmMetaFiles='rm -f *Instructions* LRU*'
					commands.getoutput(CMDRmMetaFiles)
					#CMD
					
			
	




if __name__=="__main__":
	main() #sys.argv[1:])
