from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem


def create_table():
    table = QTableWidget(4, 20)
    table.setColumnCount(4)
    table.setRowCount(1)
    table.setHorizontalHeaderLabels(
        "Дата Сумма Категория Комментарий".split())
    header = table.horizontalHeader()
    header.setSectionResizeMode(
        0, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(
        1, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(
        2, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(
        3, QHeaderView.Stretch)
    table.setEditTriggers(
        QAbstractItemView.NoEditTriggers)
    table.verticalHeader().hide()

    for i in range(table.rowCount()):
        for j in range(table.columnCount()):
            table.setItem(i, j, QTableWidgetItem('-'))

    return table
