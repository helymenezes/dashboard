from msal import ConfidentialClientApplication

app = ConfidentialClientApplication(
    client_id='374b3759-a544-4335-8377-b0dc85f30ca1',
    authority='https://login.microsoftonline.com/me',
    client_credential='3b08e64e-b3be-402b-bb26-1fa4f91cf61f',
)

token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
access_token = token_response['access_token']
