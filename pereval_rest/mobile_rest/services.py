import logging
import json
import datetime
from enum import Enum
from .models import Tourist, PerevalAdded, Images

logger_one = logging.getLogger('debug_one')


class PerevalDataControl:
    """
    Управляет изменениями в базе перевалов.
    Возвращает json:
        status — код HTTP, целое число:
            500 — ошибка при выполнении операции;
            400 — Bad Request (при нехватке полей);
            200 — успех.
        message — строка:
            Причина ошибки (если она была);
        Отправлено успешно;
            Если отправка успешна, дополнительно возвращается id вставленной
            записи.
        id — идентификатор, который был присвоен объекту при добавлении в базу
        данных.
    result = {"status": 500,
                  "message": "Ошибка подключения к базе данных",
                  "id": 'null'}
    """

    def __init__(self, data_in: str) -> None:
        self.data_in_raw = data_in
        self.data_in_decoded = {}
        self.status = 0
        self.message = ''
        self.new_id = 0
        super().__init__()

    class ResultCode(Enum):
        OperationError = '500'
        BadRequest = '400'
        Success = '200'

    def check_data(self):
        """
        Проверка наличия всех полей
        """
        control_keys = {"beauty_title",
                        "title",
                        "other_titles",
                        "connect",
                        "add_time",
                        "user",
                        "level",
                        "images"}
        self.data_in_decoded = json.loads(self.data_in_raw)
        data_keys = set(self.data_in_decoded.keys())
        missing_keys = control_keys.difference(data_keys)
        if missing_keys:
            self.status = self.ResultCode.BadRequest.value,
            self.message = f"Bad Request. Missing keys {missing_keys}"
            self.new_id = 'null'
            return False
        return True

    def submit_data(self):
        """
        Записывает данные в базу
        """

        new_pereval = PerevalAdded()
        new_pereval.row_data = json.dumps(self.data_in_decoded)
        new_pereval.add_data = datetime.datetime.now()

        sender = self.data_in_decoded['user']
        new_pereval.tourist = self.find_or_create_tourist(sender)
        new_pereval.beautyTitle = self.data_in_decoded['beauty_title']
        new_pereval.title = self.data_in_decoded['title']
        new_pereval.other_titles = self.data_in_decoded['other_titles']
        new_pereval.connect = self.data_in_decoded['connect']
        new_pereval.add_time = self.data_in_decoded['add_time']
        coords = self.data_in_decoded['coords']
        new_pereval.latitude = coords['latitude']
        new_pereval.longitude = coords['longitude']
        new_pereval.height = coords['height']
        level = self.data_in_decoded['level']
        new_pereval.winter_level = level['winter']
        new_pereval.spring_level = level['spring']
        new_pereval.summer_level = level['summer']
        new_pereval.autumn_level = level['autumn']
        new_pereval.status = PerevalAdded.ModerationStatus.New.value
        new_pereval.save()

        self.save_images(new_pereval, self.data_in_decoded["images"])

        self.status = self.ResultCode.Success.value,
        self.message = "Успех"
        self.new_id = new_pereval.id

        return True

    def find_or_create_tourist(self, sender: dict) -> Tourist:
        """
        Ищет туриста по email, если не находит, создает нового.
        """
        found = Tourist.objects.filter(email=sender['email'])
        if not found:
            tourist = Tourist()
            tourist.email = sender['email']
            tourist.name = sender['name']
            tourist.last_name = sender['fam']
            tourist.patronymic = sender['otc']
            tourist.phone = sender['phone']
            tourist.save()
        else:
            tourist = found[0]
        return tourist

    def save_images(self, pereval: PerevalAdded, images: list) -> None:
        """
        Сохраняет изображения
        """
        for image in images:
            new_image = Images()
            new_image.pereval_added = pereval
            new_image.title = image['title']
            image_in = image['data']
            logger_one.info(f'save images {type(image_in)}')
            if type(image_in) == str:
                image_to_save = bytes(image_in, 'utf-8')
            else:
                image_to_save = image_in
            new_image.image = image_to_save
            new_image.save()

    def format_result(self) -> dict:
        """
        Возвращает форматированный ответ по результатам обработки запроса
        """
        return {"status": self.status,
                "message": self.message,
                "id": self.new_id}
