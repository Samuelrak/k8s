#!/bin/bash

URL="http://mytravel-123.com/"

for ((i=1; i<=10; i++)); do
    echo "Request $i:"
    RESPONSE=$(curl -sI $URL)
    VERSION_HEADER=$(echo "$RESPONSE" | grep -i "X-Version")
    CANARY_HEADER=$(echo "$RESPONSE" | grep -i "X-Canary")
    
    echo "Version Header: $VERSION_HEADER"
    echo "Canary Header: $CANARY_HEADER"
    echo "----------------------------------"
done
