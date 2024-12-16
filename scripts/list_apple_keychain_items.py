import subprocess
import csv
import re

# Define a function to run `security` commands
def run_security_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Command output: {e.output}")
        return f"Permission Denied: {e}"

# Function to parse output from the `security` command
def parse_security_output(output):
    if "Permission Denied" in output:
        return [{"Error": "Permission Denied"}]
    
    items = []
    current_item = {}
    for line in output.split("\n"):
        if line.strip() == "":
            if current_item:
                items.append(current_item)
                current_item = {}
        else:
            match = re.match(r'^\s*(\S+)\s*:\s*(.*)$', line)
            if match:
                key, value = match.groups()
                current_item[key.strip()] = value.strip()
    if current_item:  # Catch any final entry
        items.append(current_item)
    return items

# Function to list generic passwords from Keychain
def get_generic_passwords():
    output = run_security_command("security find-generic-password -a $(whoami)")
    if output:
        return parse_security_output(output)
    return []

# Function to list internet passwords (like GitHub tokens) from Keychain
def get_internet_passwords():
    output = run_security_command("security find-internet-password -a $(whoami)")
    if output:
        return parse_security_output(output)
    return []

# Function to list all certificates from Keychain
def get_certificates():
    output = run_security_command("security find-certificate -a -p")
    if output:
        return parse_security_output(output)
    return []

# Function to list all SSH identities from Keychain
def get_ssh_identities():
    output = run_security_command("security find-identity -v -p ssh")
    if output:
        return parse_security_output(output)
    return []

# Function to export all Keychain items to CSV
def export_to_csv(filename, items):
    if not items:
        print(f"No items to export for {filename}")
        return

    # Determine all keys from all items to ensure we capture all fields
    keys = set()
    for item in items:
        keys.update(item.keys())
    keys = list(keys)
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for item in items:
            # Write the item as a row, filling missing keys with empty strings
            writer.writerow({key: item.get(key, '') for key in keys})

    print(f"Exported {len(items)} items to {filename}")

# Main function to inventory Keychain
def main():
    print("🔐 Starting Keychain inventory...")

    print("\n📂 Gathering generic passwords...")
    generic_passwords = get_generic_passwords()
    print(f"Found {len(generic_passwords)} generic password entries.")
    export_to_csv("generic_passwords.csv", generic_passwords)

    print("\n🌐 Gathering internet passwords (like GitHub tokens)...")
    internet_passwords = get_internet_passwords()
    print(f"Found {len(internet_passwords)} internet password entries.")
    export_to_csv("internet_passwords.csv", internet_passwords)

    print("\n📜 Gathering certificates...")
    certificates = get_certificates()
    print(f"Found {len(certificates)} certificates.")
    export_to_csv("certificates.csv", certificates)

    print("\n🔑 Gathering SSH identities...")
    ssh_identities = get_ssh_identities()
    print(f"Found {len(ssh_identities)} SSH identities.")
    export_to_csv("ssh_identities.csv", ssh_identities)

    print("\n✅ Keychain inventory complete! Check the CSV files in your working directory.")

if __name__ == "__main__":
    main()
