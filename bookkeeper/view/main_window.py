from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QLineEdit)
import bookkeeper.view.budget_table as bt
import bookkeeper.view.expenses_table as et


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = None

        self.budget_table = bt.create_table()
        self.expenses_table = et.create_table()

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
        self.add_category = QLineEdit()
        self.category_layout.addWidget(self.add_category)
        self.layout.addLayout(self.category_layout)

        self.expense_button_layout = QHBoxLayout()
        self.add_expense_button = QPushButton('Добавить расходы')
        self.add_expense_button.clicked.connect(self.add_expense)
        self.expense_button_layout.addWidget(self.add_expense_button)
        self.layout.addLayout(self.expense_button_layout)

        self.layout.addWidget(QLabel('Бюджет'))
        self.layout.addWidget(self.budget_table)

        button_layout = QHBoxLayout()

        refresh_button = QPushButton('Загрузить бюджет')
        refresh_button.clicked.connect(self.refresh_budgets)
        button_layout.addWidget(refresh_button)

        update_button = QPushButton('Сохранить бюджет')
        update_button.clicked.connect(self.update_budgets)
        button_layout.addWidget(update_button)

        self.layout.addLayout(button_layout)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_controller(self, controller):
        self.controller = controller

    def refresh_budgets(self):
        bdgt = self.controller.read('Budget')
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

    def add_expense(self):
        self.controller.create('Expense', {'amount': float(self.add_amount.text()),
                                           'category': self.add_category.text()})
