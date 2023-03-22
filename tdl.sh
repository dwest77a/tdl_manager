FILE=$(pwd)/data/tdl_data.txt
DATA=$(pwd)/data
if ! [ -f "$FILE" ]; then
    if ! [ -f "$DATA" ]; then
	    echo "Creating data dir"
		mkdir $DATA
	fi
	echo "Creating new data text file for tdl"
	touch $FILE
else
	echo "Opening tdl data file"
fi

python $(pwd)/tdlman/tdlman.py