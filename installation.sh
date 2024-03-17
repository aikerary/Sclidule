#!/bin/bash

# Copy the file to /usr/bin
cp sclidule /usr/bin

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Installation succesful"
else
    echo "Failed to copy file sclidule to /usr/bin, please execute sudo"
fi