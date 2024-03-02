# Create your views here.

import base64

from django.shortcuts import render, redirect
from typing import Dict

rooms: Dict = {}


def index(request):
    print(rooms)
    return render(request, "chat/index.html", {"rooms": rooms})


def room(request, token):
    try:
        room_name, person_name = base64.b64decode(token).decode("utf-8").split("<><>")
        if room_name in rooms.keys():
            if person_name in rooms.get(room_name):
                return redirect("/chat")
    except Exception:
        return redirect("/chat")
    return render(
        request,
        "chat/room.html",
        {"room_name": room_name, "person_name": person_name, "token": token},
    )
