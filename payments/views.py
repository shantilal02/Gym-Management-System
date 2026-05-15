from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _auth(request):
    return bool(request.session.get('user'))

def payments_list(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    payments = read_json(settings.PAYMENTS_FILE)
    members = read_json(settings.MEMBERS_FILE)
    name_map = {m['id']: m['name'] for m in members}
    for p in payments:
        p['member_name'] = name_map.get(p['member_id'], 'Unknown')
    return render(request, 'payments/list.html', {'payments': payments})

@csrf_protect
def payment_record(request):
    if not _auth(request): messages.error(request,'Login'); return redirect('/accounts/login/')
    members = read_json(settings.MEMBERS_FILE)
    if request.method == 'POST':
        mid = int(request.POST.get('member_id'))
        amount = float(request.POST.get('amount','0') or 0)
        method = request.POST.get('method','CASH')
        payments = read_json(settings.PAYMENTS_FILE)
        txn_id = f"TXN-{next_id(payments)}"
        p = {'id': next_id(payments), 'member_id': mid, 'amount': amount, 'method': method, 'transaction_id': txn_id}
        payments.append(p)
        write_json(settings.PAYMENTS_FILE, payments)
        log(f"PAYMENT member={mid} amount={amount} method={method} txn={txn_id}")
        messages.success(request, 'Payment recorded')
        return redirect('payments_list')
    return render(request, 'payments/record.html', {'members': members})

