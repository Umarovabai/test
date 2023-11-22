import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import pandas as pd
import matplotlib.pyplot as plt

class BettingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Betting App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Создание таблицы для отображения аккаунтов
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Account ID', 'Balance'])
        self.layout.addWidget(self.table_widget)

        # Загрузка данных в таблицу
        self.populate_table()

        # Подключение обработчика двойного клика
        self.table_widget.itemDoubleClicked.connect(self.show_account_graph)

    def populate_table(self):
        # фиктивные данные
        data = {'Account ID': [1, 2, 3], 'Balance': [1000, 1500, 800]}
        df = pd.DataFrame(data)

        for row_index, row_data in df.iterrows():
            self.table_widget.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table_widget.setItem(row_index, col_index, item)

    def show_account_graph(self, item):
        account_id = int(self.table_widget.item(item.row(), 0).text())

        # Получение данных ставок из базы данных по account_id
        bets_data = self.get_bets_data(account_id)

        # Расчет баланса после каждой ставки
        bets_data['bet_result'] = bets_data.apply(lambda row: self.calculate_bet_result(row['bet_amount'], row['result']), axis=1)
        bets_data['balance'] = bets_data['bet_result'].cumsum()

        # Построение графика
        self.plot_account_balance(bets_data)

    def get_bets_data(self, account_id):
        # фиктивные данные
        data = {'bet_amount': [100, 200, 50], 'result': [20, -50, 30]}
        df = pd.DataFrame(data)
        return df

    def calculate_bet_result(self, bet_amount, result):
        return result - bet_amount

    def calculate_balance(self, prev_balance, bet_result):
        return prev_balance + bet_result

    def plot_account_balance(self, bets_data):
        fig, ax = plt.subplots()
        ax.plot(bets_data.index, bets_data['balance'], label='Balance')
        ax.set_xlabel('Bet Index')
        ax.set_ylabel('Balance')
        ax.legend()

        # Отображение графика в новом окне
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = BettingApp()
    main_window.show()
    sys.exit(app.exec_())
