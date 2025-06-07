#!/usr/bin/env python3
"""
Sample IP Dataset Generator for ASN Analysis Testing

This script generates a realistic sample dataset of IP addresses
that includes a mix of public infrastructure, cloud providers, 
CDNs, ISPs, and geographic diversity.
"""

import random
import ipaddress
from collections import defaultdict

def generate_sample_dataset(size=2000, output_file='sample_ip_list.txt'):
    """
    Generate a sample dataset of IP addresses for testing
    
    Args:
        size: Number of IP addresses to generate
        output_file: Output filename
    """
    
    # Real-world IP address ranges from major providers/organizations
    known_ranges = {
        # Google (AS15169)
        'google': [
            '8.8.8.0/24', '8.8.4.0/24', '8.34.208.0/20', '8.35.192.0/20',
            '74.125.128.0/17', '108.177.0.0/17', '172.217.0.0/16',
            '216.58.192.0/19', '64.233.160.0/19', '66.249.64.0/19'
        ],
        
        # Amazon AWS (AS16509, AS14618)
        'amazon': [
            '3.0.0.0/15', '13.32.0.0/15', '13.224.0.0/14', '15.177.0.0/18',
            '18.130.0.0/16', '18.144.0.0/15', '34.192.0.0/12', '35.72.0.0/13',
            '52.0.0.0/11', '54.64.0.0/11', '99.77.128.0/18', '205.251.192.0/19'
        ],
        
        # Cloudflare (AS13335)
        'cloudflare': [
            '1.1.1.0/24', '1.0.0.0/24', '104.16.0.0/13', '104.24.0.0/14',
            '108.162.192.0/18', '131.0.72.0/22', '141.101.64.0/18',
            '162.158.0.0/15', '172.64.0.0/13', '173.245.48.0/20',
            '188.114.96.0/20', '190.93.240.0/20', '197.234.240.0/22',
            '198.41.128.0/17'
        ],
        
        # Microsoft (AS8075)
        'microsoft': [
            '13.64.0.0/11', '13.104.0.0/14', '20.0.0.0/11', '23.96.0.0/13',
            '40.64.0.0/10', '52.224.0.0/11', '65.52.0.0/14', '70.37.0.0/17',
            '104.40.0.0/13', '137.116.0.0/14', '157.54.0.0/15', '168.61.0.0/16',
            '191.232.0.0/13', '199.30.16.0/20'
        ],
        
        # Facebook/Meta (AS32934)
        'facebook': [
            '31.13.24.0/21', '31.13.64.0/18', '66.220.144.0/20',
            '69.63.176.0/20', '69.171.224.0/19', '74.119.76.0/22',
            '103.4.96.0/22', '129.134.0.0/17', '157.240.0.0/17',
            '173.252.64.0/18', '179.60.192.0/22', '185.60.216.0/22'
        ],
        
        # Akamai (AS16625, AS20940)
        'akamai': [
            '2.16.0.0/13', '23.32.0.0/11', '23.192.0.0/11', '72.246.0.0/15',
            '96.16.0.0/15', '104.64.0.0/10', '184.24.0.0/13', '184.50.0.0/15'
        ],
        
        # Digital Ocean (AS14061)
        'digitalocean': [
            '104.131.0.0/16', '138.197.0.0/16', '139.59.0.0/16',
            '142.93.0.0/16', '157.230.0.0/16', '159.65.0.0/16',
            '161.35.0.0/16', '164.90.0.0/16', '165.227.0.0/16',
            '167.71.0.0/16', '167.172.0.0/16', '178.62.0.0/16',
            '188.166.0.0/16', '206.189.0.0/16'
        ],
        
        # Linode (AS63949)
        'linode': [
            '45.33.0.0/16', '45.56.0.0/16', '45.79.0.0/16',
            '66.175.208.0/20', '69.164.192.0/20', '72.14.176.0/20',
            '74.207.224.0/19', '96.126.96.0/19', '173.230.128.0/19',
            '173.255.192.0/18', '192.46.208.0/20', '198.58.96.0/19'
        ],
        
        # Comcast (AS7922)
        'comcast': [
            '68.80.0.0/13', '69.240.0.0/13', '71.192.0.0/11',
            '73.0.0.0/11', '75.64.0.0/13', '96.112.0.0/12',
            '98.192.0.0/10', '174.48.0.0/12', '184.56.0.0/13'
        ],
        
        # Verizon (AS701)
        'verizon': [
            '72.229.0.0/16', '108.25.0.0/16', '173.79.0.0/16',
            '174.192.0.0/10', '206.124.64.0/18', '98.80.0.0/12'
        ],
        
        # Universities and Research (Various ASNs)
        'education': [
            '18.0.0.0/8',        # MIT
            '36.0.0.0/8',        # Stanford  
            '128.32.0.0/16',     # UC Berkeley
            '129.25.0.0/16',     # Cornell
            '140.247.0.0/16',    # CMU
            '171.64.0.0/14'      # UCLA
        ]
    }
    
    # Generate weighted distribution (more realistic)
    distribution = {
        'google': 150,
        'amazon': 300,  # AWS is very common
        'cloudflare': 100,
        'microsoft': 200,
        'facebook': 50,
        'akamai': 80,
        'digitalocean': 150,
        'linode': 100,
        'comcast': 200,
        'verizon': 150,
        'education': 50
    }
    
    # Generate some random IP ranges for smaller ISPs/organizations
    random_ranges = []
    for _ in range(50):  # Generate 50 random /16 networks
        first_octet = random.choice([203, 202, 201, 200, 199, 198, 210, 211, 212, 213])
        second_octet = random.randint(1, 254)
        random_ranges.append(f"{first_octet}.{second_octet}.0.0/16")
    
    known_ranges['random_isps'] = random_ranges
    distribution['random_isps'] = 460  # Fill remaining slots
    
    # Generate IP addresses
    generated_ips = set()  # Use set to avoid duplicates
    ip_sources = {}  # Track which source each IP came from
    
    print(f"Generating {size} sample IP addresses...")
    
    for source, count in distribution.items():
        current_count = 0
        ranges = known_ranges[source]
        
        while current_count < count and len(generated_ips) < size:
            # Pick a random range
            range_str = random.choice(ranges)
            try:
                network = ipaddress.IPv4Network(range_str, strict=False)
                
                # Generate random IP within this range
                network_int = int(network.network_address)
                broadcast_int = int(network.broadcast_address)
                
                # Avoid network and broadcast addresses
                if broadcast_int - network_int > 2:
                    random_int = random.randint(network_int + 1, broadcast_int - 1)
                    ip = str(ipaddress.IPv4Address(random_int))
                    
                    if ip not in generated_ips:
                        generated_ips.add(ip)
                        ip_sources[ip] = source
                        current_count += 1
                        
            except Exception as e:
                print(f"Error generating IP from range {range_str}: {e}")
                continue
    
    # Convert to sorted list
    ip_list = sorted(list(generated_ips), key=lambda x: ipaddress.IPv4Address(x))
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write("# Sample IP Dataset for ASN Analysis\n")
        f.write(f"# Generated {len(ip_list)} unique IP addresses\n")
        f.write("# Distribution by source:\n")
        
        source_counts = defaultdict(int)
        for source in ip_sources.values():
            source_counts[source] += 1
        
        for source, count in sorted(source_counts.items()):
            f.write(f"# {source}: {count} IPs\n")
        
        f.write("#\n")
        f.write("# One IP per line below:\n")
        f.write("\n")
        
        for ip in ip_list:
            f.write(f"{ip}\n")
    
    print(f"\nGenerated {len(ip_list)} unique IP addresses")
    print(f"Saved to: {output_file}")
    print("\nDistribution by source:")
    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count} IPs")
    
    return ip_list, ip_sources

