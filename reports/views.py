from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from core.storage import read_json, log

def _auth(request):
    return bool(request.session.get('user'))

def summary_view(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    payments = read_json(settings.PAYMENTS_FILE)
    attendance = read_json(settings.ATTENDANCE_FILE)
    total_members = len(members)
    total_revenue = sum(p.get('amount',0) for p in payments)
    attendance_count = len(attendance)
    data = {'total_members': total_members, 'total_revenue': total_revenue, 'attendance_count': attendance_count}
    return render(request, 'reports/summary.html', {'data': data})

def export_txt(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    payments = read_json(settings.PAYMENTS_FILE)
    attendance = read_json(settings.ATTENDANCE_FILE)
    content = [
        "=== Gym Summary ===",
        f"Members: {len(members)}",
        f"Revenue: ₹{sum(p.get('amount',0) for p in payments)}",
        f"Attendance Records: {len(attendance)}",
        "==================="
    ]
    with open(settings.LOG_FILE, 'a', encoding='utf-8') as f:
        f.write('\n'.join(content) + '\n')
    log("REPORT_EXPORT")
    messages.success(request, 'Exported to logs.txt')
    return redirect('summary_view')

