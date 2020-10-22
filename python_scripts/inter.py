# intersect.py
# finding properties true in all daikon outputs given
# heavily borrows from legacy splice codes


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

def intersect():
	out_files = []
	# the struct
	# thinking i want a list of tuples of prefixes and sets of properties, maybe with a third for traces it appears in
	struct = []
	start = False
	curr_entry = []
	comp_set = []
	curr_set = []
	for n in ["cs","fl1","deb","fl2","sel4","cs2","odin","sol"]:
		# loop over lines
		start = False
		curr_entry = []
		comp_set = []
		for line in open(n + "_delta_cpl.out", "r"):
			if not start:
				if "===" in line:
					start = True
			else:
				if "Exit" in line or "===" in line: # cases without info
					1 == 1
				elif ".." in line[0:2]: # new prefix
					# wrap up old prefix
					if len(comp_set) > 0:
						curr_set = curr_entry[1]
						curr_entry[1] = curr_set.intersection(curr_set)
					# set up new prefix
					prefix = line
					new_pre = True
					for entry in struct: # find the prefix in struct
						if prefix in entry[0]:
							curr_entry = entry
							new_pre = False
							entry[2].append(n)
							comp_set = set()
					if new_pre: # if not in struct, add it
						comp_set = set()
						curr_entry = [prefix,comp_set,[n]]
						struct.append(curr_entry)
						
				else:
					comp_set.add(line)
	#for entry in struct:
	#	print("=" * 78)
	#	print("\"" + entry[0].strip() + "\" from files " + str(entry[2]))
	#	l = list(entry[1])
	#	l.sort()
	#	for ele in l:
	#		print(ele.strip())
	
	# convert struct to a spliced cache
	for i in range(len(struct)):
		e = struct[i]
		curr_set = e[1]
		new_cache = [[],[],[],[]] # eqs, equivs, ineqs, imps
		for entry in curr_set:
			if "-1" in line or "one of" in line: # catch errors
				1 == 1
			elif " <==> " in entry:
				added = False
				reg_l = line.rstrip().split(" <==> ")
				regs = set([r.strip() for r in reg_l])
				for eqs in new_cache[1]:
					for reg in regs:
						if reg in eqs:
							for reg in regs:
								eqs.add(reg)
							added = True
				if not added:
					new_cache[1].append(regs)
			elif " ==> " in entry:	
				new_cache[2].append(entry)	
			elif " == " in entry:
				added = False
				regs = set(entry.rstrip().split(" == "))
				for eqs in new_cache[0]:
					for reg in regs:
						if reg in eqs:
							for reg in regs:
								eqs.add(reg)
								added = True

				if not added:
					new_cache[0].append(regs)

			elif entry.isalpha():
				new_cache[3].append(entry)
		# clean up eqs before adding
		new_cache[0] = sets_combine(new_cache[0])
		struct[i][1] = new_cache
	for entry in struct:
		print("=" * 78)
		print("\"" + entry[0].strip() + "\" from files " + str(entry[2]))
		for ele in entry[1][0]:
			l = list(ele)
			l.sort()
			print(l)
			1 == 1

intersect()
