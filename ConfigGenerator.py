#! /usr/bin/python

####
#
#


import sys,subprocess,re,math,commands,time

 
def RecursiveStrideGen(CurrStream,NumStreams,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString):
	if(CurrStream==NumStreams):
		#print "\n\t ++ CurrStream: "+str(CurrStream)
		if(CurrString):
			for i in range(NumStrides):
				Result=CurrString+','+str((2**i))
				ResultString.append(Result)
				print "\n\t Result: "+Result
		else:
			for i in range(NumStrides):
				Result=CurrString+str((2**i))
				ResultString.append(Result)
				print "\n\t Result: "+Result		
			
		CurrStream-=1
		return #(CurrStream,CurrPrefixPos)

 	CurrPrefixPos=0	
	while(CurrPrefixPos!=NumStrides):
		if(CurrPrefix==''):	
			CurrString=CurrPrefix+str((2**CurrPrefixPos))	
		else:
			CurrString=CurrPrefix+','+str((2**CurrPrefixPos))
		#print "\n\t -- CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)		
		#print "\n\t $$ CurrStream: "+str(CurrStream)+" CurrPrefixPos: "+str(CurrPrefixPos)
		RecursiveStrideGen(CurrStream+1,NumStreams,NumStrides,CurrString,CurrString,CurrPrefixPos,ResultString)
		CurrPrefixPos+=1
		#print "\n\t %% CurrStream: "+str(CurrStream)+" CurrPrefixPos: "+str(CurrPrefixPos)		
		#return CurrStream
		
	CurrStream-=1
	#print "\n\t ^^ CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)	
	return (CurrStream,CurrPrefixPos)	
			
			
