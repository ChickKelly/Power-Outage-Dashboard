from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .forms import SignUpForm, CustomAuthenticationForm
from .models import Community, Outage, User
import json

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = SignUpForm()
    return render(request, 'outages/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred during login. Please try again.')
        else:
            messages.error(request, 'Login failed. Please check your credentials and try again.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'outages/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

@login_required
def dashboard(request):
    # Basic data
    communities = Community.objects.all()
    active_outages = Outage.objects.filter(is_resolved=False)
    
    # Calculate statistics
    today = timezone.now().date()
    total_communities = communities.count()
    communities_with_power = communities.filter(power_status=True).count()
    communities_without_power = communities.filter(power_status=False).count()
    
    # Outage statistics
    total_active_outages = active_outages.count()
    resolved_today = Outage.objects.filter(
        is_resolved=True,
        end_time__date=today
    ).count()
    
    # Team statistics
    total_team_members = User.objects.count()
    repair_team_members = User.objects.filter(role='repair_team').count()
    admin_members = User.objects.filter(role='admin').count()
    
    # Recent activity
    recent_outages = Outage.objects.all().order_by('-start_time')[:5]
    
    # Monthly statistics for chart
    current_month = timezone.now().replace(day=1)
    monthly_outages = []
    for i in range(6):
        month_start = current_month - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        count = Outage.objects.filter(
            start_time__range=[month_start, month_end]
        ).count()
        monthly_outages.append({
            'month': month_start.strftime('%b'),
            'count': count
        })
    monthly_outages.reverse()
    
    # Performance metrics
    avg_resolution_time = "2.5 hours"  # This would be calculated from actual data
    response_rate = "98.5%"
    
    context = {
        'communities': communities,
        'active_outages': active_outages,
        'stats': {
            'total_communities': total_communities,
            'communities_with_power': communities_with_power,
            'communities_without_power': communities_without_power,
            'total_active_outages': total_active_outages,
            'resolved_today': resolved_today,
            'total_team_members': total_team_members,
            'repair_team_members': repair_team_members,
            'admin_members': admin_members,
            'avg_resolution_time': avg_resolution_time,
            'response_rate': response_rate,
        },
        'recent_outages': recent_outages,
        'monthly_outages_json': json.dumps(monthly_outages),
    }
    return render(request, 'outages/dashboard.html', context)

@login_required
def outage_history(request):
    outages = Outage.objects.all().order_by('-start_time')
    context = {
        'outages': outages
    }
    return render(request, 'outages/history.html', context)

@login_required
def acknowledge_outage(request, outage_id):
    try:
        outage = get_object_or_404(Outage, id=outage_id)
        if request.method == 'POST':
            if outage.is_acknowledged:
                messages.warning(request, f'Outage at {outage.community.name} has already been acknowledged.')
            elif outage.is_resolved:
                messages.warning(request, f'Outage at {outage.community.name} has already been resolved.')
            else:
                outage.is_acknowledged = True
                outage.acknowledged_at = timezone.now()
                outage.acknowledged_by = request.user
                outage.save()
                messages.success(request, f'Successfully acknowledged outage at {outage.community.name}.')
        else:
            messages.error(request, 'Invalid request method.')
    except Exception as e:
        messages.error(request, 'An error occurred while acknowledging the outage. Please try again.')
    
    return redirect('dashboard')

@login_required
def resolve_outage(request, outage_id):
    try:
        outage = get_object_or_404(Outage, id=outage_id)
        if request.method == 'POST':
            if outage.is_resolved:
                messages.warning(request, f'Outage at {outage.community.name} has already been resolved.')
            else:
                outage.is_resolved = True
                outage.end_time = timezone.now()
                outage.resolved_by = request.user
                outage.community.power_status = True
                outage.community.save()
                outage.save()
                messages.success(request, f'Successfully resolved outage at {outage.community.name}. Power has been restored!')
        else:
            messages.error(request, 'Invalid request method.')
    except Exception as e:
        messages.error(request, 'An error occurred while resolving the outage. Please try again.')
    
    return redirect('dashboard')

@login_required
def map_view(request):
    communities = Community.objects.all()
    communities_data = list(communities.values('name', 'latitude', 'longitude', 'power_status'))
    context = {
        'communities_json': json.dumps(communities_data)
    }
    return render(request, 'outages/map.html', context)
