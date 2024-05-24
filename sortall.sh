#!/bin/bash

# Find all .txt files in the current directory and subdirectories
find . -type f -name "*.txt" | while read -r file; do
    # Sort the file in place
    sort "$file" -o "$file"
done