import os.path
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FinHelper:
    """Личный финансовый кошелек."""

    date: str
    category: str
    sum: int
    description: str

    DB = Path(__file__).parent / 'db.txt'
    LINE_IN_RECORD: int = 6


    def gen_id(self):
        """Генерация идентификатора записи."""
        if os.path.exists(self.DB):
            with open(self.DB, encoding='utf-8') as file:
                last_id = file.readlines()[-5].split()[1]
                return str(int(last_id) + 1)
        else: return '1'

    def is_valid(self):
        """Валидация введенных данных."""
        match_date = re.fullmatch(r'20\d\d\-[0-1]\d-[0-3]\d', self.date)
        match_category = any([self.category == 'Доход', self.category == 'Расход'])
        match_sum = re.fullmatch(r'\d{1,7}', self.sum)
        return all([match_date, match_category, match_sum])

    @classmethod
    def is_exists(cls, id):
        """Проверка за существование записи по заданному id."""
        if os.path.exists(cls.DB):
            with open(cls.DB, encoding='utf-8') as file:
                lines = file.readlines()
            return id <= int(lines[-5].split()[1])

    def create(self):
        """Добавление записи."""
        if self.is_valid():
            id = self.gen_id()
            with open(self.DB, 'a', encoding='utf-8') as file:
                rec = [
                    '\n',
                    f'ID: {id}\n',
                    f'Дата: {self.date}\n',
                    f'Категория: {self.category}\n',
                    f'Сумма: {self.sum}\n',
                    f'Описание: {self.description}\n',
                    ]
                file.writelines(rec)
                print()
                print(f'Запись {id} успешно создана')
        else:
            print()
            print('Новая запись не создана. Проверьте данные!')


    def update(self, id):
        """Редактирование записи."""
        if os.path.exists(self.DB):
            file = open(self.DB, encoding='utf-8')
            lines = file.readlines()
            start_index = (id - 1) * self.LINE_IN_RECORD
            if self.date:
                lines[start_index + 2] = 'Дата: '+ self.date + '\n'
            else:
                self.date = lines[start_index + 2].split()[1]
            if self.category:
                lines[start_index + 3] = 'Категория: ' + self.category + '\n'
            else:
                self.category = lines[start_index + 3].split()[1]
            if self.sum:
                lines[start_index + 4] = 'Сумма: ' + self.sum + '\n'
            else:
                self.sum = lines[start_index + 4].split()[1]
            if self.description:
                lines[start_index + 5] = 'Описание: ' + self.description + '\n'
            file.close()

            if self.is_valid():
                file = open(self.DB, 'w', encoding='utf-8')
                file.writelines(lines)
                print()
                print(f'Запись {id} успешно изменена')
                file.close()
            else:
                print()
                print(f'Запись {id} не изменена. Проверьте данные!')

    @classmethod
    def get_rec(cls, id):
        """Вывод записи по id."""
        if os.path.exists(cls.DB):
            with open(cls.DB, encoding='utf-8') as file:
                lines = file.readlines()
                start_index = (id - 1) * cls.LINE_IN_RECORD
                rec_by_id = lines[start_index : start_index + cls.LINE_IN_RECORD]
                if rec_by_id:
                    [print(line, end='') for line in rec_by_id]
                else:
                    print()
                    print(f'Запись {id} не существует')

    @classmethod
    def get_balance(cls):
        """Вывод баланса."""
        if os.path.exists(cls.DB):
            income = 0
            expense = 0
            with open(cls.DB, encoding='utf-8') as file:
                lines = file.readlines()
                start_indexes = range(0, len(lines), cls.LINE_IN_RECORD)
                for i in start_indexes:
                    if lines[i + 3] == 'Категория: Доход\n':
                        income += int(lines[i + 4].split()[1])
                    if lines[i + 3] == 'Категория: Расход\n':
                        expense += int(lines[i + 4].split()[1])
                print()
                print(f'БАЛАНС = {income - expense}')
                print(f'ДОХОДЫ = {income}')
                print(f'РАСХОДЫ = {expense}')

    @classmethod
    def search_by(cls, field, value):
        """Поиск по записям."""
        if os.path.exists(cls.DB):
            count = 0
            with open(cls.DB, encoding='utf-8') as file:
                lines = file.readlines()
                for i in range(0, len(lines), cls.LINE_IN_RECORD):
                    if ((field == 'Категория' and lines[i + 3] == f'Категория: {value}\n') or
                        (field == 'Дата' and lines[i + 2] == f'Дата: {value}\n') or
                        (field == 'Сумма' and lines[i + 4] == f'Сумма: {value}\n')):
                            id = int(lines[i + 1].split()[1])
                            FinHelper.get_rec(id)
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
            sum = input('Введите сумму: ')
            description = input('Введите описание: ')
            inst = FinHelper(data, category, sum, description)
            inst.create()

        if choice == '2':
            try:
                id = int(input('Введите номер записи: '))
                if FinHelper.is_exists(id):
                    data = input('Введите новую дату: ')
                    category = input('Введите новую категорию: ')
                    sum = input('Введите новую сумму: ')
                    description = input('Введите новое описание: ')
                    inst = FinHelper(data, category, sum, description)
                    inst.update(id)
                else:
                    print()
                    print(f'Запись {id} не существует')
            except ValueError:
                print()
                print('Недопустимый ввод')

        if choice == '3':
            try:
                id = int(input('Введите номер записи: '))
                FinHelper.get_rec(id)
            except ValueError:
                print()
                print('Недопустимый ввод')

        if choice == '4':
            FinHelper.get_balance()

        if choice == '5':
            field = input('Введите поле поиска (Дата, Категория или Сумма): ')
            value = input('Введите значение (Например: 2024-05-02, Доход, Расход, 200): ')
            FinHelper.search_by(field, value)
