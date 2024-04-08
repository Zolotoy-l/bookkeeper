"""Main bookkeeper window"""
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QTableWidgetItem, QPushButton,
                               QHBoxLayout, QLineEdit, QComboBox,
                               QInputDialog, QDialog)
import bookkeeper.view.budget_table as bt
import bookkeeper.view.expenses_table as et


class MainWindow(QMainWindow):
    """Main window logic and GUI"""
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.budget_table = bt.create_table()
        self.expenses_table = et.create_table(self.controller.get_count('Expense'))

        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 700)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))
        self.layout.addWidget(self.expenses_table)

        self.amount_layout = QHBoxLayout()
        self.amount_layout.addWidget(QLabel('Сумма:'))
        self.add_amount = QLineEdit()
        self.amount_layout.addWidget(self.add_amount)
        self.layout.addLayout(self.amount_layout)

        self.category = QComboBox(self)
        self.layout.addWidget(QLabel('Выберите категорию расхода:'))
        self.layout.addWidget(self.category)

        self.expense_button_layout = self.expenses_button_layout_create()
        self.layout.addLayout(self.expense_button_layout)

        self.category_button_layout = self.category_button_layout_create()
        self.layout.addLayout(self.category_button_layout)

        self.layout.addWidget(QLabel('Бюджет'))
        self.layout.addWidget(self.budget_table)

        self.button_layout = QHBoxLayout()

        self.refresh_button = QPushButton('Загрузить бюджет')
        self.refresh_button.clicked.connect(self.refresh_budgets)
        self.button_layout.addWidget(self.refresh_button)

        self.update_button = QPushButton('Сохранить бюджет')
        self.update_button.clicked.connect(self.update_budgets)
        self.button_layout.addWidget(self.update_button)

        self.layout.addLayout(self.button_layout)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.refresh_budgets()
        self.refresh_expenses()
        self.refresh_categories()

        self.expenses_table.itemChanged.connect(self.update_expenses)

    def expenses_button_layout_create(self):
        """create layout with expenses buttons"""
        expense_button_layout = QHBoxLayout()
        add_expense_button = QPushButton('Добавить расходы')
        add_expense_button.clicked.connect(self.add_expense)
        expense_button_layout.addWidget(add_expense_button)

        delete_expense_button = QPushButton('Удалить расходы')
        delete_expense_button.clicked.connect(self.delete_expense)
        expense_button_layout.addWidget(delete_expense_button)
        return expense_button_layout

    def category_button_layout_create(self):
        """create layout with category buttons"""
        category_button_layout = QHBoxLayout()
        add_category_button = QPushButton('Добавить категорию')
        add_category_button.clicked.connect(self.add_category)
        category_button_layout.addWidget(add_category_button)

        update_category_button = QPushButton('Обновить категорию')
        update_category_button.clicked.connect(self.update_category)
        category_button_layout.addWidget(update_category_button)

        delete_category_button = QPushButton('Удалить категорию')
        delete_category_button.clicked.connect(self.delete_category)
        category_button_layout.addWidget(delete_category_button)
        return category_button_layout

    def refresh_budgets(self):
        """refreshing dates in budget table"""
        bdgt = self.controller.read('Budget', None)
        budget_daily = str(bdgt[0])
        budget_weekly = str(bdgt[1])
        budget_monthly = str(bdgt[2])

        self.budget_table.setItem(0, 1, QTableWidgetItem(budget_daily))
        self.budget_table.setItem(1, 1, QTableWidgetItem(budget_weekly))
        self.budget_table.setItem(2, 1, QTableWidgetItem(budget_monthly))

        expense_sum = self.controller.read('Expense_sum', None)
        sum_daily = str(expense_sum[0])
        sum_weekly = str(expense_sum[1])
        sum_monthly = str(expense_sum[2])

        self.budget_table.setItem(0, 0, QTableWidgetItem(sum_daily))
        self.budget_table.setItem(1, 0, QTableWidgetItem(sum_weekly))
        self.budget_table.setItem(2, 0, QTableWidgetItem(sum_monthly))

        if expense_sum[0] > bdgt[0]:
            self.budget_table.item(0, 0).setForeground(QColor('red'))
        else:
            self.budget_table.item(0, 0).setForeground(QColor('black'))

        if expense_sum[1] > bdgt[1]:
            self.budget_table.item(1, 0).setForeground(QColor('red'))
        else:
            self.budget_table.item(1, 0).setForeground(QColor('black'))

        if expense_sum[2] > bdgt[2]:
            self.budget_table.item(2, 0).setForeground(QColor('red'))
        else:
            self.budget_table.item(2, 0).setForeground(QColor('black'))

    def update_budgets(self):
        """update budget data in database"""
        self.controller.update('Budget',
                               {'daily': float(self.budget_table.item(0, 1).text()),
                                'weekly': float(self.budget_table.item(1, 1).text()),
                                'monthly': float(self.budget_table.item(2, 1).text())})
        self.refresh_budgets()

    def refresh_expenses(self):
        """updates data un GUI expense table"""
        num_row = self.controller.get_count('Expense')
        self.expenses_table.setRowCount(num_row)
        for i in range(num_row):
            expn = self.controller.read('Expense', i)
            expn_date = str(expn[0])
            expn_amount = str(expn[1])
            expn_category = str(expn[2])
            expn_comment = str(expn[3])

            self.expenses_table.setItem(num_row-i-1, 0, QTableWidgetItem(expn_date))
            self.expenses_table.setItem(num_row-i-1, 1, QTableWidgetItem(expn_amount))
            self.expenses_table.setItem(num_row-i-1, 2, QTableWidgetItem(expn_category))
            self.expenses_table.setItem(num_row-i-1, 3, QTableWidgetItem(expn_comment))

    def add_expense(self):
        """adds expense to database and refreshes budget ant expenses table"""
        try:
            self.controller.create('Expense', {'amount': float(self.add_amount.text()),
                                               'category': self.category.currentText()})
            self.expenses_table.setRowCount(self.expenses_table.rowCount() + 1)
            self.refresh_expenses()
            self.refresh_budgets()
        except ValueError:
            print("Inserted expense amount is not float")

    def update_expenses(self, item):
        """updates expenses data in database"""
        row = item.row()
        if (self.expenses_table.item(row, 1) is not None and
                self.expenses_table.item(row, 2) is not None and
                self.expenses_table.item(row, 3) is not None):
            num_row = self.controller.get_count('Expense')
            self.controller.update('Expense',
                                   {'date': (self.expenses_table.item(row, 0).text()),
                                    'amount': float(self.expenses_table.item(row, 1).text()),
                                    'category': str(self.expenses_table.item(row, 2).text()),
                                    'comment': (self.expenses_table.item(row, 3).text()),
                                    'row': num_row - row - 1})
            self.refresh_budgets()

    def delete_expense(self):
        """delete expense from GUI table and db"""
        dlg = QInputDialog(self)
        dlg.resize(200, 100)
        dlg.setWindowTitle("Удаление расхода")
        dlg.setLabelText("Введите номер строки расхода:")
        dlg.setOkButtonText("Подтвердить")
        dlg.setCancelButtonText("Отмена")
        fin = dlg.exec()
        row = int(dlg.textValue())
        if fin:
            num_row = self.controller.get_count('Expense')
            self.controller.delete('Expense', {'row': num_row - row})
            self.refresh_expenses()
            self.refresh_budgets()

    def add_category(self):
        """add new category to combobox"""
        dlg = QInputDialog(self)
        dlg.resize(200, 100)
        dlg.setWindowTitle("Добавление категории")
        dlg.setLabelText("Введите название категории:")
        dlg.setOkButtonText("Подтвердить")
        dlg.setCancelButtonText("Отмена")
        fin = dlg.exec()
        text = dlg.textValue()
        if fin:
            self.controller.create('Category', {'name': text})
            self.refresh_categories()

    def refresh_categories(self):
        """update categories data in combobox"""
        for i in range(self.category.count()):
            self.category.removeItem(0)
        cats = self.controller.read('Category', None)
        self.category.addItems(cats)

    def delete_category(self):
        """delete category from db and combobox,
           removes all expenses with that category"""
        dlg = QInputDialog(self)
        dlg.resize(200, 100)
        dlg.setWindowTitle("Удаление категории")
        dlg.setLabelText("Введите название категории:")
        dlg.setOkButtonText("Подтвердить")
        dlg.setCancelButtonText("Отмена")
        fin = dlg.exec()
        text = dlg.textValue()
        if fin:
            self.controller.delete('Category', {'name': text})
            self.refresh_categories()
            self.refresh_expenses()
            self.refresh_budgets()

    def update_category(self):
        """rename category, updates category and expenses
           with renamed category in dg and gui table"""
        dlg = QDialog(self)
        dlg.resize(200, 100)
        dlg.setWindowTitle("Обновление категории")
        dlg.setModal(True)

        layout = QVBoxLayout()

        label = QLabel("Название категории:")
        layout.addWidget(label)
        input_prev_name = QLineEdit()
        layout.addWidget(input_prev_name)

        label = QLabel("Новое название категории:")
        layout.addWidget(label)
        input_new_name = QLineEdit()
        layout.addWidget(input_new_name)

        button_layout = QHBoxLayout()
        accept_button = QPushButton('Подтвердить')
        accept_button.clicked.connect(dlg.accept)
        button_layout.addWidget(accept_button)

        reject_button = QPushButton('Отмена')
        reject_button.clicked.connect(dlg.reject)
        button_layout.addWidget(reject_button)
        layout.addLayout(button_layout)

        dlg.setLayout(layout)

        fin = dlg.exec()

        prev_name = input_prev_name.text()
        new_name = input_new_name.text()
        if fin:
            self.controller.update('Category', {'prev_name': prev_name,
                                                'new_name': new_name})
            self.refresh_categories()
            self.refresh_expenses()
            self.refresh_budgets()
