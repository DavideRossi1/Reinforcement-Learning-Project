#!/bin/bash

for i in {11..11};
do
    current_file="Constants"$i".py"
    mv "$current_file" "Constants.py"
    for j in {1..10};
    do
    python main.py
    done
    echo "Done with "$current_file
    mv "Constants.py" "$current_file"
done
