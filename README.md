# IPscape: Map the Internet's Landscape

IPscape provides a comprehensive toolkit for **IP-to-ASN mapping** and **BGP analysis** needs. It helps you uncover the intricate relationships between IP addresses and Autonomous Systems (ASNs), visualize BGP routing paths, and explore the interconnected fabric of the global internet.

---

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
