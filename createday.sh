#!/usr/bin/env bash
# Create a new day folder and copy template files
# Usage: ./createday.sh <day number>
# Example: ./createday.sh 1

# Check if argument is passed
if [ $# -eq 0 ]; then
    echo "Usage: ./createday.sh <day number>"
    exit 1
fi

# Check if day folder already exists
if [ -d "day$1" ]; then
    echo "Day folder already exists"
    exit 1
fi

# Create day folder, using day0/ as template
cp -r day0 day$1

echo "Created new folder: day$1/"
