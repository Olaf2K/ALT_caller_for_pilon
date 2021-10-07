#!/usr/bin/env bash

#grep -v 'QP=.*;PC' HsAll-90-No0-LC-DP29-DUP-00to01.vcf > missing
#wait
#grep -vf missing HsAll-90-No0-LC-DP29-DUP-00to01.vcf > removing_missing
#wait
##quality check these numbers should all be the same
#wc -l removing_missing
#wc -l temp
#wc -l out

#replaces . with something else in other file only when dot not when anything else e.g. a or aa etc.

echo ''>out_file
n=1
while read p; do
echo "$p" > test_file_for_check
check=$(cut -f5 test_file_for_check)
rep=$(sed "${n}q;d" temp)	
echo $rep
#echo $check
  if [ $check = "." ];  then
	var=$(echo "$p" | awk 'BEGIN{FS=OFS="\t"} {if (NR==1) {$5="replace_me"}{print}}' )
	test2="${var/replace_me/"$rep"}" 
	#echo "$test2"
	var2=$(echo "$test2" | awk 'BEGIN{FS=OFS="\t"} {if (NR==1) {$10="replace_me"}{print}}' )
	test="${var2/replace_me/"0/1"}"  
	#echo $rep
	echo "$test">>out_file
	#sed -i "${n}s|.*|$test|g" removing_missing
else
	echo "$p">>out_file
  fi
  let "n+=1"
#echo $n
done <removing_missing
