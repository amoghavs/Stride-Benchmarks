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
	Max['Dims']=2
	Min['Dims']=1
	Max['Stride']=1 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['d']	
	Init='index0*10+index0'
	DS='i'
	size=[10,10,10,1000];
	SpatWindow=[8,16,32];
	
	for NumVars in range(Min['Vars'],Max['Vars']+1):
		for NumDims in range(Min['Dims'],Max['Dims']+1):
			SizeString=''
			SizeName=''
			for i in range(NumDims-1):
				SizeString=str(size[Max['Dims']-2-i])+','+str(SizeString)
				SizeName=str(size[Max['Dims']-2-i])+'_'+str(SizeName)
			if(NumDims==1):
				SizeString=str(size[Max['Dims']-1])
				SizeName=str(size[Max['Dims']-1])
			else:
				SizeString=str(SizeString)+str(size[Max['Dims']-1])
				SizeName=str(SizeName)+str(size[Max['Dims']-1])
			
			#print "\n\t SizeString: "+str(SizeString)+" and SizeName: "+str(SizeName)
			for BaseOfStride in range(Min['Stride'],Max['Stride']+1):
				Stride=2**BaseOfStride
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
