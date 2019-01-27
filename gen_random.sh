#$1 Directory to write files to 
#$2 Prefix
#$3 Number of additonal bits to generate 
#$4 Number of iterations 

for i in $(seq 1 $4); do 
	head -c $3 /dev/random >> $1/$i.bin
done
