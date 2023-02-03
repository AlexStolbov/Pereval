import logging
import json
from django.http import HttpResponse
from .services import PerevalDataControl

logger_one = logging.getLogger('debug_one')


def submit_data(request):
    """
    Принимает данные о прохождении перевала.
    Отправляет их на запись в базу.
    """
    if request.method == 'POST':
        logger_one.info(f'request body {request.body}')
        data_control = PerevalDataControl(request.body)
        if data_control.check_data():
            data_control.submit_data()
        result = data_control.format_result()
    else:
        result = {'result': 'method don"t support'}

    return HttpResponse(json.dumps(result))
