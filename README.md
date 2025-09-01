# Gree API Client
This is a Python client for the Gree API, designed to help you retrieve information about your connected Gree and Cooper & Hunter devices.

- [Gree+ Android App](https://play.google.com/store/apps/details?id=com.gree.greeplus)
- [Gree+ iOS App](https://apps.apple.com/app/gree/id1167857672)
- [EWPE Smart Android App](https://play.google.com/store/apps/details?id=com.gree.ewpesmart)
- [EWPE Smart iOS App](https://apps.apple.com/app/ewpe-smart/id1189467454)

## Installation
To get started, clone this repository to your local machine:

```shell
git clone https://github.com/luc10/gree-api-client.git
cd gree-api-client
pip3 install -r requirements.txt

```

## Usage
This script requires you to provide the API URL for your server and your Gree account credentials.

To find your API URL, refer to the list of servers and their corresponding URLs. You must provide one of these URLs as a command-line argument.

The script will prompt you for your password after you run the command.

```shell
python main.py --url [your_api_url] --username [your_gree_username]

```

**Example:**

For the Europe server, the command would be:

```shell
python main.py --url https://eugrih.gree.com --username mygreeaccount@example.com
```

### Server List
Here is the list of available API hosts for different servers. You **must** provide one of these with the `--url` argument.

| Server Name | API Host | 
 | ----- | ----- | 
| Europe | `https://eugrih.gree.com` | 
| East South Asia | `https://hkgrih.gree.com` | 
| North American | `https://nagrih.gree.com` | 
| South American | `https://sagrih.gree.com` | 
| China Mainland | `https://grih.gree.com` | 
| India | `https://ingrih.gree.com` | 
| Middle East | `https://megrih.gree.com` | 
| Australia | `https://augrih.gree.com` | 
| Russian server | `https://rugrih.gree.com` | 

## Author
* **luc10** - [Link to luc10's GitHub profile](https://github.com/luc10)
