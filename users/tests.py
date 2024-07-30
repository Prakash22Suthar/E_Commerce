from rest_framework.test import APIClient

client = APIClient()

response = client.get("api/users/", data = {}, format="json")


# response = client.login(username='naveen2@yopmail.com', password='Demo@123')

assert response.status_code == 200
print(":::::::", response)


