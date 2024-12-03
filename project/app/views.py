from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from .models import UserLogin
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.

class Registreview(View):
    def get(self,request):
        return render(request, 'register.html')
    
    def post(self,request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")


        # chec if email is alred exist
        if UserLogin.objects.filter(email=email).exists():
            messages.error(request,"Email alredy Exist")
            return render(request,"register.html")
        
        # save the user with hashed password
        hashed_password = make_password(password)
        user = UserLogin.objects.create(name=name,email=email, password=hashed_password)
        messages.success(request, f"Account created for {user.name}!")
        return redirect('login')


# Login view
class LoginView(View):
    def get(self,request):
        return render(request,"login.html")
    
    def post(self,request):
        email =  request.POST.get("email")
        password = request.POST.get("password")

        try:
            user =  UserLogin.objects.get(email=email)
            if check_password(password,user.password):

               request.session['user_id'] = user.id
               request.session['user_name'] = user.name
               request.session['email'] = user.email
               request.session.set_expiry(3600)  # Session expires in 1 hour
               messages.success(request, f"Welcome back, {user.name}!")
               return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")

        except UserLogin.DoesNotExist:
            messages.error(request, "User does not exist.")

        return render(request, 'login.html')

class LogoutView(View):
    def get(self, request):
        # Clear session data
        request.session.flush()
        messages.success(request, "You have successfully logged out.")
        return redirect('login')





