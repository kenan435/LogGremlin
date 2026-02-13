import json
import random
import threading
import time
import sys
import os
from datetime import datetime

# OpenTelemetry imports
from opentelemetry import _logs, trace
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize OpenTelemetry
OTEL_HOST = os.getenv('OTEL_HOST', 'localhost')
OTEL_PORT = os.getenv('OTEL_PORT', '4317')

print(f"Connecting to OTEL at {OTEL_HOST}:{OTEL_PORT}", file=sys.stderr, flush=True)

# Create a logger provider (we'll create separate ones for each service.name)
logger_providers = {}
tracer_providers = {}

def get_logger_for_service(service_name):
    """Get or create a logger with the appropriate service.name resource attribute"""
    if service_name not in logger_providers:
        # Create resource with service.name
        resource = Resource.create({"service.name": service_name})
        
        # Create logger provider with this resource
        provider = LoggerProvider(resource=resource)
        
        # Add OTLP exporter
        exporter = OTLPLogExporter(
            endpoint=f"{OTEL_HOST}:{OTEL_PORT}",
            insecure=True
        )
        provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        
        # Get logger from this provider
        logger = provider.get_logger(__name__)
        logger_providers[service_name] = (provider, logger)
    
    return logger_providers[service_name][1]

def get_tracer_for_service(service_name):
    """Get or create a tracer with the appropriate service.name resource attribute"""
    if service_name not in tracer_providers:
        # Create resource with service.name
        resource = Resource.create({"service.name": service_name})
        
        # Create tracer provider with this resource
        provider = TracerProvider(resource=resource)
        
        # Add OTLP span exporter with shorter batch timeout
        span_exporter = OTLPSpanExporter(
            endpoint=f"{OTEL_HOST}:{OTEL_PORT}",
            insecure=True
        )
        # Use shorter schedule_delay for faster export (default is 5s)
        provider.add_span_processor(BatchSpanProcessor(span_exporter, schedule_delay_millis=1000))
        
        # Get tracer from this provider
        tracer = provider.get_tracer(__name__)
        tracer_providers[service_name] = (provider, tracer)
        
        print(f"DEBUG: Created tracer provider for {service_name}", file=sys.stderr, flush=True)
    
    return tracer_providers[service_name][1]


def generate_ip():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_internal_ip():
    range_choice = random.choice([1, 2, 3])
    if range_choice == 1:
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    elif range_choice == 2:
        return f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    else:
        return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_external_ip():
    while True:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        if not (ip.startswith("10.") or
                ip.startswith("172.16.") or ip.startswith("172.17.") or ip.startswith("172.18.") or ip.startswith("172.19.") or
                ip.startswith("172.20.") or ip.startswith("172.21.") or ip.startswith("172.22.") or ip.startswith("172.23.") or
                ip.startswith("172.24.") or ip.startswith("172.25.") or ip.startswith("172.26.") or ip.startswith("172.27.") or
                ip.startswith("172.28.") or ip.startswith("172.29.") or ip.startswith("172.30.") or ip.startswith("172.31.") or
                ip.startswith("192.168.") or
                ip.startswith("127.") or
                ip.startswith("0.") or
                ip.startswith("169.254.") or
                ip.startswith("224.") or ip.startswith("225.") or ip.startswith("226.") or ip.startswith("227.") or
                ip.startswith("228.") or ip.startswith("229.") or ip.startswith("230.") or ip.startswith("231.") or
                ip.startswith("232.") or ip.startswith("233.") or ip.startswith("234.") or ip.startswith("235.") or
                ip.startswith("236.") or ip.startswith("237.") or ip.startswith("238.") or ip.startswith("239.") or
                ip.startswith("255.")):
            return ip

def generate_log_level():
    return random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def generate_products():
    products = [
        "t-shirt",
        "jeans",
        "dress",
        "skirt",
        "blouse",
        "sweater",
        "jacket",
        "coat",
        "shorts",
        "leggings",
        "suit",
        "blazer",
        "hoodie",
        "cardigan",
        "tank top",
        "jumpsuit",
        "scarf",
        "hat",
        "gloves",
        "socks",
        "swimwear",
        "sports bra",
        "yoga pants",
        "running shoes",
        "boots"
    ]
    return random.choice(products)

