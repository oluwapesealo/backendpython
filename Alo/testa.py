import requests
 
downloadurl =  'https://binaries.templates.cdn.office.net/support/templates/en-us/tf16402488_win32.dotx'

req = requests.get(downloadurl)

filename = req.url[downloadurl.rfind('/')+1:]

with open(filename, 'wb') as f:
    for chunk in req.iter_content(chunk_size =8192):
        if chunk:
            f.write(chunk)