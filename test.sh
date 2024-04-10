#!/bin/bash

# Variables
URL="http://mytravel-123.com"  # Change this to your actual URL
COOKIE="INGRESSCOOKIE"

# Function to send HTTP request and extract backend service from response headers
send_request() {
  local response=$(curl -s -i $URL)
  local backend_service=$(echo "$response" | grep -i "X-Backend-Service" | awk '{print $2}')
  echo "$backend_service"
}

# Initialize counters
frontend_service_count=0
frontend_service2_count=0

# Number of requests to send
total_requests=100

# Send requests and count backend service occurrences
for ((i=1; i<=$total_requests; i++)); do
  backend_service=$(send_request)
  if [ "$backend_service" == "frontend-service" ]; then
    ((frontend_service_count++))
  elif [ "$backend_service" == "frontend-service2" ]; then
    ((frontend_service2_count++))
  fi
done

# Calculate percentages
frontend_service_percentage=$(echo "scale=2; ($frontend_service_count / $total_requests) * 100" | bc)
frontend_service2_percentage=$(echo "scale=2; ($frontend_service2_count / $total_requests) * 100" | bc)

# Print results
echo "Results after $total_requests requests:"
echo "frontend-service: $frontend_service_count requests ($frontend_service_percentage%)"
echo "frontend-service2: $frontend_service2_count requests ($frontend_service2_percentage%)"
