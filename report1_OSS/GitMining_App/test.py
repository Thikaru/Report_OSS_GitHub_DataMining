from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.resize(800, 600)
        self.move(400, 100)
        # self.setWindowTitle('GitHubデータマイニング「定量的ソフトウェア開発管理」')

        # 1つ目のウィジェット
        self.TopPageWindow()

        # 2つ目のウィジェット
        self.SetHowGetRepositoryDataWindow()

        self.stacked_widget.addWidget(self.top_page_window)
        self.stacked_widget.addWidget(self.set_how_get_repository_data_window)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def switch_widget(self):
        current_widget = self.stacked_widget.currentWidget()
        index = self.stacked_widget.indexOf(current_widget)
        if index == 0:
            self.stacked_widget.setCurrentWidget(
                self.set_how_get_repository_data_window)
        elif index == 1:
            self.stacked_widget.setCurrentWidget(self.top_page_window)
        elif index == 2:
            self.stacked_widget.setCurrentWidget(
                self.decide_use_json_file_path_window)
        elif index == 3:
            self.stacked_widget.setCurrentWidget(self.result_graph_window)
        else:
            self.stacked_widget.setCurrentWidget(self.top_page_window)

    def TopPageWindow(self):
        self.top_page_window = QWidget()
        layout1 = QVBoxLayout()
        button1 = QPushButton("GitリポジトリのデータをJSONで得る", self.top_page_window)
        button1.clicked.connect(self.switch_widget)
        button2 = QPushButton("グラフ出力処理へ", self.top_page_window)
        button2.clicked.connect(self.switch_widget)
        layout1.addWidget(button1)
        layout1.addWidget(button2)
        self.top_page_window.setLayout(layout1)

    def SetHowGetRepositoryDataWindow(self):
        self.set_how_get_repository_data_window = QWidget()
        layout2 = QVBoxLayout()
        button2 = QPushButton(
            "TopPageへ", self.set_how_get_repository_data_window)
        button2.clicked.connect(self.switch_widget)
        layout2.addWidget(button2)
        self.set_how_get_repository_data_window.setLayout(layout2)

    def DecideUseJsonFilePathWindow(self):
        self.decide_use_json_file_path_window = QWidget()
        layout2 = QVBoxLayout()
        button1 = QPushButton(
            "TopPageへ", self.decide_use_json_file_path_window)
        button1.clicked.connect(self.switch_widget)
        layout2.addWidget(button1)
        button2 = QPushButton(
            "結果グラフを表示", self.decide_use_json_file_path_window)
        button2.clicked.connect(self.switch_widget)
        layout2.addWidget(button2)
        self.decide_use_json_file_path_window.setLayout(layout2)

    def ResultGraphWindow(self):
        self.result_graph_window = QWidget()
        layout2 = QVBoxLayout()
        button2 = QPushButton(
            "TopPageへ", self.result_graph_window)
        button2.clicked.connect(self.switch_widget)
        layout2.addWidget(button2)
        self.result_graph_window.setLayout(layout2)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
