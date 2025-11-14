# outages/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, CustomAuthenticationForm, AddCityForm
from .models import Community, Outage, User, VoltageReading
from django.utils import timezone

# --------------------- AUTH ---------------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'outages/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'outages/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


# --------------------- DASHBOARD ---------------------
@login_required
def dashboard(request):
    communities = Community.objects.all().order_by("name")

    # Active outages from DB
    recorded_active_outages = Outage.objects.filter(is_resolved=False)

    # Detect communities with voltage <= 0
    zero_voltage_communities = []
    community_data = []

    for community in communities:
        latest_reading = VoltageReading.objects.filter(community=community).order_by('-timestamp').first()
        voltage = latest_reading.voltage if latest_reading else None

        # Determine status
        if voltage is not None and voltage <= 0:
            status = "Voltage Issue"
            zero_voltage_communities.append(community)
        else:
            status = "Online" if community.power_status else "Offline"

        community_data.append({
            'community': community,
            'voltage': voltage if voltage is not None else "N/A",
            'status': status
        })

    # Total active outages = DB outages + communities with voltage issues
    total_active_outages = len(recorded_active_outages) + len(zero_voltage_communities)

    context = {
        'communities': communities,
        'community_data': community_data,
        'active_outages': recorded_active_outages,
        'total_active_outages': total_active_outages,
    }

    return render(request, 'outages/dashboard.html', context)

# --------------------- OUTAGE ACTIONS ---------------------
@login_required
def acknowledge_outage(request, outage_id):
    outage = get_object_or_404(Outage, id=outage_id)
    if request.method == 'POST' and not outage.is_acknowledged:
        outage.is_acknowledged = True
        outage.acknowledged_at = timezone.now()
        outage.acknowledged_by = request.user
        outage.save()
    return redirect('dashboard')


@login_required
def resolve_outage(request, outage_id):
    outage = get_object_or_404(Outage, id=outage_id)
    if request.method == 'POST' and not outage.is_resolved:
        outage.is_resolved = True
        outage.end_time = timezone.now()
        outage.resolved_by = request.user
        # Restore power status
        outage.community.power_status = True
        outage.community.save()
        outage.save()
    return redirect('dashboard')


# --------------------- ADD CITY ---------------------
@login_required
def add_city(request):
    if request.method == 'POST':
        form = AddCityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'City added successfully!')
            return redirect('dashboard')
    else:
        form = AddCityForm()
    return render(request, 'outages/add_city.html', {'form': form})
@login_required
def communities(request):
    communities = Community.objects.all().order_by('name')
    return render(request, 'outages/communities.html', {'communities': communities})
@login_required
def outages_list(request):
    active_outages = Outage.objects.filter(is_resolved=False)
    return render(request, 'outages/outages.html', {'active_outages': active_outages})

@login_required
def history(request):
    past_outages = Outage.objects.filter(is_resolved=True)
    return render(request, 'outages/history.html', {'past_outages': past_outages})

@login_required
def map_view(request):
    communities = Community.objects.all()
    return render(request, 'outages/map.html', {'communities': communities})
# outages/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community

from django.shortcuts import render, get_object_or_404, redirect
from .models import Community
from .forms import CommunityForm

def edit_community(request, pk):  # <- add pk here
    community = get_object_or_404(Community, id=pk)

    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('communities_list')  # or the name of your list view
    else:
        form = CommunityForm(instance=community)

    return render(request, 'outages/edit_community.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from .models import Community


from django.shortcuts import render
from .models import VoltageReading  # or the model you use for history

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Outage  # Assuming Outage model tracks outages

def history(request):
    # Filter for outages that happened in the last 7 days (you can change this)
    recent_time = timezone.now() - timedelta(days=7)
    recent_outages = Outage.objects.filter(start_time__gte=recent_time).order_by('-start_time')

    context = {
        'recent_outages': recent_outages,
    }
    return render(request, 'outages/history.html', context)


def delete_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        community.delete()
        messages.success(request, "✅ Community deleted successfully.")
        return redirect('community_list')
    return render(request, 'outages/confirm_delete.html', {'community': community})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community
from django.contrib import messages

def community_list(request):
    communities = Community.objects.all()
    return render(request, 'outages/community_list.html', {'communities': communities})
