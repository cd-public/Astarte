# mode

from time import sleep
from copy import deepcopy
from os import system

# my code
import uniq_insts,split,in_one


def add_to_cache(save_name, cache, line):
	to_add = []
	vars = ['INST', 'ARG1', 'ARG2', 'ADDR', 'EAX', 'EBX', 'ECX', 'EDX', 'EIP', 'EFL', 'CPL', 'II', 'A20', 'SMM', 'HLT', 'ES', 'CS', 'SS', 'DS', 'FS', 'GS', 'LDT', 'TR', 'ES_DPL', 'CS_DPL', 'SS_DPL', 'DS_DPL', 'FS_DPL', 'GS_DPL', 'LDT_DPL', 'TR_DPL', 'GDT', 'IDT', 'CR0', 'CR2', 'CR3', 'CR4', 'DR0', 'DR1', 'DR2', 'DR3', 'DR6', 'DR7', 'CCS', 'CCD', 'CC0', 'EFER', "IOPL", "VM", "CPUIDXE", "PE", "TSD", "UMIP", "VMXE", "SMEP", "SMAP", "LME", "LMA", "EFL_0", "EFL_1", "EFL_2", "EFL_3", "EFL_4", "EFL_5", "EFL_6", "EFL_7", "EFL_8", "EFL_9", "EFL_10", "EFL_11", "EFL_12", "EFL_13", "EFL_14", "EFL_15", "EFL_16", "EFL_17", "EFL_18", "EFL_19", "EFL_20", "EFL_21", "CR0_0", "CR0_1", "CR0_2", "CR0_3", "CR0_4", "CR0_5", "CR0_6", "CR0_7", "CR0_8", "CR0_9", "CR0_10", "CR0_11", "CR0_12", "CR0_13", "CR0_14", "CR0_15", "CR0_16", "CR0_17", "CR0_18", "CR0_19", "CR0_20", "CR0_21", "CR0_22", "CR0_23", "CR0_24", "CR0_25", "CR0_26", "CR0_27", "CR0_28", "CR0_29", "CR0_30", "CR4_0", "CR4_1", "CR4_2", "CR4_3", "CR4_4", "CR4_5", "CR4_6", "CR4_7", "CR4_8", "CR4_9", "CR4_10", "CR4_11", "CR4_12", "CR4_13", "CR4_14", "CR4_15", "CR4_16", "CR4_17", "CR4_18", "CR4_19", "CR4_20", "CR4_21", "CR4_22", "EFER_0", "EFER_1", "EFER_2", "EFER_3", "EFER_4", "EFER_5", "EFER_6", "EFER_7", "EFER_8", "EFER_9", "EFER_10", "EFER_11", "EFER_12", "EFER_13", "EFER_14", "EFER_15", "EFL_0_1", "EFL_2_3", "EFL_4_5", "EFL_6_7", "EFL_8_9", "EFL_10_11", "EFL_12_13", "EFL_14_15", "EFL_16_17", "EFL_18_19", "EFL_20_21", "CR0_0_1", "CR0_2_3", "CR0_4_5", "CR0_6_7", "CR0_8_9", "CR0_10_11", "CR0_12_13", "CR0_14_15", "CR0_16_17", "CR0_18_19", "CR0_20_21", "CR0_22_23", "CR0_24_25", "CR0_26_27", "CR0_28_29", "CR4_0_1", "CR4_2_3", "CR4_4_5", "CR4_6_7", "CR4_8_9", "CR4_10_11", "CR4_12_13", "CR4_14_15", "CR4_16_17", "CR4_18_19", "CR4_20_21", "EFER_0_1", "EFER_2_3", "EFER_4_5", "EFER_6_7", "EFER_8_9", "EFER_10_11", "EFER_12_13", "EFER_14_15"]
	#[[9,17,"VM"],[9,21,"CPUIDXE"],[33,0,"PE"],[36,2,"TSD"],[36,11,"UMIP"],[36,13,"VMXE"],[36,20,"SMEP"],[36,21,"SMAP"],[46,8,"LME"],[46,10,"LMA"]]
	#print(cache)
	#print(line)
	added = False
	if ("0x" in save_name and ("ARG" in line or "ADDR" in line)) or "ADDR == -1" in line: # catch some errors introduced by the frontend
		return cache
	if "*" in line:
		return cache
	if "ENTER" in save_name:
		for var in vars:
			line.replace(var,"orig(" + var + ")")
	for cond in cache:
		if save_name.replace("EXIT","ENTER") in cond[0].replace("EXIT","ENTER"):
			to_add = cond
	if " == " in line and line[0].isalpha(): # create sets of equal values
		#print(line)
		regs = set(line.rstrip().split(" == "))
		for eqs in to_add[1][0]:
			#print(eqs)
			for reg in regs:
				if reg in eqs:
					for reg in regs:
						eqs.add(reg)
					added = True
					return cache
		if not added:
			to_add[1][0].append(regs)
			added = True
			return cache
	elif " <==> " in line and not added: # create sets of equivalent conditions
		reg_l = line.rstrip().split(" <==> ")
		regs = set([r.strip() for r in reg_l])
		for eqs in to_add[1][1]:
			for reg in regs:
				if reg in eqs:
					for reg in regs:
						eqs.add(reg)
					added = True
					return cache
		if not added:
			to_add[1][1].append(regs)
			added = True
			return cache
	elif " ==> " in line and not added: # create sets of implication conditions
		splits = line.split(" ==> ")
		if to_add[1][3] == []:
			to_add[1][3] = [[splits[0].strip(),{splits[1].strip()}]]
			added = True
			return cache
		else:
			for reg in to_add[1][3]:
				if reg[0] in splits[0]:
					# found the register in the implication struct
					reg[1].add(splits[1].strip())
					added = True
					return cache
	elif line[0].isalpha() and not added and "one of" not in line: # inequality case
		# want a structure [[<reg1>,[[oper1,[<equivreg1>,<equivreg2>]][oper2,[<equivreg3>,<equivreg4>]]]],[<reg2>,[[oper3,[<equivreg5>,<equivreg6>]]]]]
		splits = line.split()
		if to_add[1][2] == []:
			to_add[1][2] = [[splits[0],[[splits[1],{splits[2]}]]]]
			added = True
			return cache
		else:
			for reg in to_add[1][2]:
				if reg[0] in splits[0]:
					# found the register in the inequality struct, now look for operator
					for oper in reg[1]:
						if splits[1] in oper[0]:
							oper[1].add(splits[2])
							added = True
							return cache
					if not added: # add new operator
						reg[1].append([splits[1],{splits[2]}])
						added = True
						return cache
			if not added: # add new reg
				to_add[1][2].append([splits[0],[[splits[1],{splits[2]}]]])
				added = True
				return cache
	elif added:
		to_add[2] = to_add[2] + line
		return cache
	return cache
	
