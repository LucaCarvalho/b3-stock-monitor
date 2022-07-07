from pprint import pprint
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Tunnel
from .utils.ticker import get_ticker_data
from .forms import TunnelForm

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(request, "tunnel_monitor/index.html")
    else:
        tunnels = Tunnel.objects.filter(auth_user=request.user.id)
        return render(request, "tunnel_monitor/list_tunnels.html", context={"tunnels": tunnels})

@login_required
def new_tunnel(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TunnelForm(request.POST)
        if form.is_valid():
            form.instance.auth_user = request.user
            form.save()
            return redirect("index")
    else:
        form = TunnelForm(initial={"auth_user": request.user})

    return render(request, "tunnel_monitor/new_tunnel.html", {"form": form})

@login_required
def edit_tunnel(request: HttpRequest, tunnel_id: int) -> HttpResponse:
    tunnel = Tunnel.objects.get(id=tunnel_id, auth_user=request.user.id)

    if request.method == "POST":
        if request.POST.get("delete", default=False):
            tunnel.delete()
        else:
            form = TunnelForm(request.POST, instance=tunnel)
            if form.is_valid():
                form.instance.auth_user = request.user
                form.save()
                
        return redirect("index")
    else:
        form = TunnelForm(instance=tunnel)

    return render(request, "tunnel_monitor/update_tunnel.html", {"form": form})