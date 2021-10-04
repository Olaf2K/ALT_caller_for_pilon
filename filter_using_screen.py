### Tested on: 4.19.0-17-amd64 #1 SMP Debian 4.19.194-3 (2021-07-18) x86_64


### Loading packages ###
import os
import math
import heapq
import subprocess
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', type=str,
                      required=True)
  parser.add_argument('-l', type=str,
                      required=False)
  args = parser.parse_args()
  original_file = args.i
  if args.l is not None:
      os.chdir(args.l)

### Parameters ###
number_file = 'out'
batch_size = 100000

### Grabbing the numbers for the nucleotides ###
def bash_command(cmd):
    subprocess.call(cmd, shell=True)

bash_command(r"grep -o 'QP=.*;PC' "+original_file+" | sed 's/QP=//' | sed 's/;PC//' | sed 's/,/\t/g' > out")
print("Finding nucleotides...")
### Finding the  second highest value in the number_file ###
nucleotides = ['A','C','T','G']
temp_out_file = 'temp'
with open(number_file, 'r') as f:
    with open(temp_out_file, 'w') as temp:
        for line in f:
            ## splitting the values into a list ##
            line_values_only = line.replace('\n', '')
            split = line.split('\t')
            A = int(split[0])
            C = int(split[1])
            T = int(split[2])
            G = int(split[3].replace('\n', ''))
            check_for_second_highest = [A,C,T,G]
            ## finding the highest and second highest value ##
            highest_and_second_highest = heapq.nlargest(2, range(len(check_for_second_highest)), key=check_for_second_highest.__getitem__)
            ## check if that second highest value exists more than once ##
            tie_check = check_for_second_highest.count(check_for_second_highest[highest_and_second_highest[1]])
            if tie_check >= 2:
                # if so: write . into temp file
                temp.write('.'+'\n')
            else:
                #if not: write the nucl into temp file
                nucl = nucleotides[highest_and_second_highest[1]]
                temp.write(nucl+'\n')

### reverse grep for '##'

bash_command(r"grep -v '##\|#' "+original_file+" > in")
bash_command(r"grep '##\|#' "+original_file+" > temp_head")
### splitting files into smaller files for batch running
### moving files to dirs
### run bash files : you can autorun the submission using /scripts/csmit -c 5 -m 7G -b 'bash test.bash' : the -b tag prevents you from opening the log
### merging hte files
print("Checking file size...")
with open("in","r") as f:
    length_file = len(f.readlines())

number_of_batches = int(math.ceil(length_file/batch_size))

b = 1
x=0
e = batch_size
folders_to_be_made = []
files_made = []
print("Splitting files, and submitting to screens...")
with open('setup.bash', 'w') as f:
    for i in range(0,number_of_batches):
        f.write("".join(["sed -n ' ",str(b),",",str(e),"p' in > ",str(b),"-",str(e),".txt\n"]))
        f.write("wait\n")
        folders_to_be_made.append(''.join([str(b),"-",str(e),".txt_dir"]))
        files_made.append(''.join([str(b),"-",str(e),".txt"]))
        b = b+batch_size
        e = e+batch_size
    for i in folders_to_be_made:
        f.write("".join(["rm -r ",i,"\n"]))
        f.write("wait\n")
    for i in folders_to_be_made:
        f.write("".join(["mkdir ",i,"\n"]))
        f.write("wait\n")
    for i in folders_to_be_made:
        f.write("".join(["cp ",files_made[x]," ",i,"\n"]))
        f.write("wait\n")
        x+=1
    x=0
    for i in folders_to_be_made:
        f.write("".join(["cp replace.bash ",i,"\n"]))
        f.write("wait\n")
    b=1
    e=batch_size
    for i in folders_to_be_made:
        f.write("".join(["sed -n ' ",str(b),",",str(e),"p' temp > ",str(b),"-",str(e),".txt_dir/temp\n"]))
        f.write("wait\n")
        b = b + batch_size
        e = e + batch_size
    for i in folders_to_be_made:
        f.write("".join(["cd ",i,"\n"]))
        f.write("wait\n")
        f.write("".join(["cp ", files_made[x], " removing_missing", "\n"]))
        f.write("wait\n")
        f.write("".join(['screen -d -m bash -c "bash replace.bash"', "\n"]))
        f.write("wait\n")
        f.write("".join(['cd ../', "\n"]))
        f.write("wait\n")
        x+=1
    x=0


#1) how long is the file; split that up into chunks of 100 000; runs replace.bash on every file
bash_command(r"bash setup.bash")

b = 1
e = batch_size
with open('fuse.bash', 'w') as f:
    for i in folders_to_be_made:
        f.write("".join(["cat ",i,"/out_file >> pre_final","\n"]))
        f.write("wait\n")
        b = b+batch_size
        e = e+batch_size
    f.write("".join(["cat temp_head >> final"]))
    f.write("".join(["cat pre_final >> final"]))
    f.write("".join(["sed -i '/^$/d' final\n"]))

### Cleanup ###
#clean = ['temp_csv','temp','out','close_final.csv', 'in']
#for file in clean:
#    os.remove(file)
