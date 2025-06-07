# IPscape: Map the Internet's Landscape

IPscape provides a comprehensive toolkit for **IP-to-ASN mapping** and **BGP analysis** needs. It helps you uncover the intricate relationships between IP addresses and Autonomous Systems (ASNs), visualize BGP routing paths, and explore the interconnected fabric of the global internet.

## Key Features

### Main Components

* **IP-to-ASN Mapping:** Uses multiple reliable data sources including Team Cymru, ip-api.com, or ipinfo.io to accurately map IP addresses to their respective ASNs.
* **ASN Information Retrieval:** Fetches detailed ASN holder information directly from RIPE NCC.
* **BGP Neighbor Discovery:** Identifies and maps BGP connections between different ASNs.
* **Visualization:** Generates insightful network graphs that visually represent complex BGP relationships.
* **Export:** Allows you to save all results to a CSV file for further analysis or reporting.

---

## Getting Started

### Key Libraries Needed

Before you begin, make sure you have the necessary Python libraries installed. You can install them using pip:

```bash
pip install requests networkx matplotlib ipaddress
```

### Usage

Input your IP list: You can either modify the sample_ips list within the script or uncomment the file reading section to load IP addresses from a text file.
Run the analysis: Execute the script, and it will automatically categorize all IPs by their associated ASNs.
Get results: Upon completion, you'll receive a CSV file containing detailed mapping information and a visual BGP graph illustrating network relationships.
Alternative Lightweight Approach
If your primary focus is solely on fast ASN mapping and you prefer an offline solution, consider using the pyasn library:

Python
```pip install pyasn```

You'll need to download a BGP data file first. Once downloaded, pyasn can provide fast offline lookups without needing external API calls.

### Important Notes
* The script includes automatic rate limiting and provides progress updates, making it suitable for processing large lists of IP addresses.
* The BGP mapping feature is especially valuable for understanding network relationships, identifying potential attack vectors, or analyzing traffic patterns.


# IP-to-ASN Analysis Tool - Installation and Usage Guide

## Prerequisites

- Python 3.7 or higher
- Internet connection for ASN/BGP data queries
- Administrative privileges (for some installations)

## Step 1: Environment Setup

### Option A: Using Virtual Environment (Recommended)
```bash
# Create a new virtual environment
python -m venv ip-asn-env

# Activate the virtual environment
# On Windows:
ip-asn-env\Scripts\activate
# On macOS/Linux:
source ip-asn-env/bin/activate
```

### Option B: System-wide Installation
Skip virtual environment setup and install packages globally (not recommended for production systems).

## Step 2: Install Required Dependencies

```bash
# Install core Python packages
pip install requests networkx matplotlib

# For DNS queries (if not already available)
# On Ubuntu/Debian:
sudo apt-get install dnsutils
# On macOS (if using Homebrew):
brew install bind
# On Windows: Usually included with system
```

## Step 3: Download and Setup the Tool

1. **Save the Script**
   - Copy the Python code to a file named `ip_asn_analyzer.py`
   - Make it executable: `chmod +x ip_asn_analyzer.py` (Linux/macOS)

2. **Create Input Directory Structure**
   ```bash
   mkdir ip-analysis-project
   cd ip-analysis-project
   # Place ip_asn_analyzer.py here
   ```

## Step 4: Prepare Your IP Address List

### Format 1: Text File (Recommended for 2000+ IPs)
Create a file named `ip_list.txt` with one IP per line:
```
8.8.8.8
1.1.1.1
208.67.222.222
192.168.1.1
10.0.0.1
```

### Format 2: CSV File
Create `ip_list.csv` if you have additional metadata:
```csv
ip,description,source
8.8.8.8,Google DNS,public
1.1.1.1,Cloudflare DNS,public
192.168.1.1,Internal Gateway,internal
```

## Step 5: Modify the Script for Your Data

Edit `ip_asn_analyzer.py` and replace the sample data loading section:

### For Text File Input:
```python
def load_ips_from_file(filename='ip_list.txt'):
    """Load IP addresses from text file"""
    try:
        with open(filename, 'r') as f:
            ip_list = []
            for line_num, line in enumerate(f, 1):
                ip = line.strip()
                if ip and not ip.startswith('#'):  # Skip empty lines and comments
                    try:
                        # Validate IP format
                        ip_address(ip)
                        ip_list.append(ip)
                    except ValueError:
                        print(f"Warning: Invalid IP at line {line_num}: {ip}")
            return ip_list
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []

# Replace the main() function's sample_ips section with:
ip_list = load_ips_from_file('ip_list.txt')
if not ip_list:
    print("No valid IPs found. Exiting.")
    return
```

### For CSV File Input:
```python
import csv

def load_ips_from_csv(filename='ip_list.csv'):
    """Load IP addresses from CSV file"""
    ip_list = []
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ip = row['ip'].strip()
                if ip:
                    try:
                        ip_address(ip)
                        ip_list.append(ip)
                    except ValueError:
                        print(f"Warning: Invalid IP: {ip}")
        return ip_list
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
```

## Step 6: Running the Analysis

### Basic Execution
```bash
# Make sure your virtual environment is activated
python ip_asn_analyzer.py
```

### Advanced Configuration Options

You can modify these parameters in the script:

