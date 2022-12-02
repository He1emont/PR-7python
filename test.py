import base64

path_on_server = "test/test1.jpg"
with open(path_on_server, 'rb') as file:
    data = file.read()
print(type(data))

print()

data = base64.b64encode(data)
print(type(data))
print()

data = data.decode()
print(type(data))

print()

data = base64.b64decode(data)
print(type(data))

print()

# data = data.encode()
# print(data)
# print()

path_on_client = "test/test2.jpg"
with open(path_on_client, 'wb') as file:
    file.write(data)