def generate_request_uri():
    request_uris = [
        "/users/list",
        f"/products/details/{random.randint(11111, 99999)}",
        f"/search/query?term={generate_products()}",
        f"/api/v1/users/{random.randint(11111, 99999)}/profile",
        f"/checkout/cart/{random.randint(11111, 99999)}",
        "/login",
        "/register/new",
        f"/settings/user/{random.randint(11111, 99999)}/preferences",
        f"/images/gallery/album/{random.randint(11111, 99999)}"
    ]
    return random.choice(request_uris)

def generate_timestamp():
    timestamp_formats = [
        '%Y-%m-%d %H:%M:%S,%f',  # e.g., 2024-06-18 12:00:00,123456
        '%d/%b/%Y:%H:%M:%S %z',  # e.g., 18/Jun/2024:12:00:00 +0000
        '%Y-%m-%dT%H:%M:%SZ',    # e.g., 2024-06-18T12:00:00Z
        '%b %d, %Y %H:%M:%S %p', # e.g., Jun 18, 2024 12:00:00 PM
    ]
    format_choice = random.choice(timestamp_formats)
    timestamp = datetime.utcnow().strftime(format_choice)
    if '%f' in format_choice:
        return timestamp[:-3]  # Trim microseconds to milliseconds if present
    return timestamp

def generate_multiline_log():
    multiline_log_types = [
        generate_java_stack_trace,
        generate_python_traceback,
        generate_timestamped_error,
        generate_generic_multiline_log
    ]
    
    log_generator = random.choice(multiline_log_types)
    return log_generator()

def generate_java_stack_trace():
    stack_trace = [
        f'{generate_timestamp()} Exception in thread "main" java.lang.NullPointerException',
        '    at com.example.myproject.Book.getTitle(Book.java:16)',
        '    at com.example.myproject.Author.getBookTitles(Author.java:25)',
        '    at com.example.myproject.Bootstrap.main(Bootstrap.java:14)'
    ]
    return '\n'.join(stack_trace)

def generate_python_traceback():
    traceback = [
        f'{generate_timestamp()} Traceback (most recent call last):',
        '  File "<stdin>", line 1, in <module>',
        '  File "<string>", line 2, in <module>',
        'ValueError: math domain error'
    ]
    return '\n'.join(traceback)

def generate_timestamped_error():
    error_log = [
        f'{generate_timestamp()} ERROR [com.example.MyClass] Something went wrong',
        'java.lang.IllegalArgumentException: argument cannot be null',
        '    at com.example.MyClass.method(MyClass.java:50)',
        '    at com.example.MyClass.main(MyClass.java:30)'
    ]
    return '\n'.join(error_log)

def generate_generic_multiline_log():
    warn_log = [
        f'{generate_timestamp()} WARN [com.example.MyClass] Possible issue detected',
        '    at com.example.MyClass.method(MyClass.java:40)',
        '    at com.example.MyClass.main(MyClass.java:20)'
    ]
    return '\n'.join(warn_log)

