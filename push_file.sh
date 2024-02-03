#!/bin/bash

# Replace these variables with your actual values
USERNAME="itayfroo"
REPOSITORY="itayfroo/stock-analyzer"
BRANCH="main"
FILENAME="users.json"

# Create a new file or update an existing one
echo "Hello, World!" > $FILENAME

# Check if the file content has changed
if [ -n "$(git status --porcelain $FILENAME)" ]; then
    # Add the file to the staging area
    git add $FILENAME

    # Commit the changes with a message
    git commit -m "Update $FILENAME"

    # Push the changes to the remote repository
    git push origin $BRANCH
else
    echo "No changes detected in $FILENAME."
fi
