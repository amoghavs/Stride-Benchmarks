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
	Max['Dims']=3
	Min['Dims']=2
	Max['Stride']=2 # ie., 2^4
	Min['Stride']=2 # ie., 2^0=1
	Alloc=['d','s']	
	Init='index0*10+index0'
	DS='i'
	SpatWindow=[8,16,32];
	MbyteSize=10 # 32Mbyte= 2^20[1M] * 2^5 [32] * 2^3[byte]
	MaxSize=2**MbyteSize
	Dim0Size=2**(MbyteSize-8)
	HigherDimSize= MaxSize/	Dim0Size
	
	
	MasterSWStats=open("MasterSWStats.txt",'w')
	for NumVars in range(Min['Vars'],Max['Vars']+1):
		for NumDims in range(Min['Dims'],Max['Dims']+1):
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

					CMDrunStrideBenchmarks='python StrideBenchmarks.py -c '+str(ConfigFile)
					commands.getoutput(CMDrunStrideBenchmarks)
					SRCCode='StrideBenchmarks_'+str(UniqueID)+'.c'
					EXE='StrideBenchmarks_'+str(UniqueID)
					CMDCompileSRC='gcc -O3 -g '+str(SRCCode)+' -o '+str(EXE)
					commands.getoutput(CMDCompileSRC)
					CMDPebilCompile='pebil --typ sim --inp SimInp.log --app '+str(EXE)
					commands.getoutput(CMDPebilCompile)
					
					
					SWStats=open(str('SWStats_'+str(Config)+'.txt'),'w')
					MasterSWStats.write("\n\t ###########################################")
					MasterSWStats.write("\n\t Config dir: "+str(Config))
					for CurrSW in SpatWindow:
						SWStats.write("\n\t---------------------")
						MasterSWStats.write("\n\t---------------------")
						SWStats.write("\n\t Spatial-window size: "+str(CurrSW)+"\n\n")
						MasterSWStats.write("\n\t Spatial-window size: "+str(CurrSW)+"\n\n")

						CMDExportSW='export METASIM_SPATIAL_WINDOW='+str(CurrSW)
						SimInst=str(EXE)+'.siminst'
						CMDRunSiminst='./'+str(SimInst)
						CMDExportSW+=' |'+CMDRunSiminst
						commands.getoutput(CMDExportSW)
						SWFile='SW_'+str(CurrSW)+'_'+str(Config)+'.log'
						CMDRenameSpatial='mv *.spatial '+str(SWFile)
						commands.getoutput(CMDRenameSpatial)
						CMDgrep='grep Total '+str(SWFile)
						GrepOutput=commands.getoutput(CMDgrep)

						Access=re.match(r'\s*.*\:\s*(\d+)+$',GrepOutput)
						if Access:
							TotalAccess=int(Access.group(1))
							#print "\n\t Total Accesses as found out: "+str(TotalAccess)+" and grep output: "+str(GrepOutput)							
						
						f=open(SWFile,'r')
						SWFileContents=f.readlines()
						f.close()
						SWStats.write( "\n\t\t Bin: \t\t Range: \t\t Count: \t\t Percentage ")						
						MasterSWStats.write( "\n\t\t Bin: \t\t Range: \t\t Count: \t\t Percentage ")
						for CurrLine in SWFileContents:
							Data=re.match(r'\s*.*Bin\:\s*(\d+)+.*Range\:\s*(\d+)+.*Count\:\s*(\d+)+$',CurrLine)	
							if Data:
								SWStats.write( "\n\t\t "+str(Data.group(1))+"\t\t "+str(Data.group(2))+"\t\t "+str(Data.group(3))+"\t\t "+str( 100* float(Data.group(3)) / TotalAccess )  )
								MasterSWStats.write( "\n\t\t "+str(Data.group(1))+"\t\t "+str(Data.group(2))+"\t\t "+str(Data.group(3))+"\t\t "+str( 100* float(Data.group(3)) / TotalAccess )  )								
								#SWStats.write( "\n\t Bin: "+str(Data.group(1))+"\t Range: "+str(Data.group(2))+"\t Count: "+str(Data.group(3))+"\t % "+str( 100* float(Data.group(3)) / TotalAccess )  )
								#print "\n\t Bin: "+str(Data.group(1))+" Range: "+str(Data.group(2))+" Count: "+str(Data.group(3))+" % "+str( 100* float(Data.group(3)) / TotalAccess ) 
						
						SWStats.write("\n\n")		
						MasterSWStats.write("\n\n")
					SWStats.close()
					CMDMvAll='mv *.c SW* *siminst* '+str(ConfigFile)+' '+str(EXE)+' '+str(Config)
					commands.getoutput(CMDMvAll)
					CMDRmMetaFiles='rm -f *Instructions* LRU*'
					commands.getoutput(CMDRmMetaFiles)
					#CMD
	MasterSWStats.close()
					
			
	




if __name__=="__main__":
	main() #sys.argv[1:])