def sorted(s):
	# set to string
	l = list(s)
	l.sort()
	return str(l)
	
def eqset(s):
	# create a string denoting a set
	l = list(s)
	l.sort()
	return "eqset: " + str(l[0])
	
def sets_combine(sets):
	# return sets
	# given list of sets of items in symmetric relations, combine sets with common elements.
	max = len(sets)
	i = 0;
	j = 0;
	while i < max:
		j = i + 1
		to_add = set()
		to_remove = set()
		while j < max:
			for e in sets[i]:
				if e in sets[j]:
					to_add = to_add.union(sets[j])
					to_remove.add(j)
			j = j + 1
		#print(to_add)
		if len(to_add) != 0:
			#print(to_add)
			sets[i].union(to_add)
			to_remove_l = list(to_remove)
			to_remove_l.sort()
			while len(to_remove_l) > 0:
				sets.remove(sets[to_remove_l.pop(-1)])
			max = len(sets)
		i = i + 1
	for s in sets:
		if "-1" in s: 
			sets.remove(s) # remove dummy values
	#print(sets)
	return sets
	
def expand_ineq(cache):
	to_del = []
	for entry in cache:
		if "EXIT" in entry[0]:
			to_del.append(entry)
		else:
			#prepare the eqs (necessarily)
			entry[1][0] = sets_combine(entry[1][0])
			eqs = entry[1][0]
			#do the LHS combine here
			# do name change
			#print("LHS: " + str(entry[0]))
			for ineqs in entry[1][2]: # looking at a LHS register
				for eq in eqs:
					if ineqs[0] in eq:
						ineqs[0] = eqset(eq)
			# with name change, walk the list and combine opers
			entry[1][2].sort() # just a convenience
			for ineq in entry[1][2]:
				ineq[1].sort()
			max = len(entry[1][2])
			i = 0;
			j = 0;
			while i < max - 1:
				#print("outer, {i,j,max} == " + str([i,j,max])) # iter check - perserved in case
				j = i + 1
				while j < max:
					if entry[1][2][i][0] == entry[1][2][j][0]:
						# here we must combine operation-wise
						for oper in entry[1][2][j][1]:
							#print(oper[0])
							if oper[0] not in [o[0] for o in entry[1][2][i][1]]: # new operation so adding the entire oper
								entry[1][2][i][1].append(oper)
							else:
								for oper_i in entry[1][2][i][1]: # finding the same operation
									if oper_i[0] in oper[0]:
										oper_i[1].union(oper[1]) # combining!
						entry[1][2].remove(entry[1][2][j]) # removing the redundant list
						max = max - 1 # iterator math - there's one few list now
						# dont have to update j since j now points to a new list! 
					else:
						j = max
						i = i + 1
			#print("RHS: " + str(entry[0]))
			#do the RHS combine here
			for ineqs in entry[1][2]: # looking at a LHS register
				for oper in ineqs[1]: # looking at LHS register and an operation
					to_remove = set()
					to_add = set()
					for reg in oper[1]: # looking at a RHS register
						for eq in eqs: # looking at sets of equal registers
							if reg in eq:
								# case LHS == RHS
								if ineqs[0] not in eq:
									to_add.add(eqset(eq))
								to_remove.add(reg)
					for ele in to_remove:
						oper[1].remove(ele)
					oper[1] = oper[1].union(to_add)
					# clobber self-equality
					if len(oper[1]) == 1:
						if ineqs[0] in oper[1]:
							ineqs[1].remove(oper)
				# clobber value-comparison LHS
				if "eqset" in ineqs[0]:
					if not ineqs[0].split()[1][0].isupper():
						for oper in ineqs[1]:
							to_remove = set()
							for rhs in oper[1]:
								if "eqset" in rhs:
									if not rhs.split()[1][0].isupper():
										to_remove.add(rhs)
								if rhs.isdigit():
									to_remove.add(rhs)
							for ele in to_remove:
								oper[1].remove(ele)			
				# clobber int / nat conversion properties LHS
				if "eqset: \"0000000000000000000000000000\"" in ineqs[0] or "eqset: 0" in ineqs[0]:
					to_remove = []
					for oper in ineqs[1]:
						if "<=" in oper[0]:
							to_remove.append(oper)
					for ele in to_remove:
						ineqs[1].remove(ele)
				# "" RHS
				for oper in ineqs[1]:
					if ">=" in oper[0]:
						for key in ["eqset: \"0000000000000000000000000000\"", "eqset: 0", "-1"]:
							if key in oper[1]:
								oper[1].remove(key)
			#do the LHS combine here:	
	for ele in to_del:
		cache.remove(ele)
	return cache
	
