#!/bin/bash

# Source file
source_file="shapenet_train_0_1000.sh"

# Loop to generate new files and update the indices
for i in $(seq 1000 1000 53000); do
    start=$i
    end=$((i + 1000))
    new_file="shapenet_train_${start}_${end}.sh"
    
    # Copy the source file to the new file
    cp "$source_file" "$new_file"
    
    # Update the start_idx and end_idx variables in the new file
    sed -i "s/^start_idx=[0-9]\+/start_idx=$start/" "$new_file"
    sed -i "s/^end_idx=[0-9]\+/end_idx=$end/" "$new_file"
done

echo "Files copied, renamed, and indices updated successfully."
