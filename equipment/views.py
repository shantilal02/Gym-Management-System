from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _auth(request):
    return bool(request.session.get('user'))

def equipment_list(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    items = read_json(settings.EQUIPMENT_FILE)
    return render(request, 'equipment/list.html', {'items': items})

@csrf_protect
def equipment_add(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category') or ''
        quantity = int(request.POST.get('quantity','1') or 1)
        status = request.POST.get('status','OK')
        items = read_json(settings.EQUIPMENT_FILE)
        it = {'id': next_id(items), 'name': name, 'category': category, 'quantity': quantity, 'status': status}
        items.append(it)
        write_json(settings.EQUIPMENT_FILE, items)
        log(f"EQUIPMENT_ADD {name}")
        messages.success(request, 'Equipment added')
        return redirect('equipment_list')
    return render(request, 'equipment/add.html')

def equipment_delete(request, eid: int):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    items = read_json(settings.EQUIPMENT_FILE)
    items = [x for x in items if x['id'] != eid]
    write_json(settings.EQUIPMENT_FILE, items)
    log(f"EQUIPMENT_DELETE id={eid}")
    messages.success(request, 'Deleted equipment')
    return redirect('equipment_list')