def print_globals(struct,outf):
	# three groups:
	pre = ["~","","not"]
	[condition, extracted] = struct
	for i in range(1,3):
		group = extracted[i]
		outf.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nGLOBAL:  " + pre[i] + condition + "\n~~ begin equality sets ~~\n")
		#print(group[0])
		for eqs in group[0]:
			outf.write(sorted(eqs) + "\n")
		outf.write("~~ end equality sets ~~\n~~ begin equivalence sets ~~\n")
		for eqs in group[1]:
			outf.write(sorted(eqs) + "\n")
		outf.write("~~ end equivalence sets ~~\n~~ begin inequality properties ~~\n")
		#print(group[2])
		for ineqs in group[2]:
			if ineqs != []:
				if len(ineqs[2]) != 0:
						outf.write(ineqs[0] + " " + ineqs[1] + " _x_ for all _x_ in  " + sorted(ineqs[2]) + "\n")
		outf.write("~~ end inequality properties ~~\n~~ begin implication properties ~~\n")
		for imps in group[3]:
			outf.write(imps[0] + " ==>  _x_ for all _x_ in  " + sorted(imps[1]) + "\n")
		outf.write("~~ end implication properties ~~\n")
	
def extract_globals(cache_orig, condition):
	cache = cache_orig
	#cache = deepcopy(cache_orig) # get a local copy, now doing it on smaller scale
	# disregarding instructions, we splits properties into 3 groups
	# (1) condition neutral (2) condition (3) not condition
	groups = [[],[],[]]
	for entry in cache:
		if "not" in entry[0] and condition in entry[0]: # contains relevant condition
			groups[2].append(entry[1])
		elif condition in entry[0]:
			groups[1].append(entry[1])
		else:
			groups[0].append(entry[1])
	out = []
	for group in groups:
		# combine equalities
		group_eqs = []
		for entry in group:
			if group_eqs == []:
				group_eqs = deepcopy(entry[0])
			else:
				keep = set()
				for iter_eq in entry[0]:
					for group_eq in group_eqs:
						for ele in iter_eq:
							if ele in group_eq:
								group_eq.intersection(iter_eq)
								if len(group_eq) != 0:
									keep.add(group_eqs.index(group_eq))
				l = list(keep)
				l.sort()
				l.reverse()
				for i in l:
					del group_eqs[i]
						
		# combine equivalences
		group_equivs = []
		for entry in group:
			if group_equivs == []:
				group_equivs = deepcopy(entry[1])
			else:
				keep = set()
				for iter_equiv in entry[1]:
					for group_equiv in group_equivs:
						for ele in iter_equiv:
							if ele in group_equiv:
								group_equiv.intersection(iter_equiv)
								if len(group_equiv) != 0:
									keep.add(group_equivs.index(group_equiv))
				l = list(keep)
				l.sort()
				l.reverse()
				for i in l:
					del group_equivs[i]
		# combine inequalities
		group_ineqs = []
		for entry in group:
			if group_ineqs == []:
				# dont use ineq struct TODO
				safety = deepcopy(entry[2])
				for lhs in safety:
					for oper in lhs[1]:
						group_ineqs.append([lhs[0], oper[0], oper[1]])
			else:
				keep = set()
				for ineq in group_ineqs:
					for lhs in entry[2]:
						if lhs[0] in ineq[0]:
							for oper in lhs[1]:
								if oper[0] in ineq[1]:
									ineq[2].intersection(oper[1])
									if len(ineq[2]) != 0:
										keep.add(group_ineqs.index(ineq))
				l = list(keep)
				l.sort()
				l.reverse()
				for i in l:
					del group_ineqs[i]
		# combine implications
		group_imps = []
		for entry in group:
			if group_imps == []:
				group_imps = deepcopy(entry[3])
			else:
				keep = set()
				for imp in group_imps:
					for lhs in entry[3]:
						if imp[0] in lhs[0]:
							imp[1].intersection(lhs[1])
							if len(lhs[1]) == 0:
								keep.add(group_imps.index(imp))
				l = list(keep)
				l.sort()
				l.reverse()
				for i in l:
					del group_ineqs[i]
		# create struct
		#print(sets_combine(group_eqs) == group_eqs)
		out.append([sets_combine(group_eqs),group_equivs,group_ineqs,group_imps])
	return [condition,out]
	
