import json
import time
import random
import logging
from datetime import datetime
from faker import Faker
import os

# Setup logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_interval = int(os.getenv('LOG_INTERVAL', '5'))

# Configure JSON logging
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(message)s',
    handlers=[
        logging.FileHandler('/app/logs/application.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
fake = Faker()

# Sample log levels and messages
LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
SERVICES = ['auth-service', 'user-service', 'payment-service', 'notification-service', 'api-gateway']
ACTIONS = ['login', 'logout', 'create_user', 'process_payment', 'send_email', 'api_call', 'database_query']

def generate_log_entry():
    """Generate a structured log entry"""
    timestamp = datetime.now().isoformat()
    level = random.choice(LOG_LEVELS)
    service = random.choice(SERVICES)
    action = random.choice(ACTIONS)
    user_id = fake.uuid4()
    
    # Generate different types of log messages based on level
    if level == 'ERROR':
        messages = [
            f"Failed to {action} for user {user_id}: Connection timeout",
            f"Database error in {service}: Table not found",
            f"Authentication failed for user {user_id}",
            f"Payment processing failed: Insufficient funds"
        ]
    elif level == 'WARNING':
        messages = [
            f"High response time detected in {service}: {random.randint(2000, 5000)}ms",
            f"Rate limit approaching for user {user_id}",
            f"Deprecated API endpoint used: /api/v1/{action}",
            f"Memory usage high in {service}: {random.randint(80, 95)}%"
        ]
    elif level == 'INFO':
        messages = [
            f"Successfully completed {action} for user {user_id}",
            f"New user registered: {user_id}",
            f"Payment processed successfully: ${random.randint(10, 1000)}",
            f"Email sent to user {user_id}"
        ]
    else:  # DEBUG
        messages = [
            f"Starting {action} process in {service}",
            f"Cache hit for key: {action}_{user_id}",
            f"Processing request from IP: {fake.ipv4()}",
            f"Database query executed in {random.randint(10, 200)}ms"
        ]
    
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "action": action,
        "user_id": user_id,
        "message": random.choice(messages),
        "request_id": fake.uuid4(),
        "ip_address": fake.ipv4(),
        "response_time": random.randint(50, 2000),
        "status_code": random.choice([200, 201, 400, 401, 404, 500]) if level == 'ERROR' else random.choice([200, 201, 202])
    }
    
    return json.dumps(log_entry)

def main():
    """Main function to generate logs continuously"""
    print(f"Starting log generator with interval: {log_interval}s")
    
    # Ensure log directory exists
    os.makedirs('/app/logs', exist_ok=True)
    
    while True:
        try:
            log_entry = generate_log_entry()
            logger.info(log_entry)
            time.sleep(log_interval)
        except KeyboardInterrupt:
            print("Log generation stopped")
            break
        except Exception as e:
            print(f"Error generating log: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