def generate_structured_log():
    service = random.choice(['ALB', 'ELB', 'NGINX', 'VPCFLOW'])

    log_data = {}

    if service == 'ALB':
        log_data.update({
            'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'elb': f"elb_{random.randint(1, 100)}",
            'client': f"{generate_external_ip()}:443",
            'target': f"{generate_internal_ip()}:443",
            'request_processing_time': random.random(),
            'target_processing_time': random.random(),
            'response_processing_time': random.random(),
            'elb_status_code': random.choice([200, 301, 400, 404, 500]),
            'target_status_code': random.choice([200, 301, 400, 404, 500]),
            'received_bytes': random.randint(100, 10000),
            'sent_bytes': random.randint(100, 10000),
            'request_method': random.choice(['GET', 'POST']),
            'request_uri': f"{generate_request_uri()}",
            'target_protocol': 'HTTP/1.1',
            'user_agent': f"{generate_user_agent()}",
            'ssl_cipher': 'ECDHE-RSA-AES128-GCM-SHA256',
            'ssl_protocol': 'TLSv1.2',
            'target_group_arn': f"arn:aws:elasticloadbalancing:{random.choice(['us-east-1', 'us-west-2'])}:{random.randint(100000000000, 999999999999)}:targetgroup/{random.choice(['my-target-group', 'your-target-group'])}/{random.randint(1000, 9999)}",
            'trace_id': f"Root={random.randint(1, 999999)}",
            'domain_name': 'example.com',
            'chosen_cert_arn': 'arn:aws:acm:region:account-id:certificate/certificate-id',
            'matched_rule_priority': str(random.randint(1, 100)),
            'request_creation_time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'actions_executed': 'forward',
            'redirect_url': '-',
            'error_reason': '-',
            'target_port_list': f"{generate_ip()}:80",
            'target_status_code_list': str(random.choice([200, 301, 400, 404, 500])),
            'classification': '-',
            'classification_reason': '-',
        })
    elif service == 'ELB':
        log_data.update({
            'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'elb': f"elb_{random.randint(1, 100)}",
            'client': f"{generate_external_ip()}:80",
            'backend': f"{generate_internal_ip()}:80",
            'request_processing_time': random.random(),
            'backend_processing_time': random.random(),
            'response_processing_time': random.random(),
            'elb_status_code': random.choice([200, 301, 400, 404, 500]),
            'backend_status_code': random.choice([200, 301, 400, 404, 500]),
            'received_bytes': random.randint(100, 10000),
            'sent_bytes': random.randint(100, 10000),
            'request_method': random.choice(['GET', 'POST']),
            'request_uri': f"{generate_request_uri()}",
            'target_protocol': 'HTTP/1.1',
            'user_agent': f"{generate_user_agent()}",
            'ssl_cipher': 'ECDHE-RSA-AES128-GCM-SHA256',
            'ssl_protocol': 'TLSv1.2',
        })
    elif service == 'NGINX':
        log_data.update({
            'remote_addr': generate_external_ip(),
            'remote_user': '-', 
            'time_local': datetime.utcnow().strftime('%d/%b/%Y:%H:%M:%S +0000'),
            'request': f"{random.choice(['GET', 'POST'])} /path/to/resource HTTP/1.1",
            'status': random.choice([200, 301, 400, 404, 500]),
            'body_bytes_sent': random.randint(100, 10000),
            'http_referer': '-',
            'http_user_agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'request_time': random.random(),
            'upstream_connect_time': random.random(),
            'upstream_header_time': random.random(),
            'upstream_response_time': random.random(),
            'upstream_ip': generate_ip(),
        })
    elif service == 'VPCFLOW':
        ip_type = random.choice(['outbound', 'inbound'])

        if ip_type == 'outbound':
            srcaddr = generate_internal_ip()
            dstaddr = generate_external_ip()
        else: 
            srcaddr = generate_external_ip()
            dstaddr = generate_internal_ip()

        log_data.update({
            'version': 2,
            'account_id': 145556732243,
            'interface_id': f"eni-{random.randint(10000000, 99999999)}",
            'srcaddr': srcaddr,
            'dstaddr': dstaddr,
            'srcport': random.randint(1, 65535),
            'dstport': random.randint(1, 65535),
            'protocol': random.choice([6, 17]), 
            'packets': random.randint(1, 1000),
            'bytes': random.randint(40, 10000),
            'start': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'action': random.choice(['ACCEPT', 'REJECT']),
            'log_status': random.choice(['OK', 'NODATA', 'SKIPDATA']),
        })

    return service, json.dumps(log_data)