def print_cache(cache, outf):
	#print(cache)
	#return
	cnt = 0
	for entry in cache:
			outf.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nCONDITION:  " + entry[0].replace("..","").replace(":::ENTER","") + "\n~~ begin equality sets ~~\n")
			#entry[1][0] = sets_combine(entry[1][0])
			# eqs - lets separate out 'origs'
			origs = []
			removes = []
			for eq in entry[1][0]:
				if len(eq) == 2:
					pair = list(eq)
					pair.sort()
					if "orig(" + pair[0] in pair[1]:
						origs.append(pair[0])
						removes.append(eq)			
			for eq in removes:
				entry[1][0].remove(eq)
			for eqs in entry[1][0]:
				outf.write(sorted(eqs) + "\n")
				cnt = cnt + 1
			if origs != []:
				outf.write(" ~ unchanged register(s) ~ \n")
				outf.write(sorted(origs) + "\n")
				cnt = cnt + 1
			outf.write("~~ end equality sets ~~\n~~ begin equivalence sets ~~\n")
			for eqs in entry[1][1]:
				outf.write(sorted(eqs) + "\n")
				cnt = cnt + 1
			outf.write("~~ end equivalence sets ~~\n~~ begin inequality properties ~~\n")
			for ineqs in entry[1][2]:
				if ineqs != []:
					for opers in ineqs[1]:
						if len(opers[1]) != 0:
							outf.write(ineqs[0] + " " + opers[0] + " _x_ for all _x_ in  " + sorted(opers[1]) + "\n")
							cnt = cnt + 1
			outf.write("~~ end inequality properties ~~\n~~ begin implication properties ~~\n")
			for imps in entry[1][3]:
				outf.write(imps[0] + " ==>  _x_ for all _x_ in  " + sorted(imps[1]) + "\n")
			outf.write("~~ end implication properties ~~\n~~ begin raw properties ~~\n")
			outf.write(entry[2])
			cnt = cnt + entry[2].count("\n")
			outf.write("~~ end raw properties ~~\n")
	#print(cnt)
	#print("\n\n\n")
	return cache
	#print_globals(extract_globals(cache, "(CPL==0)"),outf)
	
