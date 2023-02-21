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
        Создает экземпляр сериализатора для проверки наличия полей
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
        new_pereval = self._pereval_save(
            pereval_transform=pereval_transform,
            patch=False)

        self.save_images(new_pereval, self.data_in_decoded["images"])

        self.status = self.ResultCode.Success.value,
        self.message = "Успех"
        self.new_id = new_pereval.id

        return True

    def patch_data(self, pereval_id: int):
        """
        Обновляет существующие данные перевала, если он не был модерирован.
        Нельзя изменять ФИО, адрес почты, телефон.
        """
        state = 0
        message = ""
        found = PerevalAdded.objects.filter(pk=pereval_id)
        if not found.exists():
            message = f'pereval {pereval_id} not found'
        else:
            exists_pereval_transform = PerevalTransform(pereval=found[0])
            if exists_pereval_transform.status != PerevalAdded.ModerationStatus.New.value:
                message = f'pereval {pereval_id} not new'
            else:
                new_pereval_transform = self.serializer.save()
                do_not_edit_fields = ['email',
                                      'name',
                                      'fam',
                                      'otc',
                                      'phone']
                err_fields = []
                for _field in do_not_edit_fields:
                    # logger_one.info(f'patched_data {patched_pereval_transform}')
                    if exists_pereval_transform.user[_field] != new_pereval_transform.user[_field]:
                        err_fields.append(_field)
                if err_fields:
                    message = f'{err_fields} can not be changed'
                else:
                    new_pereval_transform.pereval_id = exists_pereval_transform.pereval_id
                    self._pereval_save(
                        pereval_transform=new_pereval_transform,
                        patch=True)
                    state = 1
        result = {'state': state, 'message': message}
        return result

    def _pereval_save(self,
                      pereval_transform: PerevalTransform,
                      patch: bool) -> PerevalAdded:
        new_pereval = pereval_transform.to_model()
        new_pereval.row_data = self.serializer.data
        new_pereval.add_data = datetime.datetime.now()
        if not patch:
            new_pereval.status = PerevalAdded.ModerationStatus.New.value
            new_pereval.tourist = PerevalDataControl.find_or_create_tourist(
                new_pereval.user_data
            )
        new_pereval.save()
        self.save_images(new_pereval, self.data_in_decoded["images"])
        return new_pereval

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
            new_image.image = image['data']
            new_image.save()

    def format_result(self) -> dict:
        """
        Возвращает форматированный ответ по результатам обработки запроса
        """
        return {"status": self.status,
                "message": self.message,
                "id": self.new_id}

    def get_pereval_data(self, pereval_id: int) -> bytes:
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
            result = b''
        return result

    def get_perevals_for_email(self, email: str) -> list:
        """
        Возвращает список перевалов для туриста с заданной эл. почтой.
        """
        result = []
        found_tourist = Tourist.objects.filter(email=email)
        if found_tourist.exists():
            found_perevals = PerevalAdded.objects.filter(tourist=found_tourist[0])
            for pereval in found_perevals:
                result.append(self.get_pereval_data(pereval.id).decode())
            return result
        # else:
        #     result = {'message': f'tourist with {email} not found'}
        return result

