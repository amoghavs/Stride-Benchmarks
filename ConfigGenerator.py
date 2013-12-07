#! /usr/bin/python

####
#
#


import sys,re,math,commands,time

"""def RecursiveStrideGen(TotalStreamLength,StreamLength, NumStrides,CurrStreamLength,CurrString,CurrStringPrefix,CurrStringPrefixPos,ResultString):
	for i in range(NumStrides):
		Result=CurrString+str(i)	
		ResultString.append(Result)
		print "\n\t Result: "+Result
	CurrStreamLength+=1
	TotalStreamLength+=NumStrides
	if(CurrStreamLength==StreamLength):
		return ResultString
	elif(TotalStreamLength<(NumStrides**StreamLength)):
			CurrStreamLength-=1
			CurrStringPrefixPos+=1
			CurrString=CurrStringPrefix+str(CurrStringPrefixPos)
			print '\n\t CurrStringPrefixPos: '+str(CurrStringPrefixPos)+' CurrStreamLength: '+str(CurrStreamLength)
			RecursiveStrideGen(TotalStreamLength,StreamLength, NumStrides,CurrStreamLength,CurrString,CurrStringPrefix,CurrStringPrefixPos,ResultString)
"""

def RecursiveStrideGen(CurrDim,NumDims,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString):
	if(CurrDim==NumDims):
		print "\n\t ++ CurrDim: "+str(CurrDim)
		for i in range(NumStrides):
			Result=CurrString+str(i)	
			ResultString.append(Result)
			print "\n\t Result: "+Result
		CurrDim-=1
		return (CurrDim,CurrPrefixPos)

	#CurrString=CurrPrefix+str(CurrPrefixPos)
	#print "\n\t ++ CurrPrefixPos: "+str(CurrPrefixPos)+' CurrDim: '+str(CurrDim)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)
	#CurrDim=RecursiveStrideGen(CurrDim+1,NumDims,NumStrides,CurrString,CurrString,CurrPrefixPos,ResultString)	
	#CurrString=CurrPrefix+str(CurrPrefixPos+1)	
	#time.sleep(1)
	CurrPrefixPos=0	
	while(CurrPrefixPos!=NumStrides):	
		CurrString=CurrPrefix+str(CurrPrefixPos)
		print "\n\t -- CurrPrefixPos: "+str(CurrPrefixPos)+' CurrDim: '+str(CurrDim)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)		
		print "\n\t $$ CurrDim: "+str(CurrDim)+" CurrPrefixPos: "+str(CurrPrefixPos)
		#time.sleep(1)
		#(CurrDim,Dummy)=
		RecursiveStrideGen(CurrDim+1,NumDims,NumStrides,CurrString,CurrString,CurrPrefixPos,ResultString)
		CurrPrefixPos+=1
		print "\n\t %% CurrDim: "+str(CurrDim)+" CurrPrefixPos: "+str(CurrPrefixPos)		
		#return CurrDim
		
	CurrDim-=1
	#CurrPrefixPos-=1
	print "\n\t ^^ CurrPrefixPos: "+str(CurrPrefixPos)+' CurrDim: '+str(CurrDim)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)	
	return (CurrDim,CurrPrefixPos)	
			
			
