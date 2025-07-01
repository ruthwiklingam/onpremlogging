#!/bin/bash

echo "🚀 Starting Log Ingestion and Dashboard Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "✅ Docker is running"

# Create necessary directories
mkdir -p logs sample-logs

if [ -d "logs" ]; then
    echo "   'logs' directory already exists."
else
    echo "   Created 'logs' directory."
fi

if [ -d "sample-logs" ]; then
    echo "   'sample-logs' directory already exists."
else
    echo "   Created 'sample-logs' directory."
fi

echo "📁 Created log directories"

# Start the services
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

echo "⏳ Waiting for services to start..."

# Wait for Elasticsearch to be ready
echo "🔍 Waiting for Elasticsearch..."
while ! curl -s http://localhost:9200/_cluster/health > /dev/null; do
    echo "   Still waiting for Elasticsearch..."
    sleep 10
done
echo "✅ Elasticsearch is ready"

# Wait for Kibana to be ready
echo "🔍 Waiting for Kibana..."
while ! curl -s http://localhost:5601/api/status > /dev/null; do
    echo "   Still waiting for Kibana..."
    sleep 10
done
echo "✅ Kibana is ready"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 Access your dashboard:"
echo "   Kibana: http://localhost:5601"
echo ""
echo "🔧 Service endpoints:"
echo "   Elasticsearch: http://localhost:9200"
echo "   Kibana: http://localhost:5601"
echo ""
echo "📝 Next steps:"
echo "   1. Open Kibana at http://localhost:5601"
echo "   2. Create an index pattern: 'fluentbit-*'"
echo "   3. Start exploring your logs in the Discover section"
echo ""
echo "📁 Log directories:"
echo "   - Add your JSON logs to: ./logs/"
echo "   - Add your text logs to: ./sample-logs/"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"