```python
# In the main() function, customize these settings:

# Choose ASN lookup method
asn_results = analyzer.get_asn_from_ip_bulk(ip_list, method='team_cymru')
# Options: 'team_cymru' (most reliable), 'ipapi' (faster), 'ipinfo'

# Customize output files
analyzer.analyze_ips(ip_list, output_file='my_results.csv')

# Control BGP graph depth
bgp_graph = analyzer.build_bgp_graph(asn_list, max_depth=1)
# max_depth=1: direct neighbors only
# max_depth=2: neighbors of neighbors (warning: much larger graph)

# Customize visualization
analyzer.visualize_bgp_graph(bgp_graph, output_file='my_bgp_graph.png')
```

## Step 7: Understanding the Output

### CSV Output File (`ip_asn_analysis.csv`)
```csv
ip,asn,asn_holder,country,org,ip_count_in_asn
8.8.8.8,15169,Google LLC,US,Google LLC,1
1.1.1.1,13335,Cloudflare Inc,US,Cloudflare Inc,1
```

**Columns Explained:**
- `ip`: Original IP address
- `asn`: Autonomous System Number
- `asn_holder`: Organization that owns the ASN
- `country`: Country code
- `org`: Organization name from IP geolocation
- `ip_count_in_asn`: How many of your IPs belong to this ASN

### BGP Graph (`bgp_graph.png`)
- Visual network showing ASN interconnections
- Nodes represent ASNs
- Edges represent BGP peering relationships

### Console Output
- Progress updates during processing
- Top 10 ASNs by IP count
- Error messages for failed lookups

## Step 8: Performance Optimization for Large Datasets

### For 2000+ IPs:

1. **Use Team Cymru Method** (most reliable, but slower)
2. **Enable Batch Processing**:
   ```python
   # Process in chunks to avoid timeouts
   def process_large_ip_list(ip_list, chunk_size=500):
       all_results = {}
       for i in range(0, len(ip_list), chunk_size):
           chunk = ip_list[i:i+chunk_size]
           print(f"Processing chunk {i//chunk_size + 1}/{(len(ip_list)-1)//chunk_size + 1}")
           results = analyzer.get_asn_from_ip_bulk(chunk)
           all_results.update(results)
           time.sleep(2)  # Rate limiting between chunks
       return all_results
   ```

3. **Save Intermediate Results**:
   ```python
   import pickle
   
   # Save results to avoid re-processing
   with open('asn_cache.pkl', 'wb') as f:
       pickle.dump(asn_results, f)
   
   # Load cached results
   try:
       with open('asn_cache.pkl', 'rb') as f:
           asn_results = pickle.load(f)
   except FileNotFoundError:
       # Run fresh analysis
       pass
   ```

## Step 9: Troubleshooting Common Issues

### DNS Resolution Errors
```bash
# Test DNS resolution
nslookup 8.8.8.8.origin.asn.cymru.com

# If failing, try alternative DNS servers
# Add to script:
import socket
socket.setdefaulttimeout(10)
```

### Rate Limiting Issues
- Team Cymru: No official rate limits, but be respectful
- ip-api.com: 1000 requests/month free, 45 requests/minute
- Add delays between requests if getting blocked

### Memory Issues with Large Datasets
```python
# Process in smaller batches
batch_size = 100  # Reduce if memory issues persist
```

### Missing BGP Data
Some ASNs may not have public BGP data available. This is normal.

## Step 10: Advanced Usage Examples

### Generate Summary Report
```python
def generate_summary_report(asn_groups, asn_details):
    """Generate a summary report"""
    with open('asn_summary.txt', 'w') as f:
        f.write("ASN Analysis Summary\n")
        f.write("=" * 50 + "\n\n")
        
        total_ips = sum(len(ips) for ips in asn_groups.values())
        f.write(f"Total IPs analyzed: {total_ips}\n")
        f.write(f"Unique ASNs found: {len(asn_groups)}\n\n")
        
        f.write("Top ASNs by IP count:\n")
        for asn, ips in sorted(asn_groups.items(), 
                              key=lambda x: len(x[1]), reverse=True)[:10]:
            holder = asn_details.get(asn, {}).get('holder', 'Unknown')
            f.write(f"AS{asn}: {len(ips)} IPs - {holder}\n")
```

### Filter by Country or Organization
```python
def filter_by_country(asn_results, country_code='US'):
    """Filter results by country"""
    filtered = {ip: data for ip, data in asn_results.items() 
                if data.get('country') == country_code}
    return filtered
```

## Step 11: Cleanup

```bash
# Deactivate virtual environment when done
deactivate

# Remove virtual environment (if needed)
rm -rf ip-asn-env  # Linux/macOS
rmdir /s ip-asn-env  # Windows
```

## Expected Runtime

- **2000 IPs with Team Cymru**: ~30-45 minutes
- **2000 IPs with ip-api**: ~5-10 minutes (with rate limiting)
- **BGP graph generation**: ~5-10 minutes additional

## Support and Next Steps

1. **Monitor the console output** for progress and errors
2. **Check the CSV file** for your primary results
3. **Review the BGP graph** for network relationship insights
4. **Consider integrating** results with other security tools or databases

The tool is designed to handle interruptions gracefully - you can stop and restart the analysis as needed.
