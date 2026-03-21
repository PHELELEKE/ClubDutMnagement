#!/usr/bin/env python
import requests
import time

# Wait for server to be ready
time.sleep(1)

session = requests.Session()

# Login
print("Testing leader dashboard rendering...")
response = session.post(
    'http://localhost:5000/login',
    data={'email': 'leader@dut.ac.za', 'password': 'leader@123'},
    allow_redirects=True,
    timeout=5
)
print(f"Login: {response.status_code}")

# Get leader dashboard
response = session.get('http://localhost:5000/dashboard/leader', timeout=5)
print(f"Dashboard: {response.status_code}")

# Check for key elements
checks = {
    'My Clubs': 'My Clubs' in response.text,
    'My Events': 'My Events' in response.text,
    'nav-tabs': 'nav-tabs' in response.text,
    'clubs-tab': 'clubs-tab' in response.text,
    'events-tab': 'events-tab' in response.text,
    'tab-content': 'tab-content' in response.text,
}

print("\n--- Element Presence Check ---")
for check_name, result in checks.items():
    status = '✓' if result else '✗'
    print(f"{status} {check_name}")

# Find where "My Clubs" appears
if 'My Clubs' in response.text:
    idx = response.text.find('My Clubs')
    print(f"\n'My Clubs' found at position {idx}")
    print(f"Context: ...{response.text[max(0, idx-100):idx+100]}...")

# Count occurrences
print(f"\nOccurrences of 'nav-tabs': {response.text.count('nav-tabs')}")
print(f"Occurrences of 'My Clubs': {response.text.count('My Clubs')}")
print(f"Occurrences of 'tab-pane': {response.text.count('tab-pane')}")

# Write to file for inspection
with open('/tmp/dashboard_output.html', 'w') as f:
    f.write(response.text)
print("\nHTML written to /tmp/dashboard_output.html")