def main():
	Max={}
	Min={}
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=2
	Min['Dims']=2
	Max['NumStream']=1
	Min['NumStream']=1
	Max['Stride']=1 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['d']	
	Init='index0*10+index0'
	DS='i'
	SpatWindow=[8,16,32];
	MbyteSize=20 # 2^28=32Mbyte= 2^20[1M] * 2^5 [32] * 2^3[byte]
	MaxSize=2**MbyteSize
	Dim0Size=2**(MbyteSize-8)
	HigherDimSize= MaxSize/	Dim0Size
	
	MasterSWStats=open("MasterSWStats.txt",'w')
	for NumVars in range(Min['Vars'],Max['Vars']+1):
	 # CAUTION: The main loop iterates for 'NumVars' and the config generator should be changed to accommodate #Vars > 1 and not loop over like this! 
	 
	 	"""
	 	#ArrayStrideString=[]
	 	#ResultString=[]
	 	#This=[]
	 	#RecursiveStrideGen(1,4,4,'','',0,This)
	 	#ResultString.append(This)
	 	#print "\n\t Result String length: "+str(len(ResultString[0]))
	 	#sys.exit(0)
		
		"""	
		
	
 
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

		
			for NumStreams in range(Min['NumStream'],Max['NumStream']+1):
		
				CurrStream=1
				NumStrides=((Max['Stride']-Min['Stride'])+1)	
				CurrString=''
				CurrPrefix=''
				CurrPrefixPos=0
				ResultString=[]
				RecursiveStrideGen(CurrStream,NumStreams,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString)
		
				NumStreamString='#StreamDims '+str(NumStreams) # CAUTION: Should change this when NumVars > 1
				StrideString=''
				StrideName=''
				print "\n\t This is the length of ResultString: "+str(len(ResultString))
				for CurrStreamCombi in ResultString:
					StrideString='#stride0 '+str(CurrStreamCombi)
					Strides=re.split(',',CurrStreamCombi)
					StrideName=''
					MaxStride=0
					if Strides:
						for i in range(len(Strides)-1):
							StrideName+=str(Strides[i])+'_'
							if(MaxStride<int(Strides[i])):
								MaxStride=int(Strides[i]) # CAUTION: Should change this when NumVars > 1
							else:
								print "\n\t We think strides[i]: "+str(Strides[i])+" is lesser than Maxstrides: "+str(MaxStride)
						StrideName+=str(Strides[len(Strides)-1])
						if(MaxStride<int(Strides[len(Strides)-1])):
							MaxStride=int(Strides[len(Strides)-1]) # CAUTION: Should change this when NumVars > 1
						else:
							print"\n\t -- Stride: "+str(Strides[len(Strides)-1])+" MaxStride: "+str(MaxStride)
						
						#StrideName+=str(MaxStride) # CAUTION: Should change this when NumVars > 1
						print "\n\t Stride-Name: "+str(StrideName)+' StrideString '+str(StrideString)+" and Maxstride: "+str(MaxStride)
					else:
						print "\n\t CurrStreamCombi: "+str(StrideName)+" seems to be corrupted, exitting! "
						sys.exit()
						
							
					for CurrAlloc in Alloc:
						UniqueID=str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_stride_'+str(StrideName)
						SRCID=str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_maxstride_'+str(MaxStride)
						Config="Config_"+UniqueID
						ConfigFile=str(Config)+'.txt'

						f=open(ConfigFile,'w')
						f.write("\n#vars "+str(NumVars))
						f.write("\n#dims "+str(NumDims))
						f.write("\n"+str(NumStreamString))
						f.write("\n"+str(StrideString))
						#f.write("\n#stride "+str(Stride))
						f.write("\n#size "+str(SizeString))
						f.write("\n#allocation "+str(CurrAlloc) )
						f.write("\n#init "+str(Init))
						f.write("\n#datastructure "+str(DS))
						f.close()

						
						CMDConfigDir='mkdir '+str(Config)
						commands.getoutput(CMDConfigDir)						
						
						CMDrunStrideBenchmarks='python StrideBenchmarks.py -c '+str(ConfigFile)
						commands.getoutput(CMDrunStrideBenchmarks)
						SRCCode='StrideBenchmarks_'+str(SRCID)+'.c'
						EXE='StrideBenchmarks_'+str(SRCID)
						print "\n\t Config file: "+str(ConfigFile)#+" source: "+str(SRCCode)+" exe "+str(EXE)						
						CMDCompileSRC='gcc -O3 -g '+str(SRCCode)+' -o '+str(EXE)
						commands.getoutput(CMDCompileSRC)
						CMDPebilCompile='pebil --typ jbb --app '+str(EXE)
						commands.getoutput(CMDPebilCompile)
						CMDRunJbb='./'+str(EXE)+'.jbbinst'
						commands.getoutput(CMDRunJbb)
						FuncName='FuncVar0Stride'+str(MaxStride)+'Dim'+str(NumDims-1)  # CAUTION: This should be changed if >1 variable is going to be used.
						#print "\n\t Assuming that the function is: "+str(FuncName)
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
									#print "\n\t Look Whos here: "+str(GetBBID[2]) #[2])+"!! "
									FuncBlkstoSimulate.append(str(GetBBID[2]))
							
						BBFile=open('BBlist.txt','w')
						#BBFile.write(str(FuncBlkstoSimulate[2]))
						#BBFile.write(str(FuncBlkstoSimulate[3]))
						for BB in range(0,len(FuncBlkstoSimulate)):
							BBFile.write('\n\t'+str(FuncBlkstoSimulate[BB]))
					
						BBFile.write("\n")
						BBFile.close()
						if( len(FuncBlkstoSimulate) ):
							print "\n\t Have found few BBs of the function: "+str(FuncName)
						else:
							print "\n\t Did not find any BBs of the function: "+str(FuncName)					
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

							CMDExportSW='sh export METASIM_SPATIAL_WINDOW='+str(CurrSW)#+' | export METASIM_SAMPLE_ON=1 | export METASIM_SAMPLE_OFF=0 '
																
							SimInst=str(EXE)+'.siminst'
							CMDRunSiminst='./'+str(SimInst)+' > stdout.txt'
							EnvFile=open("source_env.sh",'w')
							
							#EnvFile.write("\n\t #! /bin/bash")
							EnvFile.write('\nexport METASIM_SPATIAL_WINDOW='+str(CurrSW))
							#EnvFile.write('\necho $METASIM_SPATIAL_WINDOW')
							EnvFile.write('\n\texport METASIM_SAMPLE_ON=1')
							EnvFile.write('\n\texport METASIM_SAMPLE_OFF=0')
							EnvFile.write('\n'+str(CMDRunSiminst))
							EnvFile.write('\n')
							EnvFile.close()

							subprocess.call(['bash', 'source_env.sh']) #,shell=True)
							Check=commands.getoutput('echo $METASIM_SPATIAL_WINDOW')
	
							SWFile='SW_'+str(CurrSW)+'_'+str(Config)+'.log'
							CMDRenameSpatial='mv *.spatial '+str(SWFile)
							commands.getoutput(CMDRenameSpatial)
							CMDgrep='grep Total '+str(SWFile)
							GrepOutput=commands.getoutput(CMDgrep)

							Access=re.match(r'\s*.*\:\s*(\d+)+$',GrepOutput)
							if Access:
								TotalAccess=int(Access.group(1))
								#print "\n\t Total Accesses as found out: "+str(TotalAccess)+" and grep output: "+str(GrepOutput)	
							else:
								print "\n\t Total Accesses not found!! \n"
								sys.exit()
						
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
						
							SWStats.write("\n\n")		
							MasterSWStats.write("\n\n")
						SWStats.close()
						CMDMvAll='mv *.c SW* *siminst* *jbbinst* BBlist.txt stdout.txt '+str(ConfigFile)+' '+str(EXE)+' '+str(Config)
						commands.getoutput(CMDMvAll)
						CMDRmMetaFiles='rm -f *Instructions* LRU* JBBInfo.txt source_env.sh '
						commands.getoutput(CMDRmMetaFiles)
						#CMD
		MasterSWStats.close()
						
					
			
	




if __name__=="__main__":
	main() #sys.argv[1:])
	
