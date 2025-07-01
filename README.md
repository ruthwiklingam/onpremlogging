# Log Ingestion and Dashboard Solution

This project provides a complete solution for ingesting log files using Docker and visualizing them on a dashboard using the ELK stack (Elasticsearch, Logstash, Kibana) with Fluent Bit for log collection.

## Architecture

- **Elasticsearch**: Stores and indexes log data
- **Kibana**: Provides dashboard visualization and log analysis
- **Fluent Bit**: Lightweight log processor and forwarder
- **Log Generator**: Sample application that generates realistic log data

## Prerequisites

- Docker and Docker Compose installed on your system
- At least 4GB of RAM available for Elasticsearch

## Quick Start

1. **Start the stack**:
   ```bash
   docker-compose up -d
   ```

2. **Wait for services to be ready** (this may take 2-3 minutes):
   ```bash
   # Check if Elasticsearch is ready
   curl http://localhost:9200/_cluster/health
   
   # Check if Kibana is ready
   curl http://localhost:5601/api/status
   ```

3. **Access Kibana Dashboard**:
   Open your browser and go to: http://localhost:5601

## Setting Up Your Log Files

### For Existing Log Files

1. **Place your log files** in the appropriate directories:
   - JSON formatted logs: `./logs/` directory
   - Plain text logs: `./sample-logs/` directory

2. **Update Fluent Bit configuration** (if needed):
   Edit `fluent-bit/fluent-bit.conf` to match your log format and file locations.

### Supported Log Formats

The solution supports multiple log formats out of the box:

1. **JSON logs** (recommended):
   ```json
   {"timestamp": "2024-06-30T10:15:23", "level": "INFO", "message": "User logged in", "user_id": "123"}
   ```

2. **Common application logs**:
   ```
   2024-06-30 10:15:23 [INFO] Application started successfully
   ```

3. **Apache/Nginx access logs**:
   ```
   192.168.1.100 - - [30/Jun/2024:10:15:23 +0000] "GET /api/users HTTP/1.1" 200 1024
   ```

## Creating Dashboards in Kibana

1. **Access Kibana**: http://localhost:5601

2. **Create Index Pattern**:
   - Go to Management → Stack Management → Index Patterns
   - Click "Create index pattern"
   - Enter pattern: `fluentbit-*`
   - Select timestamp field: `@timestamp`

3. **Explore Your Data**:
   - Go to Analytics → Discover to view raw logs
   - Go to Analytics → Dashboard to create visualizations

4. **Create Visualizations**:
   - Log level distribution (pie chart)
   - Timeline of log events (line chart)
   - Top error messages (data table)
   - Geographic distribution (if IP data available)

## Customization

### Adding New Log Sources

1. **Update docker-compose.yml**:
   Add volume mounts for your log directories:
   ```yaml
   fluent-bit:
     volumes:
       - ./your-logs:/var/log/your-app:ro
   ```

2. **Update Fluent Bit configuration**:
   Add new INPUT sections in `fluent-bit/fluent-bit.conf`:
   ```ini
   [INPUT]
       Name              tail
       Path              /var/log/your-app/*.log
       Tag               your-app.logs
       Parser            your-parser
       Refresh_Interval  5
       Read_from_Head    true
   ```

### Custom Log Parsers

Add custom parsers in `fluent-bit/parsers.conf`:

```ini
[PARSER]
    Name        your-custom-parser
    Format      regex
    Regex       ^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?<level>\w+) (?<message>.*)$
    Time_Key    time
    Time_Format %Y-%m-%d %H:%M:%S
```

## Monitoring and Maintenance

### Check Service Status

```bash
# View all container status
docker-compose ps

# View logs for specific service
docker-compose logs elasticsearch
docker-compose logs kibana
docker-compose logs fluent-bit
```

### Storage Management

Elasticsearch data is persisted in a Docker volume. To clean up:

```bash
# Stop services
docker-compose down

# Remove data (WARNING: This deletes all log data)
docker volume rm loggingideas_elasticsearch_data
```

## Troubleshooting

### Common Issues

1. **Elasticsearch won't start**:
   - Ensure you have enough memory (4GB recommended)
   - Check Docker logs: `docker-compose logs elasticsearch`

2. **Kibana can't connect to Elasticsearch**:
   - Wait for Elasticsearch to be fully ready
   - Check network connectivity between containers

3. **No logs appearing in Kibana**:
   - Verify log files are in the correct directories
   - Check Fluent Bit logs: `docker-compose logs fluent-bit`
   - Ensure log files are readable (not being written to exclusively)

### Performance Tuning

For production use:

1. **Elasticsearch**:
   ```yaml
   environment:
     - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
   ```

2. **Add resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 4G
   ```

## Scaling

For larger log volumes:

1. **Use Elasticsearch cluster**: Deploy multiple Elasticsearch nodes
2. **Add Logstash**: For more complex log processing
3. **Use Kafka**: For high-throughput log streaming
4. **Implement log rotation**: To manage disk space

## Security Considerations

For production deployment:

1. Enable Elasticsearch security features
2. Use TLS/SSL for all communications
3. Implement proper authentication and authorization
4. Regular security updates for all components

## Sample Dashboards

The solution includes sample logs that demonstrate:
- Application performance monitoring
- Error tracking and alerting
- User activity analysis
- System resource monitoring

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Docker logs for error messages
3. Consult Elastic Stack documentation

# onpremlogging
Logging and Monitoring for on prem apps using Docker, ElasticSearch and Kibana
