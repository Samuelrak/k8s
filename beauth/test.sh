frontend_service_count=0
frontendv2_service_count=0

for ((i=1; i<=100; i++)); do
    response=$(curl -s -o /dev/null -w "%{http_code}" -H "canary: true" http://mytravel-123.com/)

    # Check the response to determine which service served the request
    if [[ $response == "200" ]]; then
        frontend_service_count=$((frontend_service_count + 1))
    elif [[ $response == "201" ]]; then
        frontendv2_service_count=$((frontendv2_service_count + 1))
    fi
done

echo "frontend-service count: $frontend_service_count"
echo "frontendv2-service count: $frontendv2_service_count"

# Calculate the percentage of each service
total_requests=$((frontend_service_count + frontendv2_service_count))
frontend_percentage=$((frontend_service_count * 100 / total_requests))
frontendv2_percentage=$((frontendv2_service_count * 100 / total_requests))

echo "frontend-service percentage: $frontend_percentage%"
echo "frontendv2-service percentage: $frontendv2_percentage%"
