from django.shortcuts import render,HttpResponse
from .models import Table
from django.core.paginator import Paginator
from django.core.mail import send_mail
from mydemo import settings

def pagination_function(paginator, page, is_paginated=True):
    if not is_paginated:
        return {}

    left = []
    right = []
    left_has_more = False
    right_has_more = False
    first = False
    last = False
    page_number = page.number
    total_pages = paginator.num_pages
    page_range = paginator.page_range

    if page_number == 1:
        right = page_range[page_number:page_number + 2]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        if left[0] > 2:
            left_has_more = True

        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }

    return data

def check_mail(email,msg):
    send_mail(
        subject='这是我给你推荐的洗发水，希望你变得更强(django发送)',
        message=msg,
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[email]   

    )
    #return HttpResponse('测试邮件已发出请注意查收')

def index_view(request,pageId=1):
    all_data = Table.objects.filter()
    paginator = Paginator(all_data,5)

    if pageId < 1:
        pageId = 1
    if pageId > paginator.num_pages:
        pageId = paginator.num_pages

    ulist = paginator.page(pageId)
    is_paginated = True
    data = pagination_function(paginator, ulist, is_paginated)

    if request.method == 'POST':
        print("hello")
        email = request.POST["email"]
        msg = request.POST["msg"]
        check_mail(email,msg)
    
    return render(request,'table.html',locals())