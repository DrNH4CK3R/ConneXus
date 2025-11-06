from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, MemberProfile, Notification, Club
from django.contrib import messages
from .forms import ClubForm, MemberSignupForm, UserSignupForm, EventForm, ReportForm
from django.db.models import Q
from datetime import datetime
from .gemini_service import generate_event_report

def home(request):
	return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)            
            if user.is_superuser:  # Check if the user is an admin
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            else:
                return redirect('feed')  # Redirect to the member dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html')

def logout_view(request):
	logout(request)
	return redirect('home')

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('member_signup')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

def member_signup(request):
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            form.save_m2m()  # Save the many-to-many field data for clubs
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('feed')
    else:
        form = MemberSignupForm(initial={'username': request.user.username})
    return render(request, 'createMem.html', {'form': form})

def feed_view(request):
	notes = Notification.objects.all()
	important_notifications = Notification.objects.filter(headline__icontains='import')
	latest_events = Event.objects.order_by('date_time')[:5]
	context = {
        'important_notifications': important_notifications,
        'latest_events': latest_events,
        'notdata': notes,
    }
	return render(request, 'feed.html', context)
def admin_view(request):
	notes = Notification.objects.all()
	important_notifications = Notification.objects.filter(headline__icontains='import')
	latest_events = Event.objects.order_by('date_time')[:5]
	context = {
        'important_notifications': important_notifications,
        'latest_events': latest_events,
        'notdata': notes,
    }
	return render(request, 'adminFeed.html', context)

def addEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        another_form = ReportForm(request.POST)

        if 'event_submit' in request.POST and form.is_valid():
            club_name = form.cleaned_data['organizing_club']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            try:
                club = Club.objects.get(name=club_name)
                event = form.save(commit=False)
                event.organizing_club = club
                event.date_time = datetime.combine(date, time)
                event.save()
                messages.success(request, 'Event successfully added.')
                return redirect('admin_dashboard')
            except Club.DoesNotExist:
                messages.error(request, 'Organizing club not found.')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors.')

        report = None 
        if 'report_submit' in request.POST and another_form.is_valid():
            event_data = {
                'name': another_form.cleaned_data['name'],
                'date': another_form.cleaned_data['date'],
                'description': another_form.cleaned_data['description'],
            }
            report = generate_event_report(event_data)
    else:
    	report = None
    	form = EventForm()
    	another_form = ReportForm()
        
    return render(request, 'addEvent.html', {'form': form, 'another_form': another_form, 'report': report})

def delEvent(request):
	if request.method == 'POST':
		evname = request.POST.get('event_name')
		event = get_object_or_404(Event, event_name=evname)
		event.delete()

		return redirect('admin_dashboard')

def search_events(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        events = Event.objects.filter(event_name__icontains=query)
        results = [event.event_name for event in events]
        return JsonResponse(results, safe=False)

def addNotic(request):
	if request.method == 'POST':
		nhead = request.POST.get('headline')
		ndesc = request.POST.get('notification_description')

		note = Notification(
			headline=nhead,
			description=ndesc,
		)
		note.save()

		return redirect('admin_dashboard')
	else:
		return render(request, 'addNoti.html')

def delNotic(request):
    if request.method == 'POST':
        head = request.POST.get('headline')
        notification = get_object_or_404(Notification, headline=head)
        notification.delete()
        return redirect('admin_dashboard')

def search_notifications(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        notifications = Notification.objects.filter(headline__icontains=query)
        results = [notification.headline for notification in notifications]
        return JsonResponse(results, safe=False)


def events_json(request):
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append({
            'title': event.event_name,
            'start': event.date_time.isoformat(),
            'description': event.event_description,
            'Organizer': event.organizing_club,
        })
    return JsonResponse(events_list, safe=False)

def list_users(request):
    query = request.GET.get('q')
    club_filter = request.GET.get('club')
    members = MemberProfile.objects.all()
    clubs = Club.objects.all()
    
    if query:
        members = members.filter(
            Q(full_name__icontains=query) | 
            Q(branch__icontains=query) | 
            Q(semester__icontains=query)
        )
    
    if club_filter:
        members = members.filter(clubs__name=club_filter)

    return render(request, 'members.html', {'members': members, 'clubs': clubs, 'selected_club': club_filter})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club has been added successfully.')
            return redirect('clubs')  # Redirect to the same form or wherever you want
    else:
        form = ClubForm()
        clubs = Club.objects.all()
    return render(request, 'add_club.html', {'form': form, 'clubs': clubs})

def delClub(request):
	if request.method == 'POST':
		cname = request.POST.get('club_name')
		cl = get_object_or_404(Club, name=cname)
		cl.delete()

		return redirect('clubs')

def member_detail(request, username):
    member = get_object_or_404(MemberProfile, user__username=username)
    context = {
        'member': member,
    }
    return render(request, 'member_detail.html', context)

def club_events(request):
    user = request.user
    member_profile = MemberProfile.objects.get(user=user)
    clubs = member_profile.clubs.all()
    events_by_club = {club: Event.objects.filter(organizing_club=club) for club in clubs}

    return render(request, 'club_events.html', {'events_by_club': events_by_club})



