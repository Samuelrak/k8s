#!/bin/bash

frontend_service_count=0
frontendv2_service_count=0

for ((i=1; i<=100; i++)); do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://mytravel-123.com/)

    if [[ $response == "200" ]]; then
        frontend_service_count=$((frontend_service_count + 1))
    elif [[ $response == "201" ]]; then
        frontendv2_service_count=$((frontendv2_service_count + 1))
    fi
done

echo "frontend-service count: $frontend_service_count"
echo "frontendv2-service count: $frontendv2_service_count"
