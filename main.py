import argparse
import getpass
from api_client import GreeApiClient

SERVER_LIST = {
    "Europe": "https://eugrih.gree.com",
    "East South Asia": "https://hkgrih.gree.com",
    "North American": "https://nagrih.gree.com",
    "South American": "https://sagrih.gree.com",
    "China Mainland": "https://grih.gree.com",
    "India": "https://ingrih.gree.com",
    "Middle East": "https://megrih.gree.com",
    "Australia": "https://augrih.gree.com",
    "Russian server": "https://rugrih.gree.com",
}

def main():
    server_info_help = "Base URL for the Gree API. Possible values:\n"
    for name, host in SERVER_LIST.items():
        server_info_help += f"  - {name}: {host}\n"
    
    parser = argparse.ArgumentParser(
        description="Gree API Client for retrieving device information.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help=server_info_help
    )
    parser.add_argument("--username", required=True, help="Your Gree account username.")

    args = parser.parse_args()

    password = getpass.getpass("Enter your Gree account password: ")

    api_client = GreeApiClient(args.url, args.username, password)
    api_client.login()

    print("-----------------------------------")
    print("✅ Login Successful!")
    print(f"User ID: {api_client.user_id}")
    print(f"Token:   {api_client.token}")
    print("-----------------------------------")

    print("\n🏡 Homes Found:")
    homes = api_client.get_homes()
    if homes:
        for home in homes:
            print(f"\n  🏠 **{home['name'].strip()}** (Home ID: {home['id']})")
            print("  - Devices:")
            devices = api_client.get_devices(home["id"])
            if devices:
                for device in devices:
                    print(f"    - Name: {device['name'].strip()}")
                    print(f"      MAC:  {device['mac'].strip()}")
                    print(f"      Key:  {device['key'].strip()}")
            else:
                print("      No devices found in this home.")
    else:
        print("  No homes found for this user.")
    print("\n-----------------------------------")

if __name__ == "__main__":
    main()