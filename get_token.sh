# Get and print just the token
TOKEN=$(curl -s -X POST http://localhost:8080/realms/cars-api/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=fastapi-client" \
  -d "client_secret=bfee999244ca763250fa4c1f9df53e2ade7f16fe08ad19b3a2ea48e9e3ebedd5" \
  -d "username=testuser" \
  -d "password=password123" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Your JWT Token:"
echo $TOKEN