def cull_globals(cache,struct):
	[condition, globals_list] = struct
	notcond = "not" + condition
	for entry in cache:
		# find appropriate globals to compare to
		if notcond in entry[0]: # contains relevant condition
			globs = globals_list[2]
		elif condition in entry[0]:
			globs = globals_list[1]
		else:
			globs = globals_list[0]
		#eqs
		eqs_remove = []
		for eq in entry[1][0]:
			for g_eq in globs[0]:
				if eq.issubset(g_eq):
					eqs_remove.append(eq)
		for eq in eqs_remove:
			entry[1][0].remove(eq)
		#equivs - barely changed
		eqs_remove = []
		for eq in entry[1][1]:
			for g_eq in globs[1]:
				if eq.issubset(g_eq):
					eqs_remove.append(eq)
		for eq in eqs_remove:
			entry[1][1].remove(eq)
		#ineqs
		ineqs_to_remove = []
		for ineq in entry[1][2]:
			opers_to_remove = []
			for g_ineq in globs[2]:
				if ineq[0] in g_ineq[0]:
					for oper in ineq[1]:
						vals_to_remove = set()
						if oper[0] in g_ineq[1]:
							for val in oper[1]:
								if val in g_ineq[2]:
									vals_to_remove.add(val)
						for val in vals_to_remove:
							oper[1].remove(val)
						if len(oper[1]) == 0:
							opers_to_remove.append(oper)
			#print(ineq[1])
			#print(opers_to_remove)
			temp = [ii for n,ii in enumerate(opers_to_remove) if ii not in opers_to_remove[:n]]
			for oper in temp:
				ineq[1].remove(oper)
			if len(ineq[1]) == 0:
				ineqs_to_remove.append(ineq)
		temp = [ii for n,ii in enumerate(ineqs_to_remove) if ii not in ineqs_to_remove[:n]]
		for ineq in temp:
			entry[1][2].remove(ineq)
		
		#imps
		imp_remove = []
		for imp in entry[1][3]:
			p_remove = []
			for g_imp in globs[3]:
				if imp[0] in g_imp[0]:
					for p in imp[1]:
						if p in g_imp[1]:
							p_remove.append(p)
			for p in p_remove:
				imp[1].remove(p)
			if len(imp[1]) == 0:
				imp_remove.append(imp)
		for imp in imp_remove:
			entry[1][3].remove(imp) 
	return cache

		
def splice(name,pre):
	#print(name)
	#print(pre)
	in_file = open(name + "_one.out", "r") # for ones
	check_next = False
	do_transfer = False
	do_save = False
	save_name = ""
	#for_out = ""
	cache = [] # should be of form [<ENTER line>,[<list of sets of equal regs>, <list of sets of equivalent properties>, <inequality struct>, <implication struct>],<raw string>]]
	for line in in_file:
		if "Exiting Dai" in line:
			#outf = open(name + "_" + pre + "_moded.out", "w")
			#$cache = expand_ineq(cache[1:])
			globs = extract_globals(cache, "(" + pre + ")")
			#if len(globs) == 1:
			#	print("NON-MODAL PRECONDITION:  " + pre)
			#	return
			#if globs[1][1] == [[],[],[],[]] or globs[2][1] == [[],[],[],[]]:  # this will need to become more expansive
			#	print("NON-MODAL PRECONDITION:  " + pre)
			#	return
			#print("~EU-MODAL PRECONDITION:  " + pre)
			#print_globals(globs,outf)
			to_print = cull_globals(cache, globs)
			#print_cache(to_print, outf)
			print(globs)
			return [globs,to_print]
		elif "====" in line:
			check_next = True
			if do_transfer:
				out_file.write(line)
			do_transfer = False
			do_save = False
		elif check_next:
			save_name = line.rstrip()
			if "condition" in save_name:
				cache.append([save_name,[[],[],[],[]],""]) 
				do_save = True
			check_next = False
		elif do_save:
			#print(cache)
			add_to_cache(save_name, cache, line)
	globs = extract_globals(cache, "(" + pre + ")")
	to_print = cull_globals(cache, globs)
	return [globs,to_print]

