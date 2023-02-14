import logging
import json
from django.http import HttpResponse
from .services import PerevalDataControl

logger_one = logging.getLogger('debug_one')


def submit_data(request):
    """
    POST: Принимает данные о прохождении перевала и отправляет на запись в базу.
    GET: Возвращает список перевалов согласно переданного параметра
    """
    if request.method == 'POST':
        data_control = PerevalDataControl(request.body)
        if data_control.check_data():
            data_control.submit_data()
        result = data_control.format_result()
    elif request.method == 'GET':
        if 'user__email' in request.GET:
            logger_one.info(f'get to email {request.GET.get("user__email")}')
            data_control = PerevalDataControl(request.body)
            result = data_control.get_perevals_for_email(request.GET.get('user__email'))
        else:
            result = {'result': f'parameters not found'}
    else:
        result = {'result': f'method don"t {request.method} support'}

    return HttpResponse(json.dumps(result))


def send_data(request, *args, **kwargs):
    """
    GET: Возвращает данные по id перевала
    PATCH: Обновляет данные по id перевала
    """
    if request.method == 'GET':
        logger_one.info(f'get {kwargs}')
        if 'id' in kwargs:
            data_control = PerevalDataControl(request.body)
            data = data_control.get_pereval_data(kwargs['id']).decode()
        else:
            data = f'GET missing patameter id'
    elif request.method == 'PATCH':
        data_control = PerevalDataControl(request.body)
        if data_control.check_data():
            data = data_control.patch_data(kwargs['id'])
    else:
        data = f'error: method {request.method} don"t support'

    return HttpResponse(json.dumps(data))
