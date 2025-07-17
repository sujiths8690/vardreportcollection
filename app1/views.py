from django.http import JsonResponse
from django.shortcuts import render, redirect
from app1.models import Constituency, LocalBody, MeetingReport
from django.contrib.auth import logout

def user_dashboard(request):
    return render(request, 'userdashboard.html')

def submission_history(request):
    reports = MeetingReport.objects.all().order_by('-meeting_date')
    return render(request, 'submission_history.html', {'reports': reports})

def select_constituency(request):
    constituencies = Constituency.objects.all()

    if request.method == 'POST':
        constituency_id = request.POST.get('constituency')
        local_body_id = request.POST.get('local_body')
        ward_number = request.POST.get('ward_number')

        if constituency_id and local_body_id and ward_number:
            request.session['constituency_id'] = constituency_id
            request.session['local_body_id'] = local_body_id
            request.session['ward_number'] = ward_number
            return redirect('meeting_form')

    return render(request, 'select_constituency.html', {'constituencies': constituencies})

def load_local_bodies(request):
    constituency_id = request.GET.get('constituency_id')
    local_bodies = LocalBody.objects.filter(constituency_id=constituency_id).values(
        'Local_body_id', 'name', 'new_ward_count', 'type'
    )
    return JsonResponse(list(local_bodies), safe=False)

def load_wards(request):
    local_body_id = request.GET.get('local_body_id')
    try:
        local_body = LocalBody.objects.get(Local_body_id=local_body_id)
        ward_numbers = [f"Ward {i}" for i in range(1, local_body.new_ward_count + 1)]
        return JsonResponse({'wards': ward_numbers})
    except LocalBody.DoesNotExist:
        return JsonResponse({'wards': []})

def meeting_form(request):
    if request.method == 'POST':
        constituency_id = request.session.get('constituency_id')
        local_body_id = request.session.get('local_body_id')
        ward_number_str = request.session.get('ward_number')  # e.g. "Ward 5"
        ward_number = int(ward_number_str.replace("Ward ", ""))  # convert to integer

        constituency = Constituency.objects.get(const_id=constituency_id)
        local_body = LocalBody.objects.get(Local_body_id=local_body_id)

        ward_incharge = request.POST.get('ward_incharge')
        office_bearer_name = request.POST.get('office_bearer_name')
        mobile_number = request.POST.get('mobile_number')
        meeting_date = request.POST.get('meeting_date')
        number_of_attendees = request.POST.get('number_of_attendees')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        MeetingReport.objects.create(
            constituency=constituency,
            local_body=local_body,
            ward_number=ward_number,
            ward_incharge=ward_incharge,
            office_bearer_name=office_bearer_name,
            mobile_number=mobile_number,
            meeting_date=meeting_date,
            number_of_attendees=number_of_attendees,
            image1=image1,
            image2=image2
        )

        return redirect('meeting_success')

    return render(request, 'form.html')


def meeting_success(request):
    return render(request, 'meeting_success.html')

def admin_logout_redirect(request):
    logout(request)
    return redirect('user_dashboard')