def one_split(pres,name): # ones version of the parser from split.py
	s = ""
	for pre in pres:
		s = s + pre + "\n"
	out = open(name + "_one.spinfo", "w")
	out.write("\n\nPPT_NAME ..clock"+ '\n' + s)	
	return

def do_splice(dtraces,declss,spinfos,pre):
	name = pre

	if is_ones:
		uniq_insts.one_parse(name)
		declss.append(name + "_one.decls")
		one_split(pres,name)
		spinfos.append(name + "_one.spinfo")
	else:
		# in non-one case, uniq_insts will be called from in_parse for now
		
		s = ""
		for pre in pres:
			s = s + pre + "\n"
		split.parse(s, names, name)  
	cmd = "java daikon.Daikon"
	for dtrace in dtraces:
		cmd = cmd + " " + dtrace
	for decls in declss:
		cmd = cmd + " " + decls
	for spinfo in spinfos:
		cmd = cmd + " " + spinfo
	cmd = cmd + " >" + name + ".out"
	#print(cmd)
	system(cmd)
	splice(name,pres[0])

def do_splices_old():
	#system("export JAVA_HOME=${JAVA_HOME:-$(dirname $(dirname $(dirname $(readlink -f $(/usr/bin/which java)))))}")
	#system("export CLASSPATH=\"/home/mars/radish/daikon-5.7.2/daikon.jar\"")
	#system("export DAIKONDIR=\"/home/mars/radish/daikon-5.7.2\"")
	is_ones = True
	names = ["sel4", "cs2"] # ["cs", "cs2", "deb", "fl1", "fl2", "odin", "sol"] # no boot, reducing dev time
	# finding manually for now
	elfs = [1,2,4,6,8,9,11,13]
	cr0s = [0,1,2,3,5,7,18,20]
	cr4s = [6,8,9,11,12]
	regs = ["SMM", "CPL"]
	for [s,inds] in [["ELF",elfs],["CR0",cr0s],["CR4",cr4s]]:  # does this work?
		for ind in inds:
			regs.append(s + "_" + str(ind))
			#pres.append("orig(" + s + "_" + str(ind) + ")==" + s + "_" + str(ind))
	#regs = [] # to reduce dev time	
	regs = ["SMM", "CPL"]
	pres = []
	#print(pres)
	#exit()
	is_ones = True
	name = "exp"
	dtraces = ["sel4","cs2"] # usually will be generated from names but testing for now with reduced set
	declss = []
	spinfos = []
	if is_ones:
		dtraces = [n + "_one.dtrace" for n in names]
		#for n in names:
		#	in_one.parse(n)		#- commenting to reduce dev time
		#uniq_insts.one_parse(name)
		declss.append(name + "_one.decls")
		spinfos.append(name + "_one.spinfo")
	else:
		# in non-one case, uniq_insts will be called from in_parse for now
		s = ""
		for pre in pres:
			s = s + pre + "\n"
		split.parse(s, names, name)  		
	cmd = "java daikon.Daikon"
	for dtrace in dtraces:
		cmd = cmd + " " + dtrace
	for decls in declss:
		cmd = cmd + " " + decls
	for spinfo in spinfos:
		cmd = cmd + " " + spinfo
	cmd = cmd + " >" + name + ".out"
	for reg in regs:
		pres = ["0==" + reg]
		one_split(pres,name) # batch out spinfos for performance
		print("REG == " + reg + ":  Entering Daikon for rules")
		system(cmd)
		print("REG == " + reg + ":  Splicing for rules")
		r = splice(name,pres[0])
		print(r)
		pres = ["orig(" + reg + ")==" + reg]
		one_split(pres,name) # batch out spinfos for performance
		print("REG == " + reg + ":  Entering Daikon for bounds")
		system(cmd)
		print("REG == " + reg + ":  Splicing for bounds")
		b = splice(name,pres[0])
		#splice returns [globs, to_print]
		outf = open(name + "_" + reg + "_moded.out", "w")
		print_globals(r[0],outf)
		print_globals(b[0],outf)
		print_cache(r[1], outf)
		print_cache(b[1], outf)

def do_splices():
	names = ["cs","fl1","deb","fl2","sel4","cs2","odin","sol"] # no boot, reducing dev time
	cmd = "java -Xmx1g daikon.Daikon "
	for name in names:
		print(name)
		system(cmd + name + ".dtrace in_trace.decls in_trace.spinfo>" + name + "_delta_cpl.out")

#splice("1sp")
#splice("cs3")
#one_split("SMM==1","smm")
#splice("one_css")
do_splices()
