import io
import logging
import datetime
from enum import Enum
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Tourist, PerevalAdded, Images
from .serializers import LoadDataPerevalSerializer, PerevalTransform

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
        self.serializer = LoadDataPerevalSerializer()
        super().__init__()

    class ResultCode(Enum):
        OperationError = '500'
        BadRequest = '400'
        Success = '200'

    def check_data(self):
        """
        Проверка наличия всех полей
        """
        stream = io.BytesIO(bytes(self.data_in_raw))
        data = JSONParser().parse(stream)
        self.serializer = LoadDataPerevalSerializer(data=data)
        if not self.serializer.is_valid():
            self.status = self.ResultCode.BadRequest.value,
            self.message = f"Bad Request. {self.serializer.errors}"
            self.new_id = 'null'
            return False
        self.data_in_decoded = self.serializer.validated_data
        return True

    def submit_data(self):
        """
        Записывает данные в базу
        """
        pereval_transform = self.serializer.save()
        new_pereval = pereval_transform.to_model()
        new_pereval.row_data = self.serializer.data
        new_pereval.add_data = datetime.datetime.now()
        new_pereval.status = PerevalAdded.ModerationStatus.New.value
        new_pereval.tourist = PerevalDataControl.find_or_create_tourist(new_pereval.user_data)
        new_pereval.save()

        self.save_images(new_pereval, self.data_in_decoded["images"])

        self.status = self.ResultCode.Success.value,
        self.message = "Успех"
        self.new_id = new_pereval.id

        return True

    @staticmethod
    def find_or_create_tourist(sender: dict) -> Tourist:
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

    @staticmethod
    def save_images(pereval: PerevalAdded, images: list) -> None:
        """
        Сохраняет изображения
        """
        for image in images:
            new_image = Images()
            new_image.pereval_added = pereval
            new_image.title = image['title']
            image_in = image['data']
            # logger_one.info(f'save images {type(image_in)}')
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

    @staticmethod
    def get_pereval_data(pereval_id: int) -> str:
        """
        Возвращает json представление о данных перевала по его id
        """
        found = PerevalAdded.objects.filter(pk=pereval_id)
        if found.exists():
            pereval_transform = PerevalTransform(pereval=found[0])
            serializer = LoadDataPerevalSerializer(pereval_transform)
            # logger_one.info(f'serializer {serializer.data}')
            result = JSONRenderer().render(serializer.data)
        else:
            result = f'Pereval id {pereval_id} not found'
        return result
