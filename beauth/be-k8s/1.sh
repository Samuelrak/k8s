stable_count=0
canary_count=0

# Send multiple requests and count responses
for i in {1..100}; do
  response=$(curl -s -H "Host: mytravel-123.com" -H "Canary:" http://192.168.3.6/)
  if [[ $response == *"stable"* ]]; then
    ((stable_count++))
  elif [[ $response == *"canary"* ]]; then
    ((canary_count++))
  fi
done

# Output counts
echo "Stable responses: $stable_count"
echo "Canary responses: $canary_count"
