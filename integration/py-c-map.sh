#!/bin/bash

ascada_dir="ASCADA-GUI"
at328p_dir="ASCADA-AT328p"
table_file_name="py-c-map.csv"

IFS=$'\n'                                               # Defines the default separator to \n
for i in ${!log[@]}; do
    echo -e "Index: $i \t ContentAtIndex: ${log[$i]}"
done

# Gets the last comit info of ASCADA-GUI
cd $ascada_dir
gui_last_commit=($(git log -n 1))                       # Makes an array where its items are the lines of the last git's commit log.

# Gets the last comit info of ASCADA-AT328p
cd ../$at328p_dir
at328p_last_commit=($(git log -n 1))

# Append to Python <-> C code map.
cd ..
echo '-;-' >> $table_file_name
for i in ${!gui_last_commit[@]}; do
    echo "${gui_last_commit[$i]};${at328p_last_commit[$i]}" >> $table_file_name
done