#!/bin/bash

# Your OpenAI API key
OPENAI_API_KEY="sk-xxxx"

# Retrieve list of files and parse the IDs
file_ids=$(curl -s https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id')

# Loop over the file IDs and delete each file
for file_id in $file_ids; do
  echo "Deleting file: $file_id"
  curl -s -X DELETE https://api.openai.com/v1/files/$file_id \
    -H "Authorization: Bearer $OPENAI_API_KEY"
done
