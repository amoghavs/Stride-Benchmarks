#! /usr/bin/python

####
#
#


import sys,subprocess,re,math,commands,time
 			
def main():
	Max={}
	Min={}
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=3
	Min['Dims']=1
	Max['NumStream']=4
	Min['NumStream']=1
	Max['Stride']=3 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=['d']	
	Init='index0'
	DS='i'
	SpatWindow=[8,16,32];
	LoopIterationBase=10;
	LoopIterations=[10]#,20] #,5,6];
	MbyteSize=26 # 2^28=256M = 2^20[1M] * 2^8 [256] ; # Int= 256M * 4B = 1GB. # Double= 256M * 8B= 2GB 
	MaxSize=2**MbyteSize
	Dim0Size=2**(MbyteSize-8)
	HigherDimSize= MaxSize/	Dim0Size

	ScriptUniqueID=''
	if(len(Alloc)==1):
		if( Alloc[0]=='d'):
			ScriptUniqueID='Dynamic'
		elif(Alloc[0]=='s'):
			ScriptUniqueID='Static'
		else:
			print "\n\t Data Alloc is neither dynamic or static \n"
			sys.exit()
		
		if(DS=='i' or DS=='int'):
			ScriptUniqueID='Int_'+ScriptUniqueID
		elif(DS=='f' or DS=='float'):
			ScriptUniqueID='Float_'+ScriptUniqueID		
		elif(DS=='d' or DS=='double'):
			ScriptUniqueID='Double_'+ScriptUniqueID		
	
	else:
		print "\n\t The script is designed only for including name of one allocation type and alloc has "+str(len(Alloc))+" alloc requests. You are doomed!! \n"
		sys.exit()
	
				
	MasterSWStatsPrefix='MasterSWStats_'+ScriptUniqueID+'_Stride'+str(Min['Stride'])+'to'+str(Max['Stride'])
	MasterSWStatsSuffix='_Size2power'+str(MbyteSize)+'_dim'+str(Min['Dims'])+'to'+str(Max['Dims'])+'_Stride'+str(Min['Stride'])+'to'+str(Max['Stride'])+'_Streams'+str(Min['NumStream'])+'to'+str(Max['NumStream'])+'_Iterations'+str(LoopIterations[0])+'to'+str(LoopIterations[len(LoopIterations)-1])
	FolderName='SRC_'+ScriptUniqueID+MasterSWStatsSuffix
	MasterSWStatsFile=MasterSWStatsPrefix+MasterSWStatsSuffix+'.txt'
	MasterSWStats=open(MasterSWStatsFile,'w')
	
	for NumVars in range(Min['Vars'],Max['Vars']+1):
	 # CAUTION: The main loop iterates for 'NumVars' and the config generator should be changed to accommodate #Vars > 1 and not loop over like this! 
 		for CurrLoopIterations in LoopIterations:
			NumLoopIterations= CurrLoopIterations
		  	print "\n\t NumLoopIterations: "+str(NumLoopIterations)
			MasterSWStats.write("\n\n\t ################################ \n\n");
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
 
 					CurrString=''
					RestrictLength=3
					print "\n --- NumStreams: "+str(NumStreams)
					if(NumStreams>=RestrictLength):
						for i in range(NumStreams-RestrictLength):
							CurrString+=str(1)+','
						CurrString+=str(1)
					print "\n\t PrevString: "+str(CurrString)
					ResultString=[]
					PrefixString=CurrString
					for HigherIndex in range(Min['Stride'],Max['Stride']+1): #range(Min['NumStream'],Max['NumStream']+1):
						print "\n\t CurrString: "+str(CurrString)
						
						if(NumStreams<RestrictLength-1):
							CurrString=str(2**(HigherIndex))
							ResultString.append(CurrString)
							print "\n\t REsult: "+str(CurrString)
						
						else:
						   	if(PrefixString!=''):
						   		CurrString=PrefixString+','+str(2**(HigherIndex))
						   	else:
						   		CurrString=PrefixString+str(2**(HigherIndex))
						   	print "\n\t End: CurrString "+str(CurrString)							
							for LowerIndex in range(Min['Stride'],Max['Stride']+1): #range(Min['NumStream'],Max['NumStream']+1):
						   	        if(CurrString!=''):
							   		temp=CurrString+','+str(2**(LowerIndex))
							   	else:
							   		temp=str(2**(LowerIndex))
						   		ResultString.append(temp)
						   		print "\n\t\t Result: "+str(temp)
 		
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
							UniqueID='Iters'+str(NumLoopIterations)+'_'+str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_stride_'+str(StrideName)
							SRCID='Iters'+str(NumLoopIterations)+'_'+str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_stride_'+str(StrideName)
							Config="Config_"+UniqueID
							ConfigFile=str(Config)+'.txt'

							"""f=open(ConfigFile,'w')
							f.write("\n#vars "+str(NumVars))
							f.write("\n#dims "+str(NumDims))
							f.write("\n"+str(NumStreamString))
							f.write("\n#loop_iterations "+str(NumLoopIterations))
							f.write("\n"+str(StrideString))
							#f.write("\n#stride "+str(Stride))
							f.write("\n#size "+str(SizeString))
							f.write("\n#allocation "+str(CurrAlloc) )
							f.write("\n#init "+str(Init))
							f.write("\n#datastructure "+str(DS))
							f.close()
	 
	 						#CMDConfigDir='mkdir '+str(Config)
							#commands.getoutput(CMDConfigDir)						
						
							CMDrunStrideBenchmarks='python StrideBenchmarks.py -c '+str(ConfigFile)
							commands.getoutput(CMDrunStrideBenchmarks)
							SRCCode='StrideBenchmarks_'+str(SRCID)+'.c'
							EXE='StrideBenchmarks_'+str(SRCID)
							print "\n\t Config file: "+str(ConfigFile)#+" source: "+str(SRCCode)+" exe "+str(EXE)						
							CMDCompileSRC='gcc -O3 -g '+str(SRCCode)+' -o '+str(EXE)
							commands.getoutput(CMDCompileSRC)	"""				


							SRCCode='StrideBenchmarks_'+str(SRCID)+'.c'
							EXE='StrideBenchmarks_'+str(SRCID)
							print "\n\t Config file: "+str(ConfigFile)#+" source: "+str(SRCCode)+" exe "+str(EXE)		
							stdout='Stdout_'+SRCID
							CMDRunExe='./'+str(EXE)+' > '+str(stdout) 
							#print "\n\t Exe: "+str(CMDRunExe)
							commands.getoutput(CMDRunExe)
							CMDgrep='grep Run\-time '+str(stdout)
							TimingCapture=commands.getoutput(CMDgrep)
							RunTime=re.match('\s*.*Func.*\:\s*(\d+)+.(\d+)+\s*$',TimingCapture)
							if RunTime:
								print "\n\t RunTime: "+str(RunTime.group(1))+'.'+str(RunTime.group(2))
								MasterSWStats.write("\n\t Config: "+str(ConfigFile))
								SaveThisTime=str(RunTime.group(1))+'.'+str(RunTime.group(2))
								MasterSWStats.write("\t Runtime: "+str(SaveThisTime))
							else:
								print "\n\t TimingCapture: "+str(TimingCapture)+' has failed! '
								MasterSWStats.close()
								
								CMDcreateFolder='mkdir '+str(FolderName)
							        commands.getoutput(CMDcreateFolder)
							        print "\n\t Mkdir: "+str(CMDcreateFolder)
							        CMDmvFiles='mv Config_*vars* StrideBenchmarks*vars* Stdout_* '+str(FolderName)
							        print "\n\t Mvfiles: "+str(CMDmvFiles)
							        commands.getoutput(CMDmvFiles)
								sys.exit(0)	
						
	CMDcreateFolder='mkdir '+str(FolderName)
	commands.getoutput(CMDcreateFolder)
	print "\n\t Mkdir: "+str(CMDcreateFolder)
	CMDmvFiles='mv Config_*vars* StrideBenchmarks*vars* Stdout_* '+str(FolderName)
	print "\n\t Mvfiles: "+str(CMDmvFiles)
	commands.getoutput(CMDmvFiles)




if __name__=="__main__":
	main() #sys.argv[1:])
	
