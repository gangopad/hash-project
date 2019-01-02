# Takes in a directory of binary files
# Writes a hexdump of each file to *.hex and removes the original file

for f in $1/*; do 
	hexdump -ve '1/1 "%.2x"' $f > ${f}.hex
	rm -f $f
done
