# Simulation of openFIRE 
# Simon.DENEL.fr - 2013
# Initializing the memory.txt file used by the verilog testbench to create a simulated memory
# launch it with: python3 memory_init.py && cat memory.txt
import sys

def Itobin(i, l):
	o = bin(i)[2:]
	return '0'*(l-len(o))+o
def str2hex(S):
	out = ''
	for i in range(0, len(S)):
		out+=hex(ord(S[i]))[2:]
	return out+'\n'

opcodes = {
	'ADD'	: '000000', # Add		ADD Rd,Ra,Rb			Rd := Rb + Ra
	'MUL'	: '010000', # MUL		MUL Rd,Ra,Rb 			Rd := Ra * Rb
	'ADDI'	: '001000', # ADDI immediate	ADDI Rd,Ra,Imm			Rd := s(Imm) + Ra
	'BSLLI'	: '011001', # SHIFT		BSLLI Rd,Ra,00000100000&Imm	Rd := (Ra << Imm5) & 0

	'LW'	: '110010', # Load		LW Rd,Ra,Rb 		Addr := Ra + Rb		Rd := *Addr
	'SW'	: '110110', # Save		SW Rd,Ra,Rb 		Addr := Ra + Rb		*Addr := Rd
	#'LBU'	: '110000' # Load 8		LBU Rd,Ra,Rb 		Addr := Ra + Rb		Rd[0:23] := 0		Rd[24:31] := *Addr[0:7]
	#'LHU'	: '110001' # Load 16		LHU Rd,Ra,Rb 		Addr := Ra + Rb		Rd[0:15] := 0		Rd[16:31] := *Addr[0:15]
}

# Creating registers from 0 to 31
registers = {}
for i in range(0, 32):
	tobin=bin(i)[2:]
	tobin='0'*(5-len(tobin))+tobin
	registers['R'+str(i)]=tobin
'''
Do not forget that:
- R0 is equal to 0
'''
'''
- Chargement dans R1 de A=5  stocké à l'adresse 0x1
- Chargement dans R1 de B=10 stocké à l'adresse 0x2
- R0 <- R0 + R1
- Sauvegarde de R0 en mémoire principale
'''

datas = {
	#ADDI R1,R0, <- Add(A)
	0 : ['ADDI R1,R0,1024',		"R1 <- Add(A)=0x100"],
	1 : ['LW R2,R0,R1',		"Chargement dans R2 de A=5 stocké à l'adresse 0x100"],
	2 : ['ADDI R1,R1,4',		"R1 <- Add(B)=Add(A)+4bytes"],
	3 : ['LW R3,R0,R1',		"Chargement dans R2 de A=5 stocké à l'adresse 0x100"],
	4 : ['ADD R2,R2,R3',		"R2<-5+1=6"],
	5 : ['MUL R4,R2,R2',		"R2<-R2*R2"],
	6 : ['SW R4,R0,R1',		"Sauvegarde de R2 à l'adresse 0x100"],
	
	256 : 5,
	257 : 1,
}

memory_txt=''
memory_txt_comments=''
keyMax=max(datas.keys(), key=int)+1
for i in range(0, keyMax):
	if datas.get(i):
		if isinstance(datas.get(i), list):
			print(datas[i][0])
print('\n')
for i in range(0, keyMax):
	if datas.get(i):
		if isinstance(datas.get(i), list):
			print(datas[i][1])
print('\n')
			
for i in range(0, keyMax):
	if datas.get(i):
		sys.stdout.write(str(i)+' '*(len(str(keyMax))-len(str(i)))+' : '),
		if isinstance(datas.get(i), list):
			ins=datas[i][0]

			insT=ins
			ins2bin=''
			j=0
			k=0
			while j<=len(insT):
				if j==len(insT)-1 or (len(insT) > 1 and insT[j+1] in [' ',',']):
					if k==0:
						ins2bin+=opcodes[insT[:j+1]]
					elif insT[0]=='R':
						ins2bin+=registers[insT[:j+1]]
					else: # decimal number
						ins2bin+=Itobin(int(insT[:j+1]), 32-len(ins2bin))
					insT=insT[(j+2):]
					
					j=0
					k+=1
				else:
					j+=1
			print('- - - ')
			ins2bin+='0'*(32-len(ins2bin))
			ins2hex=str(hex(int(ins2bin, 2)))[2:]
			ins2hex='0'*(8-len(ins2hex))+ins2hex
			print(ins+' '*(32-len(ins))+'-> '+ins2bin+' -> '+ins2hex+' // '+datas[i][1])
			
			memory_txt+=ins2hex+'\n'
			memory_txt_comments+=str2hex(datas[i][0])
		else:
			tohex=hex(datas.get(i))[2:]
			tohex='0'*(8-len(tohex))+tohex
			memory_txt+=tohex+'\n'
			print(str(datas.get(i))+' -> 0x'+tohex)
	else:
		memory_txt+='0'*8+'\n'
f = open('memory.txt', 'w')	
f.write(memory_txt)
f.close()
f = open('memory_comments.txt', 'w')	
f.write(memory_txt_comments)
f.close()
