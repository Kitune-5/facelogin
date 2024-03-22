
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from profiles.utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from .models import Profile,LoginHistory

def login_view(request):
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

def user_profile(request):
    return render(request,'user_profile.html')

def students(request):
    users = User.objects.all()
    user=request.user.username
    count=LoginHistory.objects.all()
    return render(request, 'students.html',{'users': users,'count':count})
    
    
# views.py or any other file

@login_required
def home_view(request):
    return render(request, 'index.html')


def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        decoded_file = base64.b64decode(str_img)

        x = Log()
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()

        res = classify_face(x.photo.path)
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
            
                x.profile = profile
                x.save()

                # Increment login count
                history, created = LoginHistory.objects.get_or_create(user=user.username)
                history.user=user.username
                history.count += 1
                history.save()

                login(request, user)
                user = request.user.username
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'User not found.'})
        return JsonResponse({'success': False, 'message': 'No face detected.'})
