# Mode Flags

# CR0[0] (Protected Mode) "PE"
# EFER[8] (Long Mode Enable) "LME"
# EFER[10] (Long Mode Active) "LMA"
# EFLAGS[17] (Virtual Mode) "VM"

# Protections

# CR4[20] "SMEP"
# CR4[21] "SMAP"

# Insn Flags

# EFLAGS[21] (CPUID enable) "CPUIDXE"
# CR4[2] (RDTSC -> CPL==0) "TSD"
# CR4[11] (SGDT, SIDT, SLDT, SMSW and STR -> CPL==0) "UMIP"
# CR4[13] (VM* enable) "VMXE"

#s = "EFL[1]==0\nEFL[2]==0\nEFL[4]==0\nEFL[6]==0\n"
#"CPL==0"# + '\n' + "PE==0" + '\n' + "LME==0" + '\n' + "LMA==0" + '\n' + "VM==0" + '\n' + "CPUIDXE==0" + '\n' + "TSD==0" + '\n' + "UMIP==0" + '\n' + "VMXE==0" + '\n'

a = ""

def gen_s():
	s = ""
	elfs = [1]#[1,2,4,6,8,9,11,13]
	cr0s = []#[0,1,2,3,5,7,18,20]
	cr4s = []#[6,8,9,11,12]
	#regs = ["SMM", "CPL"] - get these back in
	for [reg,inds] in [["EFL",elfs],["CR0",cr0s],["CR4",cr4s]]:
		for ind in inds:
			s = s + reg + "_" + str(ind) + "==0\nD_" + reg + "_" + str(ind) + "==0\n"
	return s

def parse(names, n):
	s = gen_s();
	uniq_insts = set()
	for name in names:
		for line in open(name + ".txt", "r"):
			if line[0] == "0" and line[1] == "x" and len(line) > 39:
				#print(line)
				uniq_insts.add(line[38:].replace("rep ","").split()[0])
			if "Servicing hardware INT=" in line: # interrupt start case
				uniq_insts.add(line.replace("Servicing hardware INT=", "").rstrip())
				uniq_insts.add("new" + line.replace("Servicing hardware INT=", "").rstrip())
				#print(line)
	#print(uniq_insts)
	#special cases
	for spec in ["calll","jmp","ret"]:
		if spec in uniq_insts:
			uniq_insts.remove(spec)
			uniq_insts.add(spec + "_near")
			uniq_insts.add(spec + "_far")
	out = open(n + ".spinfo", "w")
	#out.write("input-language C/C++\ndecl-version 2.0\nvar-comparability implicit\n\n") # header
	#exit()
	for i in list(uniq_insts):
		#print(i)
		out.write("\n\nPPT_NAME .."+ i + '\n' + s)
		
	return
		
	
#parse(["cs", "cs2", "boot", "deb", "fl1", "fl2", "odin", "sol", "sel4"], "in_trace")
