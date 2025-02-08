from django.shortcuts import render , redirect , get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model , authenticate, login , update_session_auth_hash , logout
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth.forms import PasswordChangeForm
import logging
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator


class UserListView(generics.ListCreateAPIView):
    """
    List and create users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users can access this view


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only Admin users can access this view


class LoginView(APIView):
    """
    View for login and getting JWT tokens.
    """

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = get_user_model().objects.filter(email=email).first()
        
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response({"detail": "Invalid credentials"}, status=400)



@login_required
def user_panel(request):
    query = request.GET.get("q")
    users = CustomUser.objects.all()  # دریافت لیست کاربران
    paginator = Paginator(users, 10)  # 10 کاربر در هر صفحه
    page_number = request.GET.get('page')  # صفحه مورد نظر از درخواست
    page_obj = paginator.get_page(page_number)  # دریافت داده‌های صفحه مشخص


    if query:
        users = users.filter(email__icontains=query)  # جستجو بر اساس ایمیل 
  
    return render(request, 'users/panel.html', {'users': users})



# Initialize logger
logger = logging.getLogger('users')  # 'users' should match the logger name in settings.py

@swagger_auto_schema(method='post', operation_description="User login POST method")
@swagger_auto_schema(method='get', operation_description="User login GET method")
@api_view(['POST', 'GET'])
def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Log successful login
            logger.info(f"User '{user.email}' logged in successfully.")
            return redirect("user-panel")  # بعد از لاگین، به پنل منتقل می‌شود
        else:
            # Log failed login attempt
            logger.warning(f"Failed login attempt for email: {email}.")
            messages.error(request, "Invalid email or password.")

    return render(request, "users/login.html")


@swagger_auto_schema(method='post', operation_description="User login POST method")
@swagger_auto_schema(method='get', operation_description="User login GET method")
@api_view(['POST', 'GET'])
def logout_view(request):
    logout(request)  # خروج از سیستم
    return redirect('user-login')  # هدایت به صفحه لاگین




# Initialize logger
logger = logging.getLogger('users')  # 'users' should match the logger name in settings.py

@swagger_auto_schema(method='post', operation_description="User login POST method")
@swagger_auto_schema(method='get', operation_description="User login GET method")
@api_view(['POST', 'GET'])
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.user.is_admin:  # فقط Admin می‌تواند کاربر حذف کند
        user.delete()
        # Log the user deletion
        logger.info(f"User with ID {user_id} has been deleted by {request.user.email}.")
    else:
        # Log failed deletion attempt
        logger.warning(f"Failed deletion attempt for user ID {user_id} by non-admin user {request.user.email}.")

    return redirect("user-panel")  # بعد از حذف، به پنل برمی‌گردد



# Initialize logger
logger = logging.getLogger('users')  # 'users' should match the logger name in settings.py

@swagger_auto_schema(method='post', operation_description="User login POST method")
@swagger_auto_schema(method='get', operation_description="User login GET method")
@api_view(['POST', 'GET'])
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # ذخیره اطلاعات جدید کاربر
            # Log successful edit
            logger.info(f"User {user.email} details updated successfully.")
            return redirect("user-panel")  # بعد از ذخیره، به پنل برمی‌گردیم
        else:
            # Log failed edit attempt
            logger.warning(f"Failed to update user {user.email}. Invalid form data.")
    else:
        form = CustomUserForm(instance=user)  # برای نمایش فرم ویرایش با اطلاعات کاربر

    return render(request, "users/edit_user.html", {"form": form, "user": user})




@login_required
def change_password_admin(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Only admin can change other users' passwords
    if not request.user.is_admin:
        return redirect("user-panel")

    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "The password has been successfully changed.")
            return redirect("user-panel")
    else:
        form = PasswordChangeForm(user)

    return render(request, "users/change_password.html", {"form": form, "is_admin": True})


@login_required
def change_password_user(request):
    user = request.user  # Regular users can only change their own password

    if request.method == "POST":
        new_password = request.POST.get("new_password1")
        user.set_password(new_password)
        user.save()
        login(request, user)
        messages.success(request, "The password has been successfully changed.")
        return redirect("user-panel")

    return render(request, "users/change_password.html", {"is_admin": False})