def generate_unstructured_log():
    unstructured_log = ""
    service = random.choice(['ALB', 'ELB', 'NGINX', 'VPCFLOW'])

    if service == 'ALB':
        unstructured_log = ""
        unstructured_log += f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} "
        unstructured_log += f"elb_{random.randint(1, 100)} "
        unstructured_log += f"{generate_external_ip()}:443 "
        unstructured_log += f"{generate_internal_ip()}:443 "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"{random.randint(100, 10000)} "
        unstructured_log += f"{random.randint(100, 10000)} "
        unstructured_log += f"{random.choice(['GET', 'POST'])} "
        unstructured_log += f"{generate_request_uri()} "
        unstructured_log += f"HTTP/1.1 "
        unstructured_log += f"{generate_user_agent()} "
        unstructured_log += f"ECDHE-RSA-AES128-GCM-SHA256 "
        unstructured_log += f"TLSv1.2 "
        unstructured_log += f"arn:aws:elasticloadbalancing:{random.choice(['us-east-1', 'us-west-2'])}:{random.randint(100000000000, 999999999999)}:targetgroup/{random.choice(['my-target-group', 'your-target-group'])}/{random.randint(1000, 9999)} "
        unstructured_log += f"Root={random.randint(1, 999999)} "
        unstructured_log += f"loggoblin.com "
        unstructured_log += f"arn:aws:acm:region:account-id:certificate/certificate-id "
        unstructured_log += f"{random.randint(1, 100)} "
        unstructured_log += f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} "
        unstructured_log += f"forward "
        unstructured_log += f"- "
        unstructured_log += f"- "
        unstructured_log += f"{generate_ip()}:80 "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"- "
        unstructured_log += f"-"

    elif service == 'ELB':
        unstructured_log = ""
        unstructured_log += f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} "
        unstructured_log += f"elb_{random.randint(1, 100)} "
        unstructured_log += f"{generate_internal_ip()}:80 "
        unstructured_log += f"{generate_internal_ip()}:80 "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"{random.randint(100, 10000)} "
        unstructured_log += f"{random.randint(100, 10000)} "
        unstructured_log += f"{random.choice(['GET', 'POST'])} "
        unstructured_log += f"{generate_request_uri()} "
        unstructured_log += f"HTTP/1.1 "
        unstructured_log += f"{generate_user_agent()} "
        unstructured_log += f"ECDHE-RSA-AES128-GCM-SHA256 "
        unstructured_log += f"TLSv1.2"

    elif service == 'NGINX':
        unstructured_log = ""
        unstructured_log += f"{generate_external_ip()} "
        unstructured_log += f"- "
        unstructured_log += f"[{datetime.utcnow().strftime('%d/%b/%Y:%H:%M:%S +0000')}] "
        unstructured_log += f"\"{random.choice(['GET', 'POST'])} /path/to/resource HTTP/1.1\" "
        unstructured_log += f"{random.choice([200, 301, 400, 404, 500])} "
        unstructured_log += f"{random.randint(100, 10000)} "
        unstructured_log += f"\"-\" "  
        unstructured_log += f"{generate_user_agent()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{random.random()} "
        unstructured_log += f"{generate_ip()}"

    elif service == 'VPCFLOW':
        ip_type = random.choice(['outbound', 'inbound'])

        if ip_type == 'outbound':
            srcaddr = generate_internal_ip()
            dstaddr = generate_external_ip()
        else: 
            srcaddr = generate_external_ip()
            dstaddr = generate_internal_ip()

        unstructured_log = f"2 "
        unstructured_log += f"145556732243 "
        unstructured_log += f"eni-{random.randint(10000000, 99999999)} "
        unstructured_log += f"{srcaddr} "
        unstructured_log += f"{dstaddr} "
        unstructured_log += f"{random.randint(1, 65535)} "
        unstructured_log += f"{random.randint(1, 65535)} "
        unstructured_log += f"{random.choice([6, 17])} "  
        unstructured_log += f"{random.randint(1, 1000)} "
        unstructured_log += f"{random.randint(40, 10000)} "
        unstructured_log += f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} "
        unstructured_log += f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} "
        unstructured_log += f"{random.choice(['ACCEPT', 'REJECT'])} "
        unstructured_log += f"{random.choice(['OK', 'NODATA', 'SKIPDATA'])}"

    return service, unstructured_log

def generate_random_text():
    texts = [
        "Sample log message",
        "Another test log entry",
        "This is a random log text",
        "Testing mapping exceptions",
        "Log entry with different format",
        "Example log message for testing"
    ]
    return random.choice(texts)

def generate_mapping_exception():
    exceptions = [
        {
            "severity": 6,
            "text": generate_random_text(),  # Expected: string, provided: string
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 6,
            "text": {
                "numbers": 123456
            },  # Expected: string, provided: object
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 6,
            "text": 123456,  # Expected: string, provided: number
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 3,
            "details": "Detailed message",  # Expected: object, provided: string
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 4,
            "details": {
                "info": "Detailed message"
            },  # Expected: object, provided: object
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 5,
            "count": "ten",  # Expected: number, provided: string
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 5,
            "count": 10,  # Expected: string, provided: number
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 2,
            "active": "yes",  # Expected: boolean, provided: string
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 2,
            "active": True,  # Expected: string, provided: boolean
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 1,
            "enabled": "true",  # Expected: boolean, provided: string
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 1,
            "enabled": False,  # Expected: string, provided: boolean
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 7,
            "created_at": "2024-06-24",  # Expected: date, provided: string
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        },
        {
            "severity": 7,
            "created_at": datetime.utcnow().isoformat(),  # Expected: string, provided: date object
            "random_text": generate_random_text(),
            "timestamp": int(time.time() * 1000)
        }
    ]
    return random.choice(exceptions)

