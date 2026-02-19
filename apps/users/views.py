
from typing import Any
import logging
# Create your views here.
from rest_framework.viewsets import ViewSet

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.request import Request
from apps.users.serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework import status

logger = logging.getLogger(__name__)


    
    

class AuthViewSet(ViewSet):


    def get_permissions(self):
        if self.action in {"register", "login", "refresh"}:
            return [AllowAny()]
        if self.action in {"me"}:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
       
        if self.action in {"logout", "list"}:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    

    @action(detail=False, methods=["post"], url_path="login")
    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))

    def login(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict,
    ) -> Response:
        email = request.data.get("email")
        logger.info(f"Login attempt with email: {request.data.get('email')}")
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
            
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            logger.info(f"User logged in successfully with email: {user.email}")
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=HTTP_200_OK,
            )
        
        logger.warning(f"Login failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["post"], url_path="register")
    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def register(
        self,
        request: Request,
       
    ) -> Response:
        email = request.data.get("email")
        logger.info(f"Registration attempt with email: {request.data.get('email')}")
        serializer = RegisterSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered successfully with email: {user.email}")
            return Response(
                {
                    "message": "User registered successfully",
                    "user": CustomUserSerializer(user).data,
                },
                status=HTTP_200_OK,
            )
        
        logger.warning(f"Registration failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path="token/refresh")
    
    def refresh(
        self,
        request: Request,
        
    ) -> Response:
        logger.info(f"Token refresh attempt for email: {request.data.get('email')}")
        serializer = TokenRefreshSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken) as e:
            logger.warning(f"Token refresh failed: {str(e)}")
            raise InvalidToken(e)

        logger.info("Token refresh successful")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(
        self,
        request: Request,
        
    ) -> Response:
        logger.info(f"Logout attempt for email: {request.user.email}")
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Logout successful for email: {request.user.email}")
            return Response({"message": "Logout successful"}, status=HTTP_200_OK)
        except Exception as e:
            logger.warning(f"Logout failed with error: {str(e)} for email: {request.user.email}")
            return Response({"error": "Invalid token"}, status=HTTP_400_BAD_REQUEST)
        


    @method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="me")
    @action(detail=False, methods=["get", "patch"], url_path="me",
        permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def me(self, request):
        user = request.user

        if request.method.lower() == "get":
            self.check_object_permissions(request, user)
            return Response(CustomUserSerializer(user).data, status=HTTP_200_OK)

        self.check_object_permissions(request, user)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CustomUserSerializer(serializer.instance).data, status=HTTP_200_OK)
    def list(
            self,           
            request: Request,
        ) -> Response:
            search = request.query_params.get("search")
            queryset = CustomUser.objects.all().order_by("id")
            if search:
                queryset = queryset.filter(
                    Q(email__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )   
            logger.info(f"User list requested by id {request.user.id} with email {request.user.email}")
            return Response(
                CustomUserSerializer(queryset, many=True).data,
                status=HTTP_200_OK,
            )