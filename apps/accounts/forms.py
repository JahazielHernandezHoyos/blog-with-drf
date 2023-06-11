from django import forms

from .models import Account


# class AccountAdminForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = (
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "validation_code",
#             "birthdate",
#             "id_document",
#             "gender",
#             "front_id_image",
#             "back_id_image",
#             "points",
#             "work_time",
#             "work_time_end",
#             "work_code",
#             "permissions",
#             "notes",
#             "status",
#             "role",
#             "deleted",
#             "reset_password_code",
#             "raw_password",
#             "token_mobile_push",
#         )
