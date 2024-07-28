import urllib.request

request = urllib.request.Request(url="http://127.0.0.1:8000/splittime")
response = urllib.request.urlopen(request)

print(response.status)
print(response.url)

delete_request = urllib.request.Request(url="http://127.0.0.1:8000/splittime/group/1/delete_group")
delete_response = urllib.request.urlopen(delete_request)

print(delete_response.status)
print(delete_response.url)

add_request = urllib.request.Request(url="http://127.0.0.1:8000/splittime/add_group")
add_response = urllib.request.urlopen(add_request)

print(add_response.status)
print(add_response.url)