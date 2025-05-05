import os
import json
import time
import random
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import RoomMember, ChatMessage
from accounts.decorators import allow_user
from agora_token_builder import RtcTokenBuilder

# ============================
# PAGE ROUTES
# ============================

@login_required(login_url='login_view')
@allow_user(['is_teacher', 'is_student'])
def lobby(request, name):
    """
    Renders the video chat lobby page with user and room context.
    """
    return render(request, 'base/lobby.html', {
        'room_name': name,
        'user_name': request.user
    })

def room(request):
    """
    Fallback view for the room (unused if lobby handles routing).
    """
    return render(request, 'base/room.html')


# ============================
# AGORA TOKEN GENERATION
# ============================

def getToken(request):
    """
    Generates a secure token using Agora's SDK for real-time video communication.
    """
    appId = "ea8afd3db07a44eeb9878e48c8295ea6"
    appCertificate = "064e5d3b00404057881f77bd81e3e2f9"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expire = int(time.time()) + 3600
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, 1, expire)
    return JsonResponse({'token': token, 'uid': uid})


# ============================
# ROOM MEMBERS (JOIN / LEAVE / GET)
# ============================

@csrf_exempt
def createMember(request):
    """
    Adds a member to the room or gets the existing one.
    """
    data = json.loads(request.body)
    member, _ = RoomMember.objects.get_or_create(
        name=data['name'], uid=data['UID'], room_name=data['room_name']
    )
    return JsonResponse({'name': data['name']}, safe=False)

def getMember(request):
    """
    Fetches the member's name from room by UID.
    """
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    return JsonResponse({'name': member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    """
    Removes a member from the room.
    """
    data = json.loads(request.body)
    RoomMember.objects.get(
        name=data['name'], uid=data['UID'], room_name=data['room_name']
    ).delete()
    return JsonResponse('Member deleted', safe=False)


# ============================
# CHAT SYSTEM (SEND / FETCH)
# ============================

@csrf_exempt
def send_chat_message(request):
    """
    API endpoint to send chat messages between users.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        sender = data.get('sender')
        receiver = data.get('receiver')
        message = data.get('message')
        if sender and receiver and message:
            ChatMessage.objects.create(sender=sender, recipient=receiver, message=message)
            return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

def get_chat_messages(request, username):
    """
    Fetches all messages sent to a user or broadcasted to the room.
    """
    if request.method == "GET":
        messages = ChatMessage.objects.filter(recipient__in=['room', username]).order_by('timestamp')
        data = [{
            "sender": m.sender,
            "message": m.message,
            "timestamp": m.timestamp.strftime("%H:%M:%S")
        } for m in messages]
        return JsonResponse({"messages": data})


# ============================
# LIVE ASL SENTENCE POLLING
# ============================

def get_live_asl_sentence(request):
    """
    Polls a text file that holds the most recent ASL-recognized sentence.
    Used for real-time sentence feedback from the detection API.
    """
    file_path = os.path.join(settings.BASE_DIR, 'meeting', 'API', 'latest_sentence.txt')
    if not os.path.exists(file_path):
        return JsonResponse({"sentence": ""})
    with open(file_path, 'r', encoding="utf-8") as f:
        sentence = f.read()
    return JsonResponse({"sentence": sentence})