def generate_logs_continuously(num_logs, sleep_interval, clear_interval):
    last_cleared_time = time.time()
    print("Starting log generation...", file=sys.stderr, flush=True)
    log_count = 0
    
    while not stop_thread_event.is_set():
        print(f"DEBUG: Top of while loop, generating {num_logs} logs", file=sys.stderr, flush=True)
        for i in range(num_logs):
            log_type = random.choice(['structured', 'unstructured', 'multiline', 'mapping_exception'])
            print(f"DEBUG: Loop iteration {i}, log_type={log_type}", file=sys.stderr, flush=True)
            
            try:
                if log_type == 'structured':
                    print(f"DEBUG: Before generate_structured_log()", file=sys.stderr, flush=True)
                    service_name, log_body = generate_structured_log()
                    print(f"DEBUG: After generate, service={service_name}", file=sys.stderr, flush=True)
                    
                    # Get logger and tracer for this service
                    logger = get_logger_for_service(service_name)
                    tracer = get_tracer_for_service(service_name)
                    print(f"DEBUG: Got logger and tracer", file=sys.stderr, flush=True)
                    
                    # Parse JSON to get attributes
                    log_attrs = json.loads(log_body)
                    
                    # Create a span for this request
                    with tracer.start_as_current_span(
                        name=f"{service_name}.request",
                        attributes={
                            "http.method": log_attrs.get("request_method", "GET"),
                            "http.status_code": log_attrs.get("elb_status_code") or log_attrs.get("backend_status_code") or log_attrs.get("status", 200),
                            "http.url": log_attrs.get("request_uri", "/"),
                        }
                    ) as span:
                        # Emit log with trace context
                        logger.emit(
                            body=json.dumps(log_attrs),
                            attributes=log_attrs,
                            severity_number=_logs.SeverityNumber.INFO
                        )
                    print(f"DEBUG: Emitted structured log and span for {service_name}", file=sys.stderr, flush=True)
                    
                elif log_type == 'unstructured':
                    service_name, log_message = generate_unstructured_log()
                    logger = get_logger_for_service(service_name)
                    tracer = get_tracer_for_service(service_name)
                    
                    # Create a span
                    with tracer.start_as_current_span(
                        name=f"{service_name}.operation",
                        attributes={"log.type": "unstructured"}
                    ):
                        logger.emit(
                            body=log_message,
                            severity_number=_logs.SeverityNumber.INFO
                        )
                    print(f"DEBUG: Emitted unstructured log and span for {service_name}", file=sys.stderr, flush=True)
                    
                elif log_type == 'multiline':
                    service_name = 'multiline'
                    log_message = generate_multiline_log()
                    logger = get_logger_for_service(service_name)
                    logger.emit(
                        body=log_message,
                        severity_number=_logs.SeverityNumber.INFO
                    )
                    print(f"DEBUG: Emitted multiline log", file=sys.stderr, flush=True)
                    
                elif log_type == 'mapping_exception':
                    service_name = 'mapping_exception'
                    log_data = generate_mapping_exception()
                    logger = get_logger_for_service(service_name)
                    logger.emit(
                        body=json.dumps(log_data),
                        attributes=log_data,
                        severity_number=_logs.SeverityNumber.INFO
                    )
                    print(f"DEBUG: Emitted mapping exception log", file=sys.stderr, flush=True)
                    
                log_count += 1
                if log_count % 10 == 0:
                    print(f"Emitted {log_count} logs so far...", file=sys.stderr, flush=True)
                    # Flush all tracer providers to ensure spans are sent
                    for service_name, (provider, _) in tracer_providers.items():
                        provider.force_flush()
                    break  # Exit inner loop to see debug output faster
                    
            except Exception as e:
                print(f"Error emitting log: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
                import traceback
                traceback.print_exc(file=sys.stderr)
                    
        print(f"DEBUG: Sleeping for {sleep_interval}s", file=sys.stderr, flush=True)
        time.sleep(sleep_interval)
        current_time = time.time()

num_logs_per_interval = 30
sleep_interval = 1  
clear_interval = 180  

stop_thread_event = threading.Event()

log_generation_thread = threading.Thread(target=generate_logs_continuously, args=(num_logs_per_interval, sleep_interval, clear_interval))
log_generation_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping log generation...")
    stop_thread_event.set()
    log_generation_thread.join()
