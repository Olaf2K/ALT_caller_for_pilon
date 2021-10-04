# ALT_caller_for_pilon

To run:
Put both filter.py and replace.bash in the same folder as the VCF file you want to ALT call

python3 filter.py -i "input file" -l "work dir"

  Required:
	
    [-i] "Input file" <- This is the VCF file given by pilon
		
  Optional:
	
    [-l] "Working dir"
		

After the scripts are done running, run fuse.bash


