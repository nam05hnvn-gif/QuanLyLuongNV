from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from datetime import datetime
from . import DAO


def index(request):
    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', 'fund_id')              
    order = request.GET.get('order', 'asc')        

    res = DAO.list_funds(search=search, sort=sort, order=order)

    if isinstance(res, dict) and res.get('error'):
        messages.error(request, f"DB error: {res.get('error')}")
        funds = []
    else:
        funds = res

    return render(request, 'funds/index.html', {
        'funds': funds,
        'search': search,
        'sort': sort,
        'order': order,
    })


def add_funds(request):
    if request.method == 'POST':
        fund_id = request.POST.get('fund_id')
        fund_amount = request.POST.get('fund_amount', '0')
        if not fund_id:
            messages.error(request, 'Thiếu fund_id.')
            return render(request, 'funds/add_funds.html', {'fund_id': fund_id, 'fund_amount': fund_amount})
        try:
            payload = {'fund_id': fund_id, 'fund_amount': fund_amount}
            res = DAO.add_fund(payload)
            if isinstance(res, dict) and res.get('error'):
                messages.error(request, f"Lỗi: {res.get('error')}")
                return render(request, 'funds/add_funds.html', {'fund_id': fund_id, 'fund_amount': fund_amount})
            # success (DAO returns {"message": ...})
            messages.success(request, res.get('message', 'Added.'))
            return redirect(reverse('funds:index'))
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm: {e}")
            return render(request, 'funds/add_funds.html', {'fund_id': fund_id, 'fund_amount': fund_amount})
    return render(request, 'funds/add_funds.html')


def change_funds(request,id):
    fund = DAO.get_fund_by_id(id)
    if request.method == 'POST':
        fund_id = id
        admin_id = request.session.get('id') #Trong session luu id admin dang dang nhap
        amount = request.POST.get('amount')
        transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Số tiền phải lớn hơn 0.')
                return redirect(reverse('funds:change_funds', args=[id]))
        except ValueError:
            messages.error(request, 'Số tiền phải là số.')
            return redirect(reverse('funds:change_funds', args=[id]))

        if transaction_type == 'rut' and amount > fund['fund_amount']:
            messages.error(request, 'Không thể rút vượt quá số dư hiện tại.')
            return redirect(reverse('funds:change_funds', args=[id]))

        try:
            payload = {
                'fund_id': fund_id,
                'admin_id': admin_id,
                'amount': amount,
                'transaction_date': transaction_date,
                'transaction_type': transaction_type
            }
            res = DAO.change_fund(payload)
            if isinstance(res, dict) and res.get('error'):
                messages.error(request, f"Lỗi: {res.get('error')}")
            else:
                messages.success(request, res.get('message', 'Updated.'))
        except Exception as e:
            messages.error(request, f"Lỗi khi cập nhật: {e}")
        return redirect(reverse('funds:change_funds', args=[id]))
    return render(request, 'funds/change_funds.html', {'fund': fund})


def delete_funds(request, id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        res = DAO.delete_fund({'fund_id': id})

        if isinstance(res, dict) and res.get('error'):
            messages.error(request, f"Lỗi khi xóa quỹ: {res.get('error')}")
        else:
            messages.success(request, res.get('message', 'Đã xóa quỹ thành công.'))

    except Exception as e:
        messages.error(request, f"Lỗi hệ thống khi xóa quỹ: {e}")

    return redirect(reverse('funds:index'))


def view_transactions(request):
    try:
        res = DAO.list_transactions()
        if isinstance(res, dict) and res.get('error'):
            messages.error(request, f"DB error: {res.get('error')}")
            transactions = []
        else:
            transactions = res
    except Exception as e:
        messages.error(request, f"Lỗi khi lấy giao dịch: {e}")
        transactions = []
    return render(request, 'funds/transactions.html', {'transactions': transactions})