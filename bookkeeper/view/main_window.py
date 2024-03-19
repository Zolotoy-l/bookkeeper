from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QLineEdit, QComboBox, QInputDialog)
import bookkeeper.view.budget_table as bt
import bookkeeper.view.expenses_table as et


class MainWindow(QMainWindow):
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

        self.category_layout = QHBoxLayout()
        self.category_layout.addWidget(QLabel('Категория:'))
        self.select_category = QLineEdit()
        self.category_layout.addWidget(self.select_category)
        self.layout.addLayout(self.category_layout)

        self.category = QComboBox(self)
        self.layout.addWidget(QLabel('Выберите категорию расхода:'))
        self.layout.addWidget(self.category)

        self.expense_button_layout = QHBoxLayout()
        self.add_expense_button = QPushButton('Добавить расходы')
        self.add_expense_button.clicked.connect(self.add_expense)
        self.expense_button_layout.addWidget(self.add_expense_button)

        self.add_category_button = QPushButton('Добавить категорию')
        self.add_category_button.clicked.connect(self.add_category)
        self.expense_button_layout.addWidget(self.add_category_button)
        self.layout.addLayout(self.expense_button_layout)

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

    def refresh_budgets(self):
        bdgt = self.controller.read('Budget', None)
        budget_daily = str(bdgt[0])
        budget_weekly = str(bdgt[1])
        budget_monthly = str(bdgt[2])

        self.budget_table.setItem(0, 1, QTableWidgetItem(budget_daily))
        self.budget_table.setItem(1, 1, QTableWidgetItem(budget_weekly))
        self.budget_table.setItem(2, 1, QTableWidgetItem(budget_monthly))

    def update_budgets(self):
        self.controller.update('Budget', {'daily': float(self.budget_table.item(0, 1).text()),
                                          'weekly': float(self.budget_table.item(1, 1).text()),
                                          'monthly': float(self.budget_table.item(2, 1).text())})
        self.refresh_budgets()

    def refresh_expenses(self):
        num_row = self.controller.get_count('Expense')
        for i in range(num_row):
            expn = self.controller.read('Expense', i+1)
            expn_date = str(expn[0])
            expn_amount = str(expn[1])
            expn_category = str(expn[2])
            expn_comment = str(expn[3])

            self.expenses_table.setItem(num_row-i-1, 0, QTableWidgetItem(expn_date))
            self.expenses_table.setItem(num_row-i-1, 1, QTableWidgetItem(expn_amount))
            self.expenses_table.setItem(num_row-i-1, 2, QTableWidgetItem(expn_category))
            self.expenses_table.setItem(num_row-i-1, 3, QTableWidgetItem(expn_comment))

    def add_expense(self):
        self.controller.create('Expense', {'amount': float(self.add_amount.text()),
                                           'category': self.add_category.text()})
        self.expenses_table.setRowCount(self.expenses_table.rowCount()+1)
        self.refresh_expenses()

    def update_expenses(self, item):
        row = item.row()
        if (self.expenses_table.item(row, 1) is not None and
            self.expenses_table.item(row, 2) is not None and
                self.expenses_table.item(row, 3) is not None):
            num_row = self.controller.get_count('Expense')
            self.controller.update('Expense', {'date': (self.expenses_table.item(row, 0).text()),
                                               'amount': float(self.expenses_table.item(row, 1).text()),
                                               'category': str(self.expenses_table.item(row, 2).text()),
                                               'comment': (self.expenses_table.item(row, 3).text()),
                                               'row': num_row-row})
        #self.refresh_expenses()

    def add_category(self):
        dlg = QInputDialog(self)
        dlg.resize(200, 100)
        dlg.setWindowTitle("Добавление категории")
        dlg.setLabelText("Введите название категории:")
        dlg.setOkButtonText("Подтвердить")
        dlg.setCancelButtonText("Отмена")
        ok = dlg.exec()
        text = dlg.textValue()
        if ok:
            self.controller.create('Category', {'name': text})
            self.refresh_categories()

    def refresh_categories(self):
        cats = self.controller.read('Category', None)
        self.category.addItems(cats)
