#Fun from ZTM Python on Udemy... Added the external file capabilities
import requests
import hashlib
import sys

#call the api to check the paasword
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/'+ query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

#get the hash and the number of times in appears in the database 
def get_password_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0
    
#get the first 5 chars of the hash
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    fisrt5_char, tail =sha1password[:5],sha1password[5:]
    response = request_api_data(fisrt5_char)
    print(fisrt5_char, tail)
    return get_password_leaks_count(response,tail)
    


def main(secret_pass):
    for password in secret_pass:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change it')
        else:
            print(f'{password} was not found... Carry On')
    return "done!"


#Read external file to check passwords 
if __name__ == '__main__':
    fs= open(r'text.txt','r',encoding = 'utf-8')
    password_list = []
    for line in fs.readlines():
        password_list.append(line.rstrip('\n'))
    print(password_list)
    sys.exit(main(password_list))

    fs.close()