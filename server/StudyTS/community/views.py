from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from StudyTS.db_connector import MysqlConnect


@csrf_exempt
def index(request):
    connector = MysqlConnect()
    cursor = connector.get_cursor()
    SQL = 'SELECT * FROM post'
    cursor.execute(SQL)
    connector.close()
    return JsonResponse(cursor.fetchall(), safe=False)


def new(request, username):
    # try:
    user = User.objects.get(email=username)
    if request.method == 'POST':
        connector = MysqlConnect()
        cursor = connector.get_cursor()
        sql = 'INSERT INTO post(user_id, title, content) VALUES ((SELECT id FROM auth_user WHERE email = %s), %s, %s)'
        val = (user.username, request.POST.get('title'), request.POST.get('content'), None)
        cursor.execute(sql, val)
        connector.commit()
        connector.close()
        return redirect('community:finish')
    # except:
    #     return redirect('community:error')
    return render(request, 'community/new.html')


@csrf_exempt
def detail(request):
    return render(request, 'community/new.html')


@csrf_exempt
def finish(request):
    return HttpResponse('')


@csrf_exempt
def error(request):
    return HttpResponse('')


