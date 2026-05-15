
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _require_login(request):
    if not request.session.get('user'):
        messages.error(request, 'Please login')
        return False
    return True

def members_list(request):
    if not _require_login(request): return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    return render(request, 'members/list.html', {'members': members})

@csrf_protect
def member_create(request):
    if not _require_login(request): return redirect('/accounts/login/')
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        age = int(request.POST.get('age','0') or 0)
        plan = request.POST.get('plan','').strip()
        price = float(request.POST.get('price','0') or 0)
        duration_days = int(request.POST.get('duration_days','30') or 30)
        members = read_json(settings.MEMBERS_FILE)
        m = {
            'id': next_id(members),
            'name': name,
            'age': age,
            'membership': {'plan': plan, 'price': price, 'duration_days': duration_days}
        }
        members.append(m)
        write_json(settings.MEMBERS_FILE, members)
        log(f"MEMBER_CREATE {name} plan={plan}")
        messages.success(request, 'Member created')
        return redirect('members_list')
    return render(request, 'members/create.html')

@csrf_protect
def member_edit(request, mid: int):
    if not _require_login(request): return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    m = next((x for x in members if x['id'] == mid), None)
    if not m:
        messages.error(request, 'Member not found')
        return redirect('members_list')
    if request.method == 'POST':
        m['name'] = request.POST.get('name', m['name']).strip()
        m['age'] = int(request.POST.get('age', m['age']))
        m['membership']['plan'] = request.POST.get('plan', m['membership']['plan']).strip()
        m['membership']['price'] = float(request.POST.get('price', m['membership']['price']))
        m['membership']['duration_days'] = int(request.POST.get('duration_days', m['membership']['duration_days']))
        write_json(settings.MEMBERS_FILE, members)
        log(f"MEMBER_EDIT id={mid}")
        messages.success(request, 'Updated')
        return redirect('members_list')
    return render(request, 'members/edit.html', {'m': m})

def member_delete(request, mid: int):
    if not _require_login(request): return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    members = [x for x in members if x['id'] != mid]
    write_json(settings.MEMBERS_FILE, members)
    log(f"MEMBER_DELETE id={mid}")
    messages.success(request, 'Deleted')
    return redirect('members_list')
