from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event, Invitee,SittingFormat
from django.utils import timezone

import datetime


def home(request):
    if request.user.is_authenticated:
        return redirect('sign_in')
    return render(request, 'index.html')

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username1']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                messages.success(request, f"{username} - Logged In Successfully as a staff!!")
                return redirect('admin_dashboard')
            
            messages.success(request, f"{username} - Logged In Successfully as a Common User!!")
            return redirect('staff_dashboard')
        else:

            if User.objects.filter(username=username,is_active = False):
                messages.error(request, "Your account has been deactivated, Please contact your supervisor.")
                return redirect('sign_in')

            else:   
                messages.error(request, "Invalid username or password.")
                return redirect('sign_in')
    else:
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('staff_dashboard')
        else:
              
            return render(request, "login.html")

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

@staff_member_required
def staff_dashboard(request):
    return render(request, "a_dashboard.html")

@staff_member_required
def client_dashboard(request):
    return HttpResponse("s_dashboard.html")


@staff_member_required
def register(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        username = request.POST['username1']
        email = request.POST['email']
        f_name = request.POST['f_name']
        password1 = request.POST['password1']
        password = request.POST['password']
        is_staff = request.POST['is_staff']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Try again!")
            return redirect('sign_up')
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered. Use another email.")
            return redirect('sign_up')
        if password1 != password:
            messages.error(request, "Passwords did not match!")
            return redirect('sign_up')
        
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = f_name
        new_user.last_name = l_name
        new_user.is_active = True
        
        if is_staff == 'on':
            new_user.is_staff = True
        else:
            new_user.is_staff = False
        new_user.save()
        print(is_staff)
        messages.success(request, f"Account for {f_name} {l_name} Created Successfully.")
        return redirect('staff_dashboard')
    
    return render(request, "register.html")

    
@staff_member_required
def all_users(request):
    all_users = User.objects.all()
    return render(request, 'all_users.html', {"all_users":all_users})

@staff_member_required
def register_event(request):
    if request.method == "POST":
        try:
            # Extracting data manually from POST request
            name = request.POST['name']
            date_of_event = request.POST['date_of_event']
            place_of_event = request.POST['place_of_event']
            no_of_invitees = 0
            no_of_invitees_to_luncheon = 0
            field_event_manager = request.POST['field_event_manager']
            luncheon_event_manager = request.POST['luncheon_event_manager']
            sitting_format_list = request.POST['sitting_format_list']
            sitting_format_list = SittingFormat.objects.get(id = sitting_format_list )
            
            # Field Card details
            field_card_cordinate_x = float(request.POST['field_card_cordinate_x'])
            field_card_cordinate_y = float(request.POST['field_card_cordinate_y'])
            field_card_font_type = request.POST['field_card_font_type']
            field_card_font_size = int(request.POST['field_card_font_size'])

            # Luncheon Card details
            luncheon_card_cordinate_x = float(request.POST['luncheon_card_cordinate_x'])
            luncheon_card_cordinate_y = float(request.POST['luncheon_card_cordinate_y'])
            luncheon_card_font_type = request.POST['luncheon_card_font_type']
            luncheon_card_font_size = int(request.POST['luncheon_card_font_size'])

            # Field Envelope details
            field_envelope_card_cordinate_x = float(request.POST['field_envelope_card_cordinate_x'])
            field_envelope_card_cordinate_y = float(request.POST['field_envelope_card_cordinate_y'])
            field_envelope_card_font_type = request.POST['field_envelope_card_font_type']
            field_envelope_card_font_size = int(request.POST['field_envelope_card_font_size'])

            # Luncheon Envelope details
            luncheon_envelope_card_cordinate_x = float(request.POST['luncheon_envelope_card_cordinate_x'])
            luncheon_envelope_card_cordinate_y = float(request.POST['luncheon_envelope_card_cordinate_y'])
            luncheon_envelope_card_font_type = request.POST['luncheon_envelope_card_font_type']
            luncheon_envelope_card_font_size = int(request.POST['luncheon_envelope_card_font_size'])

            # Save the new event
            event = Event.objects.create(
                name_of_event=name,
                date_of_event=date_of_event,
                created_by=request.user,
                place_of_event=place_of_event,
                type_of_sitting_format = sitting_format_list,
                no_of_invitees=no_of_invitees,
                field_card_cordinate_x=field_card_cordinate_x,
                field_card_cordinate_y=field_card_cordinate_y,
                field_card_font_type=field_card_font_type,
                field_card_font_size=field_card_font_size,
                luncheon_card_cordinate_x=luncheon_card_cordinate_x,
                luncheon_card_cordinate_y=luncheon_card_cordinate_y,
                luncheon_card_font_type=luncheon_card_font_type,
                luncheon_card_font_size=luncheon_card_font_size,
                field_envelope_card_cordinate_x=field_envelope_card_cordinate_x,
                field_envelope_card_cordinate_y=field_envelope_card_cordinate_y,
                field_envelope_card_font_type=field_envelope_card_font_type,
                field_envelope_card_font_size=field_envelope_card_font_size,
                luncheon_envelope_card_cordinate_x=luncheon_envelope_card_cordinate_x,
                luncheon_envelope_card_cordinate_y=luncheon_envelope_card_cordinate_y,
                luncheon_envelope_card_font_type=luncheon_envelope_card_font_type,
                luncheon_envelope_card_font_size=luncheon_envelope_card_font_size,
                no_of_invitees_to_luncheon=no_of_invitees_to_luncheon,
                field_event_manager=field_event_manager,
                luncheon_event_manager=luncheon_event_manager,
            )
            messages.success(request, "Event Registered Successfully!")
            return redirect('event_list')  # Adjust redirection
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('event_list')  # Adjust redirection
    sitting_format_list = SittingFormat.objects.all()
    return render(request, 'register_event.html',{'sitting_format_list':sitting_format_list})

@login_required
def event_list(request):
    all_events = Event.objects.all()
    return render (request, 'event_list.html',{'events':all_events})


@staff_member_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('event_list')


@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        try:
            # Extracting data manually from POST request
            name = request.POST['name']
            date_of_event = request.POST['date_of_event']
            place_of_event = request.POST['place_of_event']
            field_event_manager = request.POST['field_event_manager']
            luncheon_event_manager = request.POST['luncheon_event_manager']
            
            # Field Card details
            field_card_cordinate_x = float(request.POST['field_card_cordinate_x'])
            field_card_cordinate_y = float(request.POST['field_card_cordinate_y'])
            field_card_font_type = request.POST['field_card_font_type']
            field_card_font_size = int(request.POST['field_card_font_size'])

            # Luncheon Card details
            luncheon_card_cordinate_x = float(request.POST['luncheon_card_cordinate_x'])
            luncheon_card_cordinate_y = float(request.POST['luncheon_card_cordinate_y'])
            luncheon_card_font_type = request.POST['luncheon_card_font_type']
            luncheon_card_font_size = int(request.POST['luncheon_card_font_size'])

            # Field Envelope details
            field_envelope_card_cordinate_x = float(request.POST['field_envelope_card_cordinate_x'])
            field_envelope_card_cordinate_y = float(request.POST['field_envelope_card_cordinate_y'])
            field_envelope_card_font_type = request.POST['field_envelope_card_font_type']
            field_envelope_card_font_size = int(request.POST['field_envelope_card_font_size'])

            # Luncheon Envelope details
            luncheon_envelope_card_cordinate_x = float(request.POST['luncheon_envelope_card_cordinate_x'])
            luncheon_envelope_card_cordinate_y = float(request.POST['luncheon_envelope_card_cordinate_y'])
            luncheon_envelope_card_font_type = request.POST['luncheon_envelope_card_font_type']
            luncheon_envelope_card_font_size = int(request.POST['luncheon_envelope_card_font_size'])

            # Save the new event
            event = Event.objects.filter(id=event_id).update(
                name_of_event=name,
                date_of_event=date_of_event,
                modified_by=request.user,
                modified_date = datetime.datetime.now(),
                place_of_event=place_of_event,
                field_card_cordinate_x=field_card_cordinate_x,
                field_card_cordinate_y=field_card_cordinate_y,
                field_card_font_type=field_card_font_type,
                field_card_font_size=field_card_font_size,
                luncheon_card_cordinate_x=luncheon_card_cordinate_x,
                luncheon_card_cordinate_y=luncheon_card_cordinate_y,
                luncheon_card_font_type=luncheon_card_font_type,
                luncheon_card_font_size=luncheon_card_font_size,
                field_envelope_card_cordinate_x=field_envelope_card_cordinate_x,
                field_envelope_card_cordinate_y=field_envelope_card_cordinate_y,
                field_envelope_card_font_type=field_envelope_card_font_type,
                field_envelope_card_font_size=field_envelope_card_font_size,
                luncheon_envelope_card_cordinate_x=luncheon_envelope_card_cordinate_x,
                luncheon_envelope_card_cordinate_y=luncheon_envelope_card_cordinate_y,
                luncheon_envelope_card_font_type=luncheon_envelope_card_font_type,
                luncheon_envelope_card_font_size=luncheon_envelope_card_font_size,
                field_event_manager=field_event_manager,
                luncheon_event_manager=luncheon_event_manager,
            )
            messages.success(request, "Event Registered Successfully!")
            return redirect('event_list')  # Adjust redirection
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('event_list')  # Adjust redirection
    
    return render(request, 'edit_event.html',{'event':event})



def current_events(request):
    today = timezone.now().date()
    current_events = Event.objects.filter(date_of_event__gte=today).order_by('date_of_event')  # filter for today and future events
    return render(request, 'current_events.html', {'events': current_events})


@login_required
def register_invitee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        designation = request.POST.get('designation')
        occupation = request.POST.get('occupation')
        sitting_position_field = request.POST.get('sitting_position_field')
        invited_for_luncheon = request.POST.get('invited_for_luncheon')
        sitting_position_luncheon = request.POST.get('sitting_position_luncheon')
        event_id = request.POST.get('event')
        company_organization_department_ministry = request.POST.get('company_organization_department_ministry')
        in_care_of = request.POST.get('in_care_of')
        
        event = Event.objects.get(id=event_id)
        created_by = request.user

        # Create the invitee
        invitee = Invitee(
            name=name,
            title=title,
            designation=designation,
            occupation=occupation,
            sitting_position_field=sitting_position_field,
            invited_for_luncheon=invited_for_luncheon,
            sitting_position_luncheon=sitting_position_luncheon if invited_for_luncheon == 'yes' else None,
            event=event,
            company_organization_department_ministry=company_organization_department_ministry,
            in_care_of=in_care_of,
            created_by=created_by,
            date_created=timezone.now(),
        )
        invitee.save()

        return redirect('all_invitees')  # Replace 'all_invitees' with your actual view name

    events = Event.objects.all()  # Fetch events for the dropdown
    return render(request, 'register_invitee.html', {'events': events})


@staff_member_required
def create_sitting_format(request):
    if request.method == "POST":
        format_name = request.POST.get('format_name')
        arrangement_names = request.POST.getlist('arrangement_names')  # Get multiple sitting types

        if format_name and arrangement_names:
            # Save the format with its array of sitting types
            SittingFormat.objects.create(name=format_name, sitting_types=arrangement_names)
            messages.success(request, 'Sitting format and arrangements created successfully!')
            return redirect('sitting_format_list')  # Redirect after successful creation
        else:
            messages.error(request, 'Please provide a format name and at least one arrangement.')

    return render(request, 'create_sitting_format.html')


@login_required
def sitting_format_list(request):
    formats = SittingFormat.objects.all()  # Retrieve all sitting formats
    return render(request, 'sitting_format_list.html', {'formats': formats})


@staff_member_required
def delete_sitting_form(request, sitting_id):
    sitting_format = get_object_or_404(SittingFormat, id=sitting_id)
    sitting_format.delete()
    messages.success(request, "Sitting format deleted successfully!")
    return redirect('sitting_format_list')











