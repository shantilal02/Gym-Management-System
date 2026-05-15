from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _login(request):
    return bool(request.session.get('user'))

def attendance_list(request):
    if not _login(request): 
        messages.error(request, 'Please login'); 
        return redirect('/accounts/login/')
    records = read_json(settings.ATTENDANCE_FILE)
    members = read_json(settings.MEMBERS_FILE)
    name_map = {m['id']: m['name'] for m in members}
    for r in records:
        r['member_name'] = name_map.get(r['member_id'], 'Unknown')
    return render(request, 'attendance/list.html', {'records': records})

@csrf_protect
def attendance_record(request):
    if not _login(request): 
        messages.error(request, 'Please login'); 
        return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    if request.method == 'POST':
        mid = int(request.POST.get('member_id'))
        date = request.POST.get('date')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out') or ''
        records = read_json(settings.ATTENDANCE_FILE)
        rec = {'id': next_id(records), 'member_id': mid, 'date': date, 'check_in': check_in, 'check_out': check_out}
        records.append(rec)
        write_json(settings.ATTENDANCE_FILE, records)
        log(f"ATTENDANCE member={mid} date={date}")
        messages.success(request, 'Attendance recorded')
        return redirect('attendance_list')
    return render(request, 'attendance/record.html', {'members': members})

