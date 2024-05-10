import os.path
import re
from pathlib import Path
import pickle


class FinHelper:
    """Личный финансовый кошелек."""

    DB = Path(__file__).parent / 'db.bin'

    def __init__(self, id, date, category, summa, description):
        """Инициализация класса"""
        self.id = id
        self.date = date
        self.category = category
        self.summa = summa
        self.description = description

    def __str__(self) -> str:
        """Строковое представление экземпляра класса"""
        rec = [
                f'ID: {self.id}\n',
                f'Дата: {self.date}\n',
                f'Категория: {self.category}\n',
                f'Сумма: {self.summa}\n',
                f'Описание: {self.description}\n',
                ]
        return ''.join(rec)

    @classmethod
    def get_len_file(cls) -> int:
        """Получить количество записей в файле."""
        count = 0
        if os.path.exists(cls.DB):
            with open(cls.DB, 'rb') as file:
                try:
                    while True:
                        pickle.load(file)
                        count += 1
                except EOFError:
                    pass
                finally:
                    return count
        else: return 0

    @classmethod
    def display_record_by_id(cls, id):
        """Вывод записи по id."""
        if os.path.exists(cls.DB):
            if cls.is_exists(id):
                with open(cls.DB, 'rb') as file:
                    for _ in range(id):
                        instance = pickle.load(file)
                    print()
                    print(instance)
            else:
                print()
                print(f'Запись {id} не существует')

    def is_valid(self) -> bool:
        """Валидация введенных данных."""
        match_date = re.fullmatch(r'20\d\d\-[0-1]\d-[0-3]\d', self.date)
        match_category = any([self.category == 'Доход', self.category == 'Расход'])
        match_summa = re.fullmatch(r'\d{1,7}', self.summa)
        return all([match_date, match_category, match_summa])

    @classmethod
    def is_exists(cls, id) -> bool:
        return int(id) <= cls.get_len_file()

    def create(self):
        """Добавление записи."""
        if self.is_valid():
            with open(self.DB, 'ab') as file:
                self.id = self.get_len_file() + 1
                pickle.dump(self, file)
                print()
                print(f'Запись {self.id} успешно создана:')
        else:
            print()
            print('Новая запись не создана. Проверьте данные!')

    def update(self):
        """Редактирование записи."""
        if os.path.exists(self.DB):
            if self.is_exists(self.id):
                temp_list = self.read_file()
                index = int(self.id) - 1
                old_date = temp_list[index][1]
                old_category = temp_list[index][2]
                old_summa = temp_list[index][3]
                old_description = temp_list[index][4]

                self.date = self.date if self.date else old_date
                self.category = self.category if self.category else old_category
                self.summa = self.summa if self.summa else old_summa
                self.description = self.description if self.description else old_description

                temp_list[index] = (self.id, self.date, self.category, self.summa, self.description)

                if self.is_valid():
                    with open(self.DB, 'wb') as file:
                        for attr in temp_list:
                            instance = FinHelper(*attr)
                            pickle.dump(instance, file)
                        print()
                        print(f'Запись {self.id} успешно изменена')
                else:
                    print()
                    print(f'Запись {self.id} не изменена. Проверьте данные!')

    @classmethod
    def read_file(cls) -> list:
        """Чтение записей из файла в виде списка."""
        temp_list = []
        if os.path.exists(cls.DB):
            with open(cls.DB, 'rb') as file:
                for _ in range(cls.get_len_file()):
                    instance = pickle.load(file)
                    temp_list.append((
                        instance.id,
                        instance.date,
                        instance.category,
                        instance.summa,
                        instance.description
                        ))
                return temp_list
        else: return temp_list

    @classmethod
    def get_balance(cls):
        """Вывод баланса."""
        if os.path.exists(cls.DB):
            temp_list = cls.read_file()
            income = sum([int(i[3]) for i in temp_list if i[2] == 'Доход'])
            expense = sum([int(i[3]) for i in temp_list if i[2] == 'Расход'])
            print()
            print(f'БАЛАНС = {income - expense}')
            print(f'ДОХОДЫ = {income}')
            print(f'РАСХОДЫ = {expense}')

    @classmethod
    def search_by(cls, field, value):
        """Поиск по записям."""
        if os.path.exists(cls.DB):
            count = 0
            temp_list = cls.read_file()
            for i in temp_list:
                if (field == 'Категория' and value == i[2]) or (field == 'Дата' and value == i[1]) or (field == 'Сумма' and value == i[3]):
                    cls.display_record_by_id(int(i[0]))
                    count += 1
            if count == 0:
                    print()
                    print(f'Записей по {field}: {value} не найдено')
            else:
                print()
                print(f'Найдено {count} записей')

if __name__ == '__main__':

    while True:
        print()
        print('МЕНЮ:')
        print('0 - ВЫХОД')
        print('1 - НОВАЯ ЗАПИСЬ')
        print('2 - ИЗМЕНИТЬ ЗАПИСЬ')
        print('3 - ПОЛУЧИТЬ ЗАПИСЬ ПО id')
        print('4 - ВЫВОД БАЛАНСА')
        print('5 - ПОИСК')

        choice = input('Выберете действие: ')

        if choice == '0': break

        if choice == '1':
            data = input('Введите дату: ')
            category = input('Введите категорию: ')
            summa = input('Введите сумму: ')
            description = input('Введите описание: ')
            inst = FinHelper(None, data, category, summa, description)
            inst.create()

        if choice == '2':
            try:
                id = int(input('Введите номер записи: '))
                if FinHelper.is_exists(id):
                    data = input('Введите новую дату: ')
                    category = input('Введите новую категорию: ')
                    summa = input('Введите новую сумму: ')
                    description = input('Введите новое описание: ')
                    inst = FinHelper(id, data, category, summa, description)
                    inst.update()
                else:
                    print()
                    print(f'Запись {id} не существует')
            except ValueError:
                print()
                print('Недопустимый ввод')

        if choice == '3':
            try:
                id = int(input('Введите номер записи: '))
                FinHelper.display_record_by_id(id)
            except ValueError:
                print()
                print('Недопустимый ввод')

        if choice == '4':
            FinHelper.get_balance()

        if choice == '5':
            field = input('Введите поле поиска (Дата, Категория или Сумма): ')
            value = input('Введите значение (Например: 2024-05-02, Доход, Расход, 200): ')
            FinHelper.search_by(field, value)
