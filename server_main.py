import requests
import warnings
import csv
from requests.exceptions import SSLError

# List of websites to check
websites = [
    "https://socialwelfare.mn.gov.in/",
    "https://artnculturemanipur.gov.in/",
    "https://ccmanipur.mn.gov.in/en/",
    "https://dcimanipur.gov.in/",
    "https://serimanipur.nic.in/",
    "https://employmentservicemanipur.nic.in",
    "https://manipurgovtpress.nic.in/",
    "https://planningmanipur.gov.in/en/",
    "http://pwdmanipur.nic.in/en/",
    "https://pdsmanipur.nic.in/en/",
    "https://techedu.mn.gov.in/",
    "https://www.manipurtaxes.gov.in/",
    "https://www.tpmanipur.mn.gov.in/",
    "https://wrd.mn.gov.in/en/",
    "https://www.fisheries.mn.gov.in/en/",
    "https://taandhills.mn.gov.in/en/",
    "https://prison.mn.gov.in/en/",
    "https://www.adulteducation.mn.gov.in/en/",
    "https://familywelfare.mn.gov.in/en/",
    "https://dlpi.mn.gov.in/en/",
    "https://horticulture.mn.gov.in/",
    "https://www.phedmanipur.gov.in/",
    "http://www.highereducationmanipur.gov.in/",
    "https://maolkekifoundation.org/en/"
]

def check_website_status(url):
    """
    Checks the status of a website and captures any warnings or errors.

    Parameters:
        url (str): The URL of the website to check.

    Returns:
        tuple: A tuple containing the status code (int or None) and a list of warning/error messages.
    """
    try:
        # Capture all warnings during the request
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")  # Capture all warnings

            # Make the HTTP GET request
            response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds

            # Collect any warnings that were raised
            warning_messages = [str(warning.message) for warning in w]

            return response.status_code, warning_messages

    except SSLError as ssl_error:
        # Handle SSL errors specifically
        return None, ["SSL expired or invalid"] if "certificate has expired" in str(ssl_error) else [str(ssl_error)]

    except requests.exceptions.RequestException as e:
        # If an exception occurs, return None for status code and the exception message as a warning
        return None, [str(e)]

def save_results_to_csv(results, filename='website_status.csv'):
    """
    Saves the website status results to a CSV file.

    Parameters:
        results (list of dict): The list of results to save.
        filename (str): The name of the CSV file.
    """
    # Define CSV headers
    headers = ['URL', 'Status Code', 'Warnings']

    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write each result as a row in the CSV
        for result in results:
            writer.writerow(result)

    print(f"Results have been saved to '{filename}'.")

def main():
    # List to store the results
    results = []

    # Iterate through each website and check its status
    for website in websites:
        status_code, warnings_list = check_website_status(website)

        # Prepare the result dictionary
        result = {
            'URL': website,
            'Status Code': status_code if status_code is not None else 'Failed',
            'Warnings': '; '.join(warnings_list) if warnings_list else ''
        }

        # Append the result to the results list
        results.append(result)

        # Optional: Print the result to the console
        print(f"URL: {result['URL']} - Status Code: {result['Status Code']}")
        if result['Warnings']:
            print(f"  Warnings: {result['Warnings']}")

    # Save all results to a CSV file
    save_results_to_csv(results)

if __name__ == "__main__":
    main()