def generate_csv_dataset(size=2000, output_file='sample_ip_dataset.csv'):
    """Generate CSV format with additional metadata"""
    import csv
    from datetime import datetime, timedelta
    
    ip_list, ip_sources = generate_sample_dataset(size)
    
    # Generate additional metadata
    categories = ['web_server', 'dns_server', 'mail_server', 'cdn', 'cloud_instance', 
                  'load_balancer', 'database', 'api_endpoint', 'monitoring', 'unknown']
    
    priorities = ['high', 'medium', 'low']
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['ip', 'source_category', 'service_type', 'priority', 'first_seen', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        base_date = datetime.now() - timedelta(days=365)
        
        for i, ip in enumerate(ip_list):
            # Generate realistic first_seen date (within last year)
            days_offset = random.randint(0, 365)
            first_seen = base_date + timedelta(days=days_offset)
            
            writer.writerow({
                'ip': ip,
                'source_category': ip_sources.get(ip, 'unknown'),
                'service_type': random.choice(categories),
                'priority': random.choice(priorities),
                'first_seen': first_seen.strftime('%Y-%m-%d'),
                'notes': f'Sample entry {i+1}'
            })
    
    print(f"CSV dataset saved to: {output_file}")

def main():
    print("IP Dataset Generator")
    print("=" * 40)
    
    # Generate different formats
    print("\n1. Generating plain text IP list...")
    generate_sample_dataset(2000, 'sample_ip_list.txt')
    
    print("\n2. Generating CSV with metadata...")
    generate_csv_dataset(2000, 'sample_ip_dataset.csv')
    
    print("\n3. Generating smaller test dataset...")
    generate_sample_dataset(100, 'test_ip_list.txt')
    
    print("\nDataset generation complete!")
    print("\nFiles created:")
    print("- sample_ip_list.txt (2000 IPs, plain text)")
    print("- sample_ip_dataset.csv (2000 IPs with metadata)")  
    print("- test_ip_list.txt (100 IPs for quick testing)")
    
    print("\nTo use with the ASN analyzer:")
    print("1. Use 'test_ip_list.txt' first to verify everything works")
    print("2. Then use 'sample_ip_list.txt' for full analysis")
    print("3. Modify the analyzer script to load from these files")

if __name__ == "__main__":
    main()
