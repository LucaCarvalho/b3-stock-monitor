from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from tunnel_monitor.utils.ticker import get_last_quote
from .models import Tunnel, PriceLog
from .forms import TunnelForm

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(request, "tunnel_monitor/index.html")
    else:
        tunnels = Tunnel.objects.filter(auth_user=request.user.id)
        last_prices = {}
        for tunnel in tunnels:
            last_prices[tunnel.id] = get_last_quote(tunnel.id)

        return render(request, "tunnel_monitor/list_tunnels.html", context={"tunnels": tunnels, "last_prices": last_prices})

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

@login_required
def get_quote_history(request: HttpRequest, tunnel_id: int) -> JsonResponse:
    # Doing this to ensure the tunnel belongs to the current user
    tunnel = Tunnel.objects.get(id=tunnel_id, auth_user=request.user.id)
    prices = PriceLog.objects.filter(tunnel=tunnel.id)

    price_series = {}
    for price in prices:
        price_series[price.time.isoformat()] = price.price
    
    return JsonResponse(price_series)