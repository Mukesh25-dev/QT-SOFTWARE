# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QTableView, QVBoxLayout, QWidget)

import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(781, 576)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setIconSize(QSize(16, 16))
        self.tab_file_attr = QWidget()
        self.tab_file_attr.setObjectName(u"tab_file_attr")
        self.verticalLayout = QVBoxLayout(self.tab_file_attr)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.tab_file_attr)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.tab_file_attr)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton_choose = QPushButton(self.tab_file_attr)
        self.pushButton_choose.setObjectName(u"pushButton_choose")

        self.horizontalLayout_2.addWidget(self.pushButton_choose)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_file_type = QLabel(self.tab_file_attr)
        self.label_file_type.setObjectName(u"label_file_type")

        self.horizontalLayout_4.addWidget(self.label_file_type)

        self.comboBox_data_format = QComboBox(self.tab_file_attr)
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.setObjectName(u"comboBox_data_format")

        self.horizontalLayout_4.addWidget(self.comboBox_data_format)

        self.pushButton_read_attr = QPushButton(self.tab_file_attr)
        self.pushButton_read_attr.setObjectName(u"pushButton_read_attr")

        self.horizontalLayout_4.addWidget(self.pushButton_read_attr)

        self.pushButton_process_file = QPushButton(self.tab_file_attr)
        self.pushButton_process_file.setObjectName(u"pushButton_process_file")

        self.horizontalLayout_4.addWidget(self.pushButton_process_file)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableView_attr = QTableView(self.tab_file_attr)
        self.tableView_attr.setObjectName(u"tableView_attr")

        self.horizontalLayout_3.addWidget(self.tableView_attr)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_proc_algo = QLabel(self.tab_file_attr)
        self.label_proc_algo.setObjectName(u"label_proc_algo")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_proc_algo)

        self.comboBox_proc_algo = QComboBox(self.tab_file_attr)
        self.comboBox_proc_algo.addItem("")
        self.comboBox_proc_algo.addItem("")
        self.comboBox_proc_algo.setObjectName(u"comboBox_proc_algo")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBox_proc_algo)

        self.label_glc = QLabel(self.tab_file_attr)
        self.label_glc.setObjectName(u"label_glc")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_glc)

        self.spinBox_glc = QSpinBox(self.tab_file_attr)
        self.spinBox_glc.setObjectName(u"spinBox_glc")
        self.spinBox_glc.setMinimum(1)
        self.spinBox_glc.setMaximum(1000)
        self.spinBox_glc.setSingleStep(10)
        self.spinBox_glc.setValue(10)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinBox_glc)

        self.label_hpf_order = QLabel(self.tab_file_attr)
        self.label_hpf_order.setObjectName(u"label_hpf_order")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_hpf_order)

        self.spinBox_hpf_order = QSpinBox(self.tab_file_attr)
        self.spinBox_hpf_order.setObjectName(u"spinBox_hpf_order")
        self.spinBox_hpf_order.setMinimum(1)
        self.spinBox_hpf_order.setMaximum(10)
        self.spinBox_hpf_order.setValue(2)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spinBox_hpf_order)

        self.label_hpf_cutoff = QLabel(self.tab_file_attr)
        self.label_hpf_cutoff.setObjectName(u"label_hpf_cutoff")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_hpf_cutoff)

        self.spinBox_hpf_cutoff = QSpinBox(self.tab_file_attr)
        self.spinBox_hpf_cutoff.setObjectName(u"spinBox_hpf_cutoff")
        self.spinBox_hpf_cutoff.setMaximum(1000)
        self.spinBox_hpf_cutoff.setValue(10)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spinBox_hpf_cutoff)

        self.label_window_size = QLabel(self.tab_file_attr)
        self.label_window_size.setObjectName(u"label_window_size")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_window_size)

        self.spinBox_window_size = QSpinBox(self.tab_file_attr)
        self.spinBox_window_size.setObjectName(u"spinBox_window_size")
        self.spinBox_window_size.setMinimum(1)
        self.spinBox_window_size.setMaximum(9999)
        self.spinBox_window_size.setValue(256)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spinBox_window_size)

        self.label_stft_overlap = QLabel(self.tab_file_attr)
        self.label_stft_overlap.setObjectName(u"label_stft_overlap")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_stft_overlap)

        self.spinBox_stft_overlap = QSpinBox(self.tab_file_attr)
        self.spinBox_stft_overlap.setObjectName(u"spinBox_stft_overlap")
        self.spinBox_stft_overlap.setMinimum(1)
        self.spinBox_stft_overlap.setMaximum(9999)
        self.spinBox_stft_overlap.setValue(128)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spinBox_stft_overlap)


        self.horizontalLayout_3.addLayout(self.formLayout)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_file_attr, "")
        self.tab_raw = QWidget()
        self.tab_raw.setObjectName(u"tab_raw")
        self.verticalLayout_2 = QVBoxLayout(self.tab_raw)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_row_no = QLabel(self.tab_raw)
        self.label_row_no.setObjectName(u"label_row_no")

        self.horizontalLayout_5.addWidget(self.label_row_no)

        self.spinBox_row_no = QSpinBox(self.tab_raw)
        self.spinBox_row_no.setObjectName(u"spinBox_row_no")
        self.spinBox_row_no.setMaximum(2)

        self.horizontalLayout_5.addWidget(self.spinBox_row_no)

        self.pushButton_raw = QPushButton(self.tab_raw)
        self.pushButton_raw.setObjectName(u"pushButton_raw")

        self.horizontalLayout_5.addWidget(self.pushButton_raw)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.graphicsView_ch0_raw = pg.PlotWidget(self.tab_raw)
        self.graphicsView_ch0_raw.setObjectName(u"graphicsView_ch0_raw")

        self.verticalLayout_2.addWidget(self.graphicsView_ch0_raw)

        self.graphicsView_ch1_raw = pg.PlotWidget(self.tab_raw)
        self.graphicsView_ch1_raw.setObjectName(u"graphicsView_ch1_raw")

        self.verticalLayout_2.addWidget(self.graphicsView_ch1_raw)

        self.tabWidget.addTab(self.tab_raw, "")
        self.tab_var = QWidget()
        self.tab_var.setObjectName(u"tab_var")
        self.verticalLayout_3 = QVBoxLayout(self.tab_var)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.checkBox_variance = QCheckBox(self.tab_var)
        self.checkBox_variance.setObjectName(u"checkBox_variance")

        self.horizontalLayout_6.addWidget(self.checkBox_variance)

        self.checkBox_sat = QCheckBox(self.tab_var)
        self.checkBox_sat.setObjectName(u"checkBox_sat")

        self.horizontalLayout_6.addWidget(self.checkBox_sat)

        self.checkBox_min_sat = QCheckBox(self.tab_var)
        self.checkBox_min_sat.setObjectName(u"checkBox_min_sat")

        self.horizontalLayout_6.addWidget(self.checkBox_min_sat)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.graphicsView_var = pg.PlotWidget(self.tab_var)
        self.graphicsView_var.setObjectName(u"graphicsView_var")

        self.verticalLayout_3.addWidget(self.graphicsView_var)

        self.tabWidget.addTab(self.tab_var, "")
        self.tab_wf = QWidget()
        self.tab_wf.setObjectName(u"tab_wf")
        self.horizontalLayout_8 = QHBoxLayout(self.tab_wf)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.graphicsView_wf = pg.PlotWidget(self.tab_wf)
        self.graphicsView_wf.setObjectName(u"graphicsView_wf")

        self.horizontalLayout_8.addWidget(self.graphicsView_wf)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_wf_row = QLabel(self.tab_wf)
        self.label_wf_row.setObjectName(u"label_wf_row")
        font = QFont()
        font.setPointSize(12)
        self.label_wf_row.setFont(font)
        self.label_wf_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_wf_row)

        self.doubleSpinBox_wfrow = QDoubleSpinBox(self.tab_wf)
        self.doubleSpinBox_wfrow.setObjectName(u"doubleSpinBox_wfrow")

        self.verticalLayout_5.addWidget(self.doubleSpinBox_wfrow)

        self.pushbutton_wfrow = QPushButton(self.tab_wf)
        self.pushbutton_wfrow.setObjectName(u"pushbutton_wfrow")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        self.pushbutton_wfrow.setFont(font1)

        self.verticalLayout_5.addWidget(self.pushbutton_wfrow)

        self.graphicsView_wf_row = pg.PlotWidget(self.tab_wf)
        self.graphicsView_wf_row.setObjectName(u"graphicsView_wf_row")

        self.verticalLayout_5.addWidget(self.graphicsView_wf_row)

        self.label_wfcolumn = QLabel(self.tab_wf)
        self.label_wfcolumn.setObjectName(u"label_wfcolumn")
        self.label_wfcolumn.setFont(font)
        self.label_wfcolumn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_wfcolumn)

        self.doubleSpinBox_wfcolumn = QDoubleSpinBox(self.tab_wf)
        self.doubleSpinBox_wfcolumn.setObjectName(u"doubleSpinBox_wfcolumn")

        self.verticalLayout_5.addWidget(self.doubleSpinBox_wfcolumn)

        self.pushButton_wfcol = QPushButton(self.tab_wf)
        self.pushButton_wfcol.setObjectName(u"pushButton_wfcol")
        font2 = QFont()
        font2.setPointSize(11)
        self.pushButton_wfcol.setFont(font2)

        self.verticalLayout_5.addWidget(self.pushButton_wfcol)

        self.graphicsView_wf_col = pg.PlotWidget(self.tab_wf)
        self.graphicsView_wf_col.setObjectName(u"graphicsView_wf_col")

        self.verticalLayout_5.addWidget(self.graphicsView_wf_col)


        self.horizontalLayout_8.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tab_wf, "")
        self.tab_freq = QWidget()
        self.tab_freq.setObjectName(u"tab_freq")
        self.horizontalLayout_9 = QHBoxLayout(self.tab_freq)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.graphicsView_psd = pg.PlotWidget(self.tab_freq)
        self.graphicsView_psd.setObjectName(u"graphicsView_psd")

        self.horizontalLayout_9.addWidget(self.graphicsView_psd)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_specrow = QLabel(self.tab_freq)
        self.label_specrow.setObjectName(u"label_specrow")
        self.label_specrow.setFont(font)
        self.label_specrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_specrow)

        self.doubleSpinBox_specrow = QDoubleSpinBox(self.tab_freq)
        self.doubleSpinBox_specrow.setObjectName(u"doubleSpinBox_specrow")

        self.verticalLayout_6.addWidget(self.doubleSpinBox_specrow)

        self.pushButton_specrow = QPushButton(self.tab_freq)
        self.pushButton_specrow.setObjectName(u"pushButton_specrow")
        self.pushButton_specrow.setFont(font2)

        self.verticalLayout_6.addWidget(self.pushButton_specrow)

        self.graphicsView_psd_row = pg.PlotWidget(self.tab_freq)
        self.graphicsView_psd_row.setObjectName(u"graphicsView_psd_row")

        self.verticalLayout_6.addWidget(self.graphicsView_psd_row)

        self.label_speccol = QLabel(self.tab_freq)
        self.label_speccol.setObjectName(u"label_speccol")
        self.label_speccol.setFont(font)
        self.label_speccol.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_speccol)

        self.doubleSpinBox_speccol = QDoubleSpinBox(self.tab_freq)
        self.doubleSpinBox_speccol.setObjectName(u"doubleSpinBox_speccol")

        self.verticalLayout_6.addWidget(self.doubleSpinBox_speccol)

        self.pushButton_speccol = QPushButton(self.tab_freq)
        self.pushButton_speccol.setObjectName(u"pushButton_speccol")
        self.pushButton_speccol.setFont(font2)

        self.verticalLayout_6.addWidget(self.pushButton_speccol)

        self.graphicsView_psd_col = pg.PlotWidget(self.tab_freq)
        self.graphicsView_psd_col.setObjectName(u"graphicsView_psd_col")

        self.verticalLayout_6.addWidget(self.graphicsView_psd_col)


        self.horizontalLayout_9.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.tab_freq, "")
        self.tab_stft = QWidget()
        self.tab_stft.setObjectName(u"tab_stft")
        self.horizontalLayout_10 = QHBoxLayout(self.tab_stft)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.graphicsView_stft = pg.PlotWidget(self.tab_stft)
        self.graphicsView_stft.setObjectName(u"graphicsView_stft")

        self.horizontalLayout_10.addWidget(self.graphicsView_stft)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_stftrow = QLabel(self.tab_stft)
        self.label_stftrow.setObjectName(u"label_stftrow")
        self.label_stftrow.setFont(font)
        self.label_stftrow.setFrameShadow(QFrame.Shadow.Plain)
        self.label_stftrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_stftrow)

        self.doubleSpinBox_stftrow = QDoubleSpinBox(self.tab_stft)
        self.doubleSpinBox_stftrow.setObjectName(u"doubleSpinBox_stftrow")

        self.verticalLayout_7.addWidget(self.doubleSpinBox_stftrow)

        self.pushButton_stftrow = QPushButton(self.tab_stft)
        self.pushButton_stftrow.setObjectName(u"pushButton_stftrow")
        self.pushButton_stftrow.setFont(font2)

        self.verticalLayout_7.addWidget(self.pushButton_stftrow)

        self.graphicsView_stft_row = pg.PlotWidget(self.tab_stft)
        self.graphicsView_stft_row.setObjectName(u"graphicsView_stft_row")

        self.verticalLayout_7.addWidget(self.graphicsView_stft_row)

        self.label_stftcol = QLabel(self.tab_stft)
        self.label_stftcol.setObjectName(u"label_stftcol")
        self.label_stftcol.setFont(font)
        self.label_stftcol.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_stftcol)

        self.doubleSpinBox_stftcol = QDoubleSpinBox(self.tab_stft)
        self.doubleSpinBox_stftcol.setObjectName(u"doubleSpinBox_stftcol")

        self.verticalLayout_7.addWidget(self.doubleSpinBox_stftcol)

        self.pushButton_stftcol = QPushButton(self.tab_stft)
        self.pushButton_stftcol.setObjectName(u"pushButton_stftcol")
        self.pushButton_stftcol.setFont(font2)

        self.verticalLayout_7.addWidget(self.pushButton_stftcol)

        self.graphicsView_stft_col = pg.PlotWidget(self.tab_stft)
        self.graphicsView_stft_col.setObjectName(u"graphicsView_stft_col")

        self.verticalLayout_7.addWidget(self.graphicsView_stft_col)


        self.horizontalLayout_10.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.tab_stft, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.graphicsView = pg.PlotWidget(self.tab)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(10, 10, 411, 501))
        self.verticalLayoutWidget = QWidget(self.tab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(430, 10, 321, 501))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fk_label_row = QLabel(self.verticalLayoutWidget)
        self.fk_label_row.setObjectName(u"fk_label_row")
        self.fk_label_row.setFont(font)
        self.fk_label_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.fk_label_row)

        self.doubleSpinBox_fkrow = QDoubleSpinBox(self.verticalLayoutWidget)
        self.doubleSpinBox_fkrow.setObjectName(u"doubleSpinBox_fkrow")

        self.verticalLayout_4.addWidget(self.doubleSpinBox_fkrow)

        self.pushButton_fk_row = QPushButton(self.verticalLayoutWidget)
        self.pushButton_fk_row.setObjectName(u"pushButton_fk_row")
        self.pushButton_fk_row.setFont(font)

        self.verticalLayout_4.addWidget(self.pushButton_fk_row)

        self.graphicsView_fk_row = pg.PlotWidget(self.verticalLayoutWidget)
        self.graphicsView_fk_row.setObjectName(u"graphicsView_fk_row")

        self.verticalLayout_4.addWidget(self.graphicsView_fk_row)

        self.label_fk_column = QLabel(self.verticalLayoutWidget)
        self.label_fk_column.setObjectName(u"label_fk_column")
        self.label_fk_column.setFont(font)
        self.label_fk_column.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_fk_column)

        self.doubleSpinBox_fk_col = QDoubleSpinBox(self.verticalLayoutWidget)
        self.doubleSpinBox_fk_col.setObjectName(u"doubleSpinBox_fk_col")

        self.verticalLayout_4.addWidget(self.doubleSpinBox_fk_col)

        self.pushButton_fk_col = QPushButton(self.verticalLayoutWidget)
        self.pushButton_fk_col.setObjectName(u"pushButton_fk_col")
        self.pushButton_fk_col.setFont(font)

        self.verticalLayout_4.addWidget(self.pushButton_fk_col)

        self.graphicsView_fk_col = pg.PlotWidget(self.verticalLayoutWidget)
        self.graphicsView_fk_col.setObjectName(u"graphicsView_fk_col")

        self.verticalLayout_4.addWidget(self.graphicsView_fk_col)

        self.tabWidget.addTab(self.tab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"File path", None))
        self.pushButton_choose.setText(QCoreApplication.translate("MainWindow", u"Choose", None))
        self.label_file_type.setText(QCoreApplication.translate("MainWindow", u"Data format", None))
        self.comboBox_data_format.setItemText(0, QCoreApplication.translate("MainWindow", u"Digitizer Studio", None))
        self.comboBox_data_format.setItemText(1, QCoreApplication.translate("MainWindow", u"GAIL ML code", None))
        self.comboBox_data_format.setItemText(2, QCoreApplication.translate("MainWindow", u"QT GUI", None))

        self.pushButton_read_attr.setText(QCoreApplication.translate("MainWindow", u"Read Attributes", None))
        self.pushButton_process_file.setText(QCoreApplication.translate("MainWindow", u"Process data", None))
        self.label_proc_algo.setText(QCoreApplication.translate("MainWindow", u"Processing algorithm", None))
        self.comboBox_proc_algo.setItemText(0, QCoreApplication.translate("MainWindow", u"Conventional", None))
        self.comboBox_proc_algo.setItemText(1, QCoreApplication.translate("MainWindow", u"Kishore algorithm", None))

        self.label_glc.setText(QCoreApplication.translate("MainWindow", u"GLC window", None))
        self.label_hpf_order.setText(QCoreApplication.translate("MainWindow", u"HPF order", None))
        self.label_hpf_cutoff.setText(QCoreApplication.translate("MainWindow", u"HPF cutoff", None))
        self.label_window_size.setText(QCoreApplication.translate("MainWindow", u"STFT window size", None))
        self.label_stft_overlap.setText(QCoreApplication.translate("MainWindow", u"STFT overlap", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_file_attr), QCoreApplication.translate("MainWindow", u"File Attributes", None))
        self.label_row_no.setText(QCoreApplication.translate("MainWindow", u"Fast time trace number", None))
        self.pushButton_raw.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_raw), QCoreApplication.translate("MainWindow", u"Raw trace", None))
        self.checkBox_variance.setText(QCoreApplication.translate("MainWindow", u"Variance", None))
        self.checkBox_sat.setText(QCoreApplication.translate("MainWindow", u"SAT", None))
        self.checkBox_min_sat.setText(QCoreApplication.translate("MainWindow", u"Minimized SAT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_var), QCoreApplication.translate("MainWindow", u"Variance", None))
        self.label_wf_row.setText(QCoreApplication.translate("MainWindow", u"Enter Row", None))
        self.pushbutton_wfrow.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_wfcolumn.setText(QCoreApplication.translate("MainWindow", u"Enter Column", None))
        self.pushButton_wfcol.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_wf), QCoreApplication.translate("MainWindow", u"Waterfall", None))
        self.label_specrow.setText(QCoreApplication.translate("MainWindow", u"Enter Row", None))
        self.pushButton_specrow.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_speccol.setText(QCoreApplication.translate("MainWindow", u"Enter Column", None))
        self.pushButton_speccol.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_freq), QCoreApplication.translate("MainWindow", u"Spectrum", None))
        self.label_stftrow.setText(QCoreApplication.translate("MainWindow", u"Enter Row", None))
        self.pushButton_stftrow.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_stftcol.setText(QCoreApplication.translate("MainWindow", u"Enter Column", None))
        self.pushButton_stftcol.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_stft), QCoreApplication.translate("MainWindow", u"STFT", None))
        self.fk_label_row.setText(QCoreApplication.translate("MainWindow", u"Enter Row", None))
        self.pushButton_fk_row.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_fk_column.setText(QCoreApplication.translate("MainWindow", u"Enter Column", None))
        self.pushButton_fk_col.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"F-K Analysis", None))
    # retranslateUi

