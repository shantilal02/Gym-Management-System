from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _ensure_login(request):
    if not request.session.get('user'):
        messages.error(request, 'Please login')
        return False
    return True

def classes_list(request):
    if not _ensure_login(request): return redirect('/accounts/login/')
    classes = read_json(settings.CLASSES_FILE)
    members = read_json(settings.MEMBERS_FILE)
    return render(request, 'classes/list.html', {'classes': classes, 'members': members})

@csrf_protect
def class_create(request):
    if not _ensure_login(request): return redirect('/accounts/login/')
    if request.method == 'POST':
        title = request.POST.get('title','').strip()
        trainer = request.POST.get('trainer','').strip()
        capacity = int(request.POST.get('capacity','20') or 20)
        date = request.POST.get('date','')
        start = request.POST.get('start','')
        end = request.POST.get('end','')
        classes = read_json(settings.CLASSES_FILE)
        c = {'id': next_id(classes), 'title': title, 'trainer': trainer, 'capacity': capacity,
             'schedule': {'date': date, 'start': start, 'end': end}, 'attendees': []}
        classes.append(c)
        write_json(settings.CLASSES_FILE, classes)
        log(f"CLASS_CREATE {title} trainer={trainer}")
        messages.success(request, 'Class created')
        return redirect('classes_list')
    return render(request, 'classes/create.html')

@csrf_protect
def class_enroll(request, cid: int):
    if not _ensure_login(request): return redirect('/accounts/login/')
    classes = read_json(settings.CLASSES_FILE)
    members = read_json(settings.MEMBERS_FILE)
    c = next((x for x in classes if x['id'] == cid), None)
    if not c:
        messages.error(request, 'Class not found')
        return redirect('classes_list')
    if request.method == 'POST':
        mid = int(request.POST.get('member_id'))
        if len(c['attendees']) >= c['capacity']:
            messages.error(request, 'Class is full')
            return redirect('classes_list')
        if mid in c['attendees']:
            messages.error(request, 'Member already enrolled')
            return redirect('classes_list')
        if not any(m['id'] == mid for m in members):
            messages.error(request, 'Member not found')
            return redirect('classes_list')
        c['attendees'].append(mid)
        write_json(settings.CLASSES_FILE, classes)
        log(f"CLASS_ENROLL class={cid} member={mid}")
        messages.success(request, 'Member enrolled')
        return redirect('classes_list')
    return render(request, 'classes/enroll.html', {'c': c, 'members': members})

def class_delete(request, cid: int):
    if not _ensure_login(request): return redirect('/accounts/login/')
    classes = read_json(settings.CLASSES_FILE)
    classes = [x for x in classes if x['id'] != cid]
    write_json(settings.CLASSES_FILE, classes)
    log(f"CLASS_DELETE id={cid}")
    messages.success(request, 'Deleted class')
    return redirect('classes_list')