def main():
	Max={}
	Min={}
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=4
	Min['Dims']=4
	Max['NumStream']=3
	Min['NumStream']=1
	Max['Stride']=3 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['s']	
	Init='index0*10+index0'
	DS='f'
	SpatWindow=[8,16,32];
	MbyteSize=24 # 2^28=32Mbyte= 2^20[1M] * 2^5 [32] * 2^3[byte]
	MaxSize=2**MbyteSize
	Dim0Size=2**(MbyteSize-8)
	HigherDimSize= MaxSize/	Dim0Size
	
	
	
	
	MasterSWStats=open("MasterSWStats.txt",'w')
	for NumVars in range(Min['Vars'],Max['Vars']+1):
	 # CAUTION: The main loop iterates for 'NumVars' and the config generator should be changed to accommodate #Vars > 1 and not loop over like this! 
	 
	 	ArrayStrideString=[]
	 	ResultString=[]
	 	RecursiveStrideGen(1,4,4,'','',0,ResultString)
	 	print "\n\t Result String length: "+str(len(ResultString))
	 	"""for CurrNumStream in range(Min['NumStream'],Max['NumStream']+1):
	 		#for CurrStride in range(Min['Stride'],Max['Stride']+1):
	 			for StreamNum in range(CurrNumStream):
	 				for CurrStride in range(Min['Stride'],Max['Stride']+1):
	 					PotentialStrideString=str( 2** CurrStride)
	 					StrideStringPrefix=PotentialStrideString
	 					if(CurrNumStream>1):
		 					for CurrStreamStride in range(Min['Stride'],Max['Stride']+1):
		 						PotentialStrideString=StrideStringPrefix
		 						for i in range(StreamNum):
			 						PotentialStrideString+=','+str( 2**CurrStreamStride )
				 				print "\n\t PotentialStrideString: "+str(PotentialStrideString)+' CurrNumStream: '+str(CurrNumStream)+' StreamNum: '+str(StreamNum)
	 
		for NumDims in range(Min['Dims'],Max['Dims']+1):
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

					CMDrunStrideBenchmarks='python StrideBenchmarks.py -c '+str(ConfigFile)
					commands.getoutput(CMDrunStrideBenchmarks)
					SRCCode='StrideBenchmarks_'+str(UniqueID)+'.c'
					EXE='StrideBenchmarks_'+str(UniqueID)
					CMDCompileSRC='gcc -O3 -g '+str(SRCCode)+' -o '+str(EXE)
					commands.getoutput(CMDCompileSRC)
					CMDPebilCompile='pebil --typ jbb --app '+str(EXE)
					commands.getoutput(CMDPebilCompile)
					CMDRunJbb='./'+str(EXE)+'.jbbinst'
					commands.getoutput(CMDRunJbb)
					FuncName='FuncVar0Stride'+str(Stride)+'Dim'+str(NumDims-1)  # CAUTION: This should be changed if >1 variable is going to be used.
					CMDFindBBs='grep '+str(FuncName)+' '+str(EXE)+'.r00000000.t00000001.jbbinst > JBBInfo.txt'
					commands.getoutput(CMDFindBBs)
					jbbfile=open("JBBInfo.txt",'r')
					FuncBlks=jbbfile.readlines()
					FuncBlkstoSimulate=[]
					for BB in FuncBlks:
						#print "\n\t "+str(BB)
						CheckBLK=re.match(r'\s*BLK.*',BB)
						if(CheckBLK):
							GetBBID=re.split('\t',BB)#re.match(r'\s*BLK\s*(\d+)+\s*0x(.*)\s*(\d+)+\s*(\d+)+.*',BB)
							if GetBBID:
								print "\n\t Look Whos here: "+str(GetBBID[2]) #[2])+"!! "
								FuncBlkstoSimulate.append(str(GetBBID[2]))
							
					BBFile=open('BBlist.txt','w')
					#BBFile.write(str(FuncBlkstoSimulate[2]))
					#BBFile.write(str(FuncBlkstoSimulate[3]))
					for BB in range(0,len(FuncBlkstoSimulate)):
						BBFile.write('\n\t'+str(FuncBlkstoSimulate[BB]))

					BBFile.write("\n")
					BBFile.close()

					CMDPebilCompile='pebil --typ sim --app '+str(EXE)+' --inp BBlist.txt'
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
						SWStats.write( "\n\t\t Bin: \t\t Range: \t Count: \t\t Percentage ")						
						MasterSWStats.write( "\n\t\t Bin: \t\t Range: \t Count: \t\t Percentage ")
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
					CMDMvAll='mv *.c SW* *siminst* *jbbinst* BBlist.txt '+str(ConfigFile)+' '+str(EXE)+' '+str(Config)
					commands.getoutput(CMDMvAll)
					CMDRmMetaFiles='rm -f *Instructions* LRU*'
					commands.getoutput(CMDRmMetaFiles)
					#CMD
	MasterSWStats.close()
					"""
					
			
	




if __name__=="__main__":
	main() #sys.argv[1:])
	
