#!/bin/bash

for i in {1..21};
do
    current_file="Constants"$i".py"
    mv "$current_file" "Constants.py"
    python main.py
    mv "Constants.py" "$current_file"
done
