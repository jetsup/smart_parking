from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from parking.models import User, Slots
from django.db.models import Q


# Create your views here.
def search_user(request: HttpRequest):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        card_info = request.GET.dict()
        user_card = card_info.get("user-card")
        try:
            user = User.objects.get(rfid=user_card)
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "User does not exist. Consult the admin",
                }
            )
            print("User does not exist:", e)
        print("Card Details: ", user, user_card)
        print("IN USER:", user)
        slot = Slots.objects.get(occupied_by=user)
        if slot:
            print("SLOT:", slot, user)
            msg = "Allocated " + str(slot.slot) + " is_occupied: " + str(slot.occupied)
            return JsonResponse(
                {
                    "status": "success",
                    "message": msg,
                }
            )
        else:
            print("SLOT:", slot, user)
            return JsonResponse(
                {
                    "status": "warning",
                    "message": "You should book your slot from our website",
                }
            )
