from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login, decorators
from .forms import MyUserForm
from .models.models import MyUser
#fix login when have account
from django.contrib.auth.models import auth


# Create your views here.
class LoginView(View):
    def get(self, request):
        f = MyUserForm()
        return render(request, 'homepage/base_login.html', {'f':f})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '' or password == '':
            error_message = 'Vui lòng nhập đủ thông tin!'
            context={'username':username, 'error_message':error_message}
            return render(request, 'homepage/base_login.html', context)
        #user = authenticate(username=username, password = password)
        try:
            user = MyUser.objects.get(username=username, password=password)
        except:
            error_message = 'Tài khoản không tồn tại!'
            context={'username':username, 'error_message':error_message}
            return render(request, 'homepage/base_login.html', context)
        #login(request,user)
        request.session['username'] = user.username
        request.session['id'] = user.id
        
        return redirect('/')

class RegisterView(View):
    def post(self, request):
        user = MyUserForm(request.POST)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if password != confirm_password:
            error_message = 'Xác nhận mật khẩu không khớp!'
            context={'error_message_2':error_message, 'f':user}
            return render(request, 'homepage/base_login.html', context)
        if not user.is_valid():
            error_message = 'Dữ liệu chưa hợp lệ!'
            context={'error_message_2':error_message, 'f':user}
            return render(request, 'homepage/base_login.html', context)
        user.save()
        
        error_message = 'Tạo tài khoản thành công!'
        user = MyUserForm()
        context={'error_message_2':error_message, 'f':user}
        return render(request, 'homepage/base_login.html', context)

class LogoutView(View):
    def get(self, request):
        username = request.session['username']
        error_message = 'Đăng xuất thành công!'
        f = MyUserForm()
        context={'username':username, 'error_message':error_message, 'f':f}
        #xóa session
        del request.session['username']
        del request.session['id']

        return render(request, 'homepage/base_login.html', context)

class AccountView(View):
    def get(self, request):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        f = MyUserForm()
        f.fields['email'].initial = user.email
        f.fields['first_name'].initial = user.first_name
        f.fields['last_name'].initial = user.last_name
        f.fields['birth'].initial = user.birth
        f.fields['sex'].initial = user.sex
        f.fields['address'].initial = user.address
        return render(request, 'homepage/account.html', {'f':f})
    def post(self, request):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        user_form = MyUserForm(request.POST)
        user.email = user_form.data['email']
        user.first_name = user_form.data['first_name']
        user.last_name = user_form.data['last_name']
        user.sex = user_form.data['sex']
        user.birth = user_form.data['birth']
        user.address = user_form.data['address']

        user.save()
        #return redirect('/')
        error_message_2 = "Cập nhật thông tin tài khoản thành công!"
        return render(request, 'homepage/account.html', {'f':user_form, 'error_message_2':error_message_2})
    
class ChangePassword(View):
    def get(self, request):
        return render(request, 'homepage/change_password.html')
    def post(self, request):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        password = request.POST.get('password')
        password_new = request.POST.get('password_new')
        password_confirm = request.POST.get('password_confirm')

        if password != user.password:
            error_message = 'Mật khẩu chưa chính xác!'
            context={'error_message_2':error_message}
            return render(request, 'homepage/change_password.html', context)
        if password_new != password_confirm:
            error_message = 'Mật khẩu xác nhận chưa chính xác!'
            context={'error_message_2':error_message}
            return render(request, 'homepage/change_password.html', context)

        user.password = password_new
        user.save()
        
        error_message_2 = "Thay đổi mật khẩu thành công!"
        context={'error_message_2':error_message_2}
        return render(request, 'homepage/change_password.html', context)