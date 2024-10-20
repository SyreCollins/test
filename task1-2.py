# Task 1
import json

def validate_and_assign_serial_numbers(json_data):
    # Define the allowed range of serial numbers
    serial_range = ["C25CTW00000000001470", "C25CTW00000000001471", "C25CTW00000000001472",
                    "C25CTW00000000001473", "C25CTW00000000001474", "C25CTW00000000001475",
                    "C25CTW00000000001476", "C25CTW00000000001477", "C25CTW00000000001478"]

    # Reverse the serial number order (for mn1 to mn8)
    reversed_serials = serial_range[1:].copy()  # Skip the first one (1470) since men1 keeps it
    reversed_serials.reverse()  # Assign in reverse order for mn1 to mn8

    # Validate the schema (basic validation for 'Internet_hubs' key existence)
    if 'Internet_hubs' not in json_data:
        raise ValueError("Invalid JSON schema: 'Internet_hubs' key is missing.")

    hubs = json_data['Internet_hubs']

    # Track the assignment for mn1 to mn9
    index = 0  # For assigning reversed serials

    for hub in hubs:
        hub_id = hub.get('id')
        if hub_id == 'men1':
            # men1 keeps its original serial number (1470)
            hub['serial_number'] = serial_range[0]
        elif hub_id.startswith('mn') and hub_id != 'mn9':
            # Assign reversed serial numbers for mn1 to mn8
            hub['serial_number'] = reversed_serials[index]
            index += 1
        elif hub_id == 'mn9':
            # Assign the second lowest serial number (1471) to mn9
            hub['serial_number'] = serial_range[1]

    return json_data


json_input = {
    "comment": "Do NOT commit local changes to this file to source control",
    "Internet_hubs": [
        {"id": "men1", "serial_number": "C25CTW00000000001470"},
        {"id": "mn1", "serial_number": "<serial number here>"},
        {"id": "mn2", "serial_number": "<serial number here>"},
        {"id": "mn3", "serial_number": "<serial number here>"},
        {"id": "mn4", "serial_number": "<serial number here>"},
        {"id": "mn5", "serial_number": "<serial number here>"},
        {"id": "mn6", "serial_number": "<serial number here>"},
        {"id": "mn7", "serial_number": "<serial number here>"},
        {"id": "mn8", "serial_number": "<serial number here>"},
        {"id": "mn9", "serial_number": "<serial number here>"}
    ]
}

# Execute the function
updated_json = validate_and_assign_serial_numbers(json_input)
#print(json.dumps(updated_json, indent=4))

# Task 2
import requests
import csv


def fetch_customer_numbers(api_key):
    url = "https://pysoftware.com/v1/customer_numbers"
    headers = {'X-API-KEY': api_key}
    response = requests.get(url, headers=headers)
    return response.json()


def fetch_customer_address(customer_number, api_key):
    url = f"https://pysoftware.com/v1/address_inventory/{customer_number}"
    headers = {'X-API-KEY': api_key}
    response = requests.get(url, headers=headers)
    return response.json()


def clean_and_validate_address(address):
    if 'postcode' not in address or address['postcode'] == "":
        address['postcode'] = 'Unknown'
    return address


def save_to_csv(addresses, filename):
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(addresses)
    return filename


def get_all_addresses_and_save(api_key):
    # Retrieve customer numbers
    customer_numbers = fetch_customer_numbers(api_key)

    all_addresses = []
    for customer_number in range(1, customer_numbers + 1):
        address = fetch_customer_address(customer_number, api_key)
        cleaned_address = clean_and_validate_address(address)
        all_addresses.append(cleaned_address)

    # Save addresses to CSV
    csv_filename = 'customer_addresses.csv'
    save_to_csv(all_addresses, csv_filename)

    # Return file name and path
    print(f"CSV file saved at: {csv_filename}")

    return all_addresses


api_key = "ssfdsjfksjdhfgjfgvjdshgvshgkjsdlgvkjsdgjkl"
all_addresses = get_all_addresses_and_save(api_key)
for address in all_addresses:
    print(address)
