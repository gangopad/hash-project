# Compute hashs of all files in directory $1 to dir $2

for file in $1/*; do 
	md5 -q $file | tr -d '\n' > $2/$(basename $file).md5
done
