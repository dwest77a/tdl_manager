cd ~/Documents/tdl_manager
FILE=$(pwd)/tdl_data.txt
if ! [ -f "$FILE" ]; then
	echo "Creating new data text file for tdl"
	touch $FILE
else
	echo "Opening tdl data file"
fi

python $(pwd)/tdl_man_v2.py
