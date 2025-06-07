#!/usr/bin/env python3
"""
IP to ASN Mapping and BGP Connection Analysis Tool

This script categorizes IP addresses by their ASN and maps BGP connections.
Requires: pip install pyasn requests networkx matplotlib
"""

import requests
import json
import time
from collections import defaultdict, Counter
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import ip_address, ip_network
import csv

class IPASNAnalyzer:
    def __init__(self):
        self.asn_data = {}
        self.bgp_connections = defaultdict(set)
        
    def get_asn_from_ip_bulk(self, ip_list, method='team_cymru'):
        """
        Get ASN information for multiple IPs using different methods
        """
        results = {}
        
        if method == 'team_cymru':
            results = self._query_team_cymru(ip_list)
        elif method == 'ipapi':
            results = self._query_ipapi(ip_list)
        elif method == 'ipinfo':
            results = self._query_ipinfo(ip_list)
        
        return results
    
    def _query_team_cymru(self, ip_list):
        """Query Team Cymru's ASN lookup service (most reliable, free)"""
        import socket
        results = {}
        
        print("Querying Team Cymru ASN database...")
        for i, ip in enumerate(ip_list):
            if i % 100 == 0:
                print(f"Processed {i}/{len(ip_list)} IPs")
            
            try:
                # Reverse the IP for DNS query
                reversed_ip = '.'.join(reversed(ip.split('.')))
                query = f"{reversed_ip}.origin.asn.cymru.com"
                
                # DNS TXT query
                import subprocess
                result = subprocess.run(['nslookup', '-type=txt', query], 
                                      capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'text =' in line and '|' in line:
                            parts = line.split('"')[1].split('|')
                            if len(parts) >= 3:
                                asn = parts[0].strip()
                                prefix = parts[1].strip()
                                country = parts[2].strip()
                                results[ip] = {
                                    'asn': asn,
                                    'prefix': prefix,
                                    'country': country,
                                    'org': ''
                                }
                                break
            except Exception as e:
                print(f"Error querying {ip}: {e}")
                results[ip] = {'asn': 'Unknown', 'prefix': '', 'country': '', 'org': ''}
        
        return results
    
    def _query_ipapi(self, ip_list):
        """Query ip-api.com (free, rate limited)"""
        results = {}
        batch_size = 100  # ip-api allows batch queries
        
        print("Querying ip-api.com...")
        for i in range(0, len(ip_list), batch_size):
            batch = ip_list[i:i+batch_size]
            
            try:
                response = requests.post('http://ip-api.com/batch', 
                                       json=batch,
                                       headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    data = response.json()
                    for j, item in enumerate(data):
                        ip = batch[j]
                        if item['status'] == 'success':
                            results[ip] = {
                                'asn': item.get('as', '').split()[0].replace('AS', ''),
                                'org': item.get('as', '').split(' ', 1)[1] if ' ' in item.get('as', '') else '',
                                'country': item.get('countryCode', ''),
                                'prefix': ''
                            }
                        else:
                            results[ip] = {'asn': 'Unknown', 'prefix': '', 'country': '', 'org': ''}
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in batch query: {e}")
        
        return results
    
    def get_asn_info(self, asn):
        """Get detailed ASN information"""
        try:
            # Query RIPE NCC for ASN info
            url = f"https://stat.ripe.net/data/as-overview/data.json?resource=AS{asn}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    'asn': asn,
                    'holder': data['data']['holder'],
                    'block': data['data']['block'],
                    'announced': data['data']['announced']
                }
        except:
            pass
        
        return {'asn': asn, 'holder': 'Unknown', 'block': {}, 'announced': True}
    
    def get_bgp_neighbors(self, asn):
        """Get BGP neighbors/peers for an ASN"""
        try:
            # Query RIPE NCC for BGP data
            url = f"https://stat.ripe.net/data/asn-neighbours/data.json?resource=AS{asn}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                neighbors = []
                for neighbor in data['data']['neighbours']:
                    neighbors.append({
                        'asn': neighbor['asn'],
                        'type': neighbor['type'],  # left/right/uncertain
                        'power': neighbor.get('power', 0)
                    })
                return neighbors
        except Exception as e:
            print(f"Error getting BGP neighbors for AS{asn}: {e}")
        
        return []
    
    def analyze_ips(self, ip_list, output_file='ip_asn_analysis.csv'):
        """Main analysis function"""
        print(f"Starting analysis of {len(ip_list)} IP addresses...")
        
        # Get ASN data for all IPs
        asn_results = self.get_asn_from_ip_bulk(ip_list)
        
        # Categorize by ASN
        asn_groups = defaultdict(list)
        for ip, data in asn_results.items():
            asn = data['asn']
            if asn and asn != 'Unknown':
                asn_groups[asn].append(ip)
        
        print(f"\nFound {len(asn_groups)} unique ASNs")
        
        # Get detailed ASN information
        asn_details = {}
        for asn in asn_groups.keys():
            print(f"Getting details for AS{asn}...")
            asn_details[asn] = self.get_asn_info(asn)
            time.sleep(0.5)  # Rate limiting
        
        # Write results to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ip', 'asn', 'asn_holder', 'country', 'org', 'ip_count_in_asn']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for ip, data in asn_results.items():
                asn = data['asn']
                holder = asn_details.get(asn, {}).get('holder', 'Unknown')
                writer.writerow({
                    'ip': ip,
                    'asn': asn,
                    'asn_holder': holder,
                    'country': data.get('country', ''),
                    'org': data.get('org', ''),
                    'ip_count_in_asn': len(asn_groups.get(asn, []))
                })
        
        print(f"Results written to {output_file}")
        
        # Print summary
        print("\n=== ASN Summary ===")
        asn_counts = Counter()
        for asn, ips in asn_groups.items():
            asn_counts[asn] = len(ips)
        
        for asn, count in asn_counts.most_common(10):
            holder = asn_details.get(asn, {}).get('holder', 'Unknown')
            print(f"AS{asn}: {count} IPs - {holder}")
        
        return asn_groups, asn_details
    
    def build_bgp_graph(self, asn_list, max_depth=1):
        """Build BGP connection graph"""
        print(f"\nBuilding BGP graph for {len(asn_list)} ASNs...")
        
        G = nx.Graph()
        processed = set()
        
        for asn in asn_list:
            if asn in processed or asn == 'Unknown':
                continue
                
            print(f"Getting BGP neighbors for AS{asn}...")
            neighbors = self.get_bgp_neighbors(asn)
            
            # Add nodes
            G.add_node(asn)
            
            # Add edges to neighbors
            for neighbor in neighbors:
                neighbor_asn = neighbor['asn']
                G.add_node(neighbor_asn)
                G.add_edge(asn, neighbor_asn, 
                          type=neighbor['type'], 
                          power=neighbor.get('power', 0))
            
            processed.add(asn)
            time.sleep(0.5)  # Rate limiting
        
        return G
    
    def visualize_bgp_graph(self, G, output_file='bgp_graph.png'):
        """Visualize BGP connections"""
        if len(G.nodes()) == 0:
            print("No BGP data to visualize")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=500, alpha=0.7)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=0.5)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.title("BGP ASN Connections")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"BGP graph saved to {output_file}")

def main():
    # Example usage
    analyzer = IPASNAnalyzer()
    
    # Sample IP list (replace with your 2000+ IPs)
    sample_ips = [
        '8.8.8.8',
        '1.1.1.1', 
        '208.67.222.222',
        '9.9.9.9',
        '76.76.19.19'
    ]
    
    # Read IPs from file
    # with open('ip_list.txt', 'r') as f:
    #     ip_list = [line.strip() for line in f if line.strip()]
    
    # Analyze IPs
    asn_groups, asn_details = analyzer.analyze_ips(sample_ips)
    
    # Build and visualize BGP graph
    asn_list = list(asn_groups.keys())
    bgp_graph = analyzer.build_bgp_graph(asn_list)
    analyzer.visualize_bgp_graph(bgp_graph)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
