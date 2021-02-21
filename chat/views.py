from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'user_name': request.user.username
    })

def logout(request):
    logout(request)
    return render(request, 'chat/index.html')

