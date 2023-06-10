import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from apps.account.models import SMSHistory
from apps.config.models import Config
from apps.utils.shortcuts import get_object_or_none


class Twilio:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.messaging_service_sid = os.getenv("TWILIO_MESSAGING_SERVICE_SID")
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, phone: str, body: str, user_id: int = None) -> None:
        try:
            message = self.client.messages.create(
                phone, messaging_service_sid=self.messaging_service_sid, body=body
            )
        except TwilioRestException as e:

            class Object:
                def __init__(self, sid):
                    self.sid = sid

            message = Object(e.msg)
        config = Config.objects.first()
        if config.save_sms_history and user_id and user_id:
            sms_history = get_object_or_none(SMSHistory, account=user_id)
            if sms_history:
                sms_history.sids = f"{message.sid},{sms_history.sids}"
                sms_history.count += 1
                sms_history.save()
            else:
                sms_history = SMSHistory.objects.create(
                    account_id=user_id, sids=message.sid, count=1
                )

    def fetch_sms(self, sid: str) -> dict:
        message = self.client.messages(sid).fetch()
        return message.__dict__


twilio = Twilio()
