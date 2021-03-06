docker build -t stock-calculator-service:dev ./calculator-service
docker build -t stock-pricer-service:dev ./pricer-service
docker build -t stock-identity-service:dev ./identity-service
docker build -f ./client-service/Dockerfile.dev -t stock-client-service:dev ./client-service
docker build -t stock-gateway-service:dev ./gateway-service
docker build -t stock-redis-service:dev ./redis-service
docker build -t stock-nginx-service:dev ./nginx-service