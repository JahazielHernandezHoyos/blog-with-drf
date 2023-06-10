# import firebase_admin
# from firebase_admin import credentials, messaging

# # cred = credentials.Certificate("firebase.json")
# firebase_app = firebase_admin.initialize_app(cred)


# def send_notification_push(message, token):
#     message = messaging.Message(
#         notification=messaging.Notification(title="Test", body=message),
#         token=token,
#     )
#     messaging.send(message)
#     return True
