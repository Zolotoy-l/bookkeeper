from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem


def create_table():
    table = QTableWidget(4, 20)
    table.setColumnCount(2)
    table.setRowCount(3)
    table.setHorizontalHeaderLabels(
        "Сумма Бюджет".split())
    table.setVerticalHeaderLabels(
        "День Неделя Месяц".split())
    header = table.horizontalHeader()
    header.setSectionResizeMode(
        0, QHeaderView.Stretch)
    header.setSectionResizeMode(
        1, QHeaderView.Stretch)
    table.setEditTriggers(
        QAbstractItemView.DoubleClicked)

    for i in range(table.rowCount()):
        for j in range(table.columnCount()):
            table.setItem(i, j, QTableWidgetItem('0'))

    return table
