#!/bin/bash

for i in {11..21};
do
    current_file="Constants"$i".py"
    mv "$current_file" "Constants.py"
    for j in {1..5};
    do
    python main.py
    done
    echo "Done with "$current_file
    mv "Constants.py" "$current_file"
done
