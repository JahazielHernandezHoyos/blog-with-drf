from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Account, Category, Comments, Entrace, Tags
from apps.accounts.serializers import (
    AccountRegisterSerializer,
    AccountSerializer,
    UserLoginSerializer,
    BaseSerializer,
    CommentsSerializer,
    EntranceSerializer,
)
from apps.utils.permissions import IsAccount, IsRegisterEnabled
from apps.utils.viewsets import BaseViewSet, PrivateModelViewSet, CrudModelViewSet


class AccountRegisterViewSet(viewsets.GenericViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(deleted=False)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny, IsRegisterEnabled],
        serializer_class=AccountRegisterSerializer,
    )
    def register(self, request):
        account_serializer = self.serializer_class(data=request.data)
        if account_serializer.is_valid(raise_exception=True):
            account_serializer.save()
            return Response(account_serializer.data)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def update_login_data(data):
            data = data.copy()
            data["email"] = data.get("username", "")
            data["password"] = data.get("raw_password", "")
            return data

        login_data = update_login_data(request.data)
        login_serializer = UserLoginSerializer(data=login_data)
        if login_serializer.is_valid(raise_exception=True):
            user, token = login_serializer.save()
            return Response({"user": user, "token": token})
        return Response(account_serializer.data)


class AccountAuthViewSet(viewsets.GenericViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        serializer_class=UserLoginSerializer,
    )
    def login(self, request):
        """User sign in."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        user["profile_picture"] = request.build_absolute_uri(user["profile_picture"])
        return Response({"user": user, "token": token})

    @action(detail=False, permission_classes=[IsAuthenticated], methods=["GET"])
    def detail_user(self, request):
        serializer = self.serializer_class(request.user.account)
        data = serializer.data
        data["profile_picture"] = request.build_absolute_uri(data["profile_picture"])
        return Response(data)

    @action(detail=False, permission_classes=[IsAuthenticated], methods=["PATCH"])
    def update_user(self, request):
        serializer = self.serializer_class(request.user.account, request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        request.user.auth_token.delete()
        request.user.token_mobile_push = ""
        return Response({"success": True})

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def delete_account(self, request):
        request.user.account.logical_erase()
        return Response({"success": True})
        
    @action(
        detail=False,
        methods=["DELETE"],
        permission_classes=[IsAuthenticated],
    )
    def delete_user(self, request):
        user = request.user.account
        user.delete()
        return Response({"success": True})

class TagsViewSet(CrudModelViewSet):
    serializer_class = BaseSerializer
    model = Tags
    queryset = Tags.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user.account)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

class CategoryViewSet(CrudModelViewSet):
    serializer_class = BaseSerializer
    model = Category
    queryset = Category.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user.account)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

class CommentsViewSet(CrudModelViewSet):
    serializer_class = CommentsSerializer
    model = Comments
    queryset = Comments.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user.account)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

class EntranceViewSet(CrudModelViewSet):
    serializer_class = EntranceSerializer
    model = Entrace
    queryset = Entrace.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user.account)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)
