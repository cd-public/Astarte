# README #

Supporting files for the Astarte tool.

### Python Scripts ###

This is a snapshot of the constellation of scripts that comprise Daikon front
end and post processor that accepted as input the debug information from a Qemu
run and produce as output "human readable" properties, which contain the 
necessary properties to block any of the exploits seen in Michael's thesis.

The snapshots are from 5 Sept 2019.  I do have versions of this files I was
iterating over up to 7 Nov 2019, but if my memory serves this is the snapshot
the paper was written from because it was the first to have the coverage I was
hoping for. I can't say I'm proud of the level of documentation due to deadline
pressure, but the processor flow sketch is: 

	uniq_insts: qemu debug -> decls

utility function to define program points. 
	
	in_parse: qemu debug -> dtrace

first pass frontend, for security labels. 
	
	in_one: qemu debug -> decls

second pass frontend, for security properties. 
	
	split: daikon output -> spinfo

first pass analyzer, generate splitinfo file for Daikon preconditions
	
	moder: daikon output -> plain text, less readable

find modes from Daikon output 
	
	inter: plain text, less readable -> plain text, more readable

simply modes from Daikon out

### "ref" ###

This is the working document I used while drafting the Astarte paper. It is the 
output of the toolchain process with my manual annotations to help keep track
of what the different bits mean.

### Who do I talk to? ###

* cd@cs.unc.edu

## Acknowledgements  

This material is based upon work
supported by the National Science Foundation under Grants
No. CNS-1651276 and CNS-1816637, by the Semiconductor
Research Corporation, Intel, and by a Google Faculty Research
Award.
