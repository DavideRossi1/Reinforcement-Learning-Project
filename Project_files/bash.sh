#!/bin/bash

#files=("Constants1.py" "Constants2.py" "Constants3.py" "Constants4.py" "Constants5.py" "Constants6.py" "Constants7.py")


for i in 1 2 3 4 5 6 7 8
do
    current_file="Constants"$i".py"
    mv "$current_file" "Constants.py"
    python main.py
    mv "Constants.py" "$current_file"
done