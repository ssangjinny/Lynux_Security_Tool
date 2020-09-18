import sys
import os
import os.path
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QApplication(sys.argv)


class windows(QMainWindow):  # 메인 윈도우 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.a = Apache_modal()
        self.c = Chkrootkit_modal()
        self.l = Lynis_modal()
        self.cl = Clamav_modal()
        self.ac = ApacheCheck()
        self.clamav.clicked.connect(self.clam)
        self.chkrootkit.clicked.connect(self.chk)
        self.apache.clicked.connect(self.apa)
        self.lynis.clicked.connect(self.lyn)

    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(490, 480)
        window.setMaximumSize(QSize(1000, 1000))
        icon = QIcon("icons/icon.ico")
        window.setWindowIcon(icon)
        self.centralwidget = QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.clamav = QPushButton(self.centralwidget)
        self.clamav.setGeometry(QRect(30, 20, 200, 200))
        icon1 = QIcon("icons/clamav.png")
        self.clamav.setIcon(icon1)
        self.clamav.setIconSize(QSize(200, 200))
        self.clamav.setObjectName("clamav")
        self.chkrootkit = QPushButton(self.centralwidget)
        self.chkrootkit.setGeometry(QRect(260, 20, 200, 200))
        icon2 = QIcon("icons/chkrootkit.png")
        self.chkrootkit.setIcon(icon2)
        self.chkrootkit.setIconSize(QSize(150, 180))
        self.chkrootkit.setObjectName("chkrootkit")
        self.apache = QPushButton(self.centralwidget)
        self.apache.setGeometry(QRect(30, 250, 200, 200))
        icon3 = QIcon("icons/apache.png")
        self.apache.setIcon(icon3)
        self.apache.setIconSize(QSize(200, 200))
        self.apache.setObjectName("apache")
        self.lynis = QPushButton(self.centralwidget)
        self.lynis.setGeometry(QRect(260, 250, 200, 200))
        icon4 = QIcon("icons/lynis.png")
        self.lynis.setIcon(icon4)
        self.lynis.setIconSize(QSize(200, 200))
        self.lynis.setObjectName("lynis")
        window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.retranslateUi(window)
        QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Main"))

    def timesleep(self):  # 시간 지연 함수
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)  # msec
        loop.exec_()

    def clam(self):  # 코모도 버튼 클릭 시 발생 함수
        self.cl.textBrowser.clear()
        self.cl.show()
        file = "/usr/bin/clamscan"
        if not os.path.isfile(file):
            self.cl.textBrowser.append("Clamav가 설치되지 않았습니다. 설치파일을 실행해주세요.")
            self.cl.clamavbutton.setDisabled(True)

        else:
            self.cl.textBrowser.append("Clamav 바이러스 검사입니다.")
            self.cl.textBrowser.append("검사 할 디렉토리를 지정해주세요. (default : /)")

    def chk(self):  # 체크루트킷 버튼 클릭 시 발생 함수
        self.c.textBrowser.clear()
        self.c.show()
        file = "/usr/sbin/chkrootkit"
        if not os.path.isfile(file):
            self.c.textBrowser.append("Chkrootkit이 설치되지 않았습니다. 설치파일을 실행해주세요.")
            self.c.clamavbutton.setDisabled(True)

        else:
            self.c.textBrowser.append("Chkrootkit 루트 킷 검사입니다.")

    def apa(self):  # 아파치 버튼 클릭 시 발생 함수
        self.a.textBrowser.clear()
        self.a.bu.setDisabled(True)
        self.a.server.setDisabled(True)
        self.a.server2.setDisabled(True)
        self.a.sl.setDisabled(True)
        self.a.dir.setDisabled(True)
        self.a.error.setDisabled(True)
        self.a.show()
        if self.ac.isthis == 0:
            self.a.textBrowser.append("Apache가 설치되지 않았습니다. 설치파일을 실행해주세요.")

        else:
            self.a.textBrowser.append("아파치 보안 설정 툴입니다.")
            self.a.textBrowser.append("보안 취약점을 검사합니다.")
            self.timesleep()
            result = self.ac.startCheckApache()
            self.check(result)
            self.a.bu.setEnabled(True)

    def lyn(self):  # 리니스 버튼 클릭 시 발생 함수
        self.l.textBrowser.clear()
        self.l.show()
        file = "/usr/sbin/lynis"
        if not os.path.isfile(file):
            self.l.textBrowser.append("lynis가 설치되지 않았습니다. 설치파일을 실행해주세요.")
            self.l.Lynisbutton.setDisabled(True)

        else:
            self.l.textBrowser.append("리니스 보안 설정 검사입니다.")

    def check(self, result = []):
        flag = 0
        if result[0] == 0:
            self.a.server.setDisabled(True)
            self.a.textBrowser.append("ServerTokens가 OS로 설정되어 있지 않습니다.")

        else:
            self.a.textBrowser.append("ServerTokens가 OS로 설정되어 있어 보안에 취약합니다.")
            self.a.server.setEnabled(True)
            flag = flag + 1

        self.timesleep()
        if result[1] == 0:
            self.a.server2.setDisabled(True)
            self.a.textBrowser.append("ServerSignature가 ON으로 설정되어 있지 않습니다.")

        else:
            self.a.textBrowser.append("ServerSignature가 ON으로 설정되어 있어 보안에 취약합니다.")
            self.a.server2.setEnabled(True)
            flag = flag + 1

        self.timesleep()
        if result[2] == 0:
            self.a.sl.setDisabled(True)
            self.a.textBrowser.append("심볼릭 링크가 설정되어 있지 않습니다.")

        else:
            self.a.textBrowser.append("심볼릭 링크가 설정되어 있어 보안에 취약합니다.")
            self.a.sl.setEnabled(True)
            flag = flag + 1

        self.timesleep()
        if result[3] == 0:
            self.a.dir.setDisabled(True)
            self.a.textBrowser.append("디렉터리 인덱싱이 되어 있지 않습니다.")

        else:
            self.a.textBrowser.append("디렉터리 인덱싱이 되어 있어 보안에 취약합니다.")
            self.a.dir.setEnabled(True)
            flag = flag + 1

        self.timesleep()
        if result[4] == 0:
            self.a.error.setDisabled(True)
            self.a.textBrowser.append("에러 페이지가 설정 되어 있습니다.")

        else:
            self.a.textBrowser.append("에러 페이지가 설정 되어 있지 않아 보안에 취약합니다.")
            self.a.error.setEnabled(True)
            flag = flag + 1
        self.a.textBrowser.append("총 " + str(flag) + "개의 보안 취약점이 발견되었습니다.")


class Clamav_modal(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.f = FilePath()
        self.toolButton.clicked.connect(self.file)
        self.clamavbutton.clicked.connect(self.Clamav_def)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(297, 314)
        Dialog.setModal(True)
        icon = QIcon("icons/clamav.png")
        self.setWindowIcon(icon)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QRect(9, 39, 281, 231))
        self.textBrowser.setObjectName("textBrowser")
        self.clamavbutton = QPushButton(Dialog)
        self.clamavbutton.setEnabled(True)
        self.clamavbutton.setGeometry(QRect(9, 274, 281, 31))
        self.clamavbutton.setObjectName("clamavbutton")
        self.toolButton = QToolButton(Dialog)
        self.toolButton.setGeometry(QRect(260, 10, 27, 21))
        self.toolButton.setObjectName("toolButton")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setGeometry(QRect(10, 10, 241, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Clamav"))
        self.clamavbutton.setText(_translate("Dialog", "START"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.lineEdit.setText(_translate("Dialog", "/"))

    def timesleep(self):  # 시간 지연 함수
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)  # msec
        loop.exec_()

    def Clamav_def(self):
        self.clamavbutton.setDisabled(True)
        self.toolButton.setDisabled(True)
        i = 0
        t = time.localtime(time.time())
        st = time.strftime('%m%d%H%M%S', t) + ""
        string = "logs/Clamav/Clamav_" + st + ".log"
        pt = self.lineEdit.text()
        self.textBrowser.append("바이러스 검사 중...")
        self.timesleep()
        os.system("clamscan -ri " + pt + " > " + string)
        self.timesleep()
        result = open(string, 'r')
        txt = result.readlines()
        while i < len(txt):
            inf = str(txt[i])
            if "Infected" in inf:
                self.textBrowser.append(inf.replace("Infected files", "감염된 파일 "))
            i = i + 1

        self.textBrowser.append("바이러스 검사가 끝났습니다.")
        self.textBrowser.append("자세한 결과는 로그 파일을 참조하세요.")
        self.clamavbutton.setEnabled(True)
        self.toolButton.setEnabled(True)

    def file(self):
        self.lineEdit.clear()
        path = self.f.directory_select()
        self.lineEdit.setText(path)


class FilePath(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'File Path'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def directory_select(self):
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "select Directory")
        return directory_path


class Chkrootkit_modal(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chkbutton.clicked.connect(self.Chkrootkit_def)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(298, 314)
        Dialog.setModal(True)
        icon = QIcon("icons/chkrootkit.png")
        self.setWindowIcon(icon)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QRect(9, 9, 281, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.chkbutton = QPushButton(Dialog)
        self.chkbutton.setEnabled(True)
        self.chkbutton.setGeometry(QRect(9, 274, 281, 31))
        self.chkbutton.setObjectName("chkbutton")
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chkrootkit"))
        self.chkbutton.setText(_translate("Dialog", "START"))

    def timesleep(self):  # 시간 지연 함수
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)  # msec
        loop.exec_()

    def Chkrootkit_def(self):
        self.chkbutton.setDisabled(True)
        t = time.localtime(time.time())
        st = time.strftime('%m%d%H%M%S', t) + ""
        string = "logs/Chkrootkit/Chkrootkit_" + st + ".log"
        self.textBrowser.append("루트 킷 검사 중...")
        self.timesleep()
        os.system("sudo chkrootkit > " + string)
        file = open(string, 'r')
        result = file.readlines()
        i = 0
        flag = 0
        while i == len(result):
            i = i + 1
            if result[i] in "INFECTED":
                inf = str(result[i])
                self.textBrowser.append(inf)
                flag += 1

        self.textBrowser.append("변조된 파일이 " + str(flag) + "개 있습니다.")
        self.textBrowser.append("루트 킷 검사가 끝났습니다.")
        self.textBrowser.append("자세한 검사 내역은 로그 파일을 참조하세요.")
        self.chkbutton.setEnabled(True)


class ApacheCheck:

    def __init__(self):
        self.isthis = -1

        isthisdebian = os.path.isfile("/etc/apache2/apache2.conf")
        if isthisdebian:
            self.isthis = 1
        else:
            self.isthis = 0

        # Check ServerToken

    def checkServerTokens(self):
        os.system("cat /etc/apache2/conf-available/security.conf | grep \'ServerTokens OS\' > ./checkServerTokens")
        f = open("./checkServerTokens", "r")
        checkservertokens = f.readline()
        if checkservertokens == "":
            f.close()
            os.system("rm -r ./checkServerTokens")
            return 0
        else:
            f.close()
            os.system("rm -r ./checkServerTokens")
            return 1

    def checkServerSignature(self):
        os.system(
            "cat /etc/apache2/conf-available/security.conf | grep \'ServerSignature On\' > ./checkServerSignature")
        f = open("./checkServerSignature", "r")
        checkservertokens = f.readline()
        if checkservertokens == "":
            f.close()
            os.system("rm -r ./checkServerSignature")
            return 0
        else:
            f.close()
            os.system("rm -r ./checkServerSignature")
            return 1

    # Check FollowSymLinks

    def checkFollowSymLinks(self):
        os.system("cat /etc/apache2/apache2.conf | grep \'<Directory /var/www/>\' -C 1 > ./checkFollowSymLinks")
        os.system("cat ./checkFollowSymLinks | grep FollowSymLinks > ./checkFollowSymLinks2")
        f = open("./checkFollowSymLinks2", "r")
        checkfollowsymlinks = f.readline()

        if checkfollowsymlinks == "":
            f.close()
            os.system("rm -r ./checkFollowSymLinks ./checkFollowSymLinks2")
            return 0
        else:
            os.system("rm -r ./checkFollowSymLinks ./checkFollowSymLinks2")
            f.close()
            return 1

    # Check Directory Indexing

    def checkIndexing(self):
        os.system("cat -n /etc/apache2/apache2.conf | grep \'<Directory /var/www/>\' -C 1 > ./checkIndexing")
        os.system("cat ./checkIndexing | grep Indexes > ./checkIndexing2")
        f = open("./checkIndexing2", "r")
        checkindexing = f.readline()
        if checkindexing == "":
            f.close()
            os.system("rm -r ./checkIndexing ./checkIndexing2")
            return 0
        else:
            f.close()
            os.system("rm -r ./checkIndexing ./checkIndexing2")
            return 1

    def checkErrorDocument(self):
        os.system("cat /etc/apache2/sites-available/000-default.conf | grep \'Errordocument\' > ./checkErrorDocument")
        f = open("./checkErrorDocument", "r")
        checkindexing = f.readline()
        if checkindexing == "":
            f.close()
            os.system("rm -r ./checkErrorDocument")
            return 1
        else:
            f.close()
            os.system("rm -r ./checkErrorDocument")
            return 0

    # Controller Method

    def startCheckApache(self):
        if self.isthis == 1:
            result = [self.checkServerTokens(), self.checkServerSignature(), self.checkFollowSymLinks(),
                      self.checkIndexing(), self.checkErrorDocument()]
            return result

        else:
            print("Apache is not installed.")
            return -1


class SetApacheOptions:

    def setServerTokens(self):
        os.system("cat -n /etc/apache2/conf-available/security.conf | grep \'ServerTokens OS\' > ./checkServerTokens")
        f = open("./checkServerTokens", "r")
        checkservertokens = f.readline()

        if checkservertokens == "":
            f.close()
            os.system("rm -r ./checkServerTokens")

        else:
            num = checkservertokens.split(' ')[4].split('	')[0].strip('\n')
            os.system("sed -i \'" + num + "s/OS/Prod/\' /etc/apache2/conf-available/security.conf")
            f.close()
            os.system("rm -r ./checkServerTokens")

    def setServerSignature(self):
        os.system(
            "cat -n /etc/apache2/conf-available/security.conf | grep \'ServerSignature On\' > ./checkServerSignature")
        f = open("./checkServerSignature", "r")
        checkserversignature = f.readline()

        if checkserversignature == "":
            f.close()
            os.system("rm -r ./checkServerSignature")

        else:
            num = checkserversignature.split(' ')[4].split('	')[0].strip('\n')
            os.system("sed -i \'" + num + "s/On/Off/\' /etc/apache2/conf-available/security.conf")
            f.close()
            os.system("rm -r ./checkServerSignature")

    # Set FollowSymLinks

    def setFollowSymLinks(self):
        os.system("cat -n /etc/apache2/apache2.conf | grep \'<Directory /var/www/>\' -C 1 > ./checkFollowSymLinks")
        os.system("cat ./checkFollowSymLinks | grep FollowSymLinks > ./checkFollowSymLinks2")
        f = open("./checkFollowSymLinks2", "r")
        checkfollowsymlinks = f.readline()

        if checkfollowsymlinks == "":
            f.close()
            os.system("rm -r ./checkFollowSymLinks ./checkFollowSymLinks2")
        else:
            num = checkfollowsymlinks.split(' ')[3].split('	')[0].strip('\n')
            os.system("sed -i \'" + num + "s/FollowSymLinks/ /\' /etc/apache2/apache2.conf")
            f.close()

    # set Directory Indexing

    def setIndexing(self):
        os.system("cat -n /etc/apache2/apache2.conf | grep \'<Directory /var/www/>\' -C 1 > ./checkIndexing")
        os.system("cat ./checkIndexing | grep Indexes > ./checkIndexing2")
        f = open("./checkIndexing2", "r")
        checkindexing = f.readline()
        if checkindexing == "":
            f.close()
            os.system("rm -r ./checkIndexing ./checkIndexing2")
        else:
            num = checkindexing.split(' ')[3].split('	')[0].strip('\n')
            os.system("sed -i \'" + num + "s/Indexes/ /\' /etc/apache2/apache2.conf")
            f.close()
            os.system("rm -r ./checkIndexing ./checkIndexing2")

    def setErrorDocument(self):
        os.system(
            "cat -n /etc/apache2/sites-available/000-default.conf | grep \'</VirtualHost>\' > ./checkErrorDocument")
        f = open("./checkErrorDocument", "r")
        checkerrordocument = f.readline()
        num = checkerrordocument.split(' ')[4].split('	')[0].strip('\n')
        os.system("sed -i \'" + num + "s/<\/VirtualHost>/ /\' /etc/apache2/sites-available/000-default.conf")
        os.system("echo \'      Errordocument 403 \"/error.html\"\' >> /etc/apache2/sites-available/000-default.conf")
        os.system("echo \'      Errordocument 404 \"/error.html\"\' >> /etc/apache2/sites-available/000-default.conf")
        os.system("echo \'      Errordocument 500 \"/error.html\"\' >> /etc/apache2/sites-available/000-default.conf")
        os.system("echo \'</VirtualHost>\' >> /etc/apache2/sites-available/000-default.conf")
        os.system("echo \'error!!\' > /var/www/html/error.html")
        f.close()
        os.system("rm -r ./checkErrorDocument")


class Apache_modal(QDialog):  # 아파치 모달 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 4
        self.sao = SetApacheOptions()
        self.bu.clicked.connect(self.Apache_def)

    def setupUi(self, Form):  # GUI 설정 함수
        Form.setObjectName("Form")
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(298, 406)
        Form.setMaximumSize(QSize(1000, 1000))
        icon = QIcon("icons/apache.png")
        self.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.server = QCheckBox(Form)
        self.server.setObjectName("server")
        self.gridLayout.addWidget(self.server, 2, 0, 1, 1)
        self.server2 = QCheckBox(Form)
        self.server2.setObjectName("server2")
        self.gridLayout.addWidget(self.server2, 3, 0, 1, 1)
        self.sl = QCheckBox(Form)
        self.sl.setObjectName("sl")
        self.gridLayout.addWidget(self.sl, 4, 0, 1, 1)
        self.dir = QCheckBox(Form)
        self.dir.setObjectName("dir")
        self.gridLayout.addWidget(self.dir, 5, 0, 1, 1)
        self.error = QCheckBox(Form)
        self.error.setObjectName("dir")
        self.gridLayout.addWidget(self.error, 6, 0, 1, 1)
        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.bu = QPushButton(Form)
        self.bu.setEnabled(True)
        self.bu.setObjectName("bu")
        self.gridLayout.addWidget(self.bu, 7, 0, 1, 1)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):  # 이름 재설정 함수
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Apache"))
        self.server.setText(_translate("Form", "서버 정보 노출(ServerTokens)"))
        self.server2.setText(_translate("Form", "서버 정보 노출(ServerSignature)"))
        self.sl.setText(_translate("Form", "심볼릭 링크"))
        self.dir.setText(_translate("Form", "디렉토리 인덱싱"))
        self.error.setText(_translate("Form", "에러페이지 설정"))
        self.bu.setText(_translate("Form", "START"))

    def timesleep(self):  # 시간 지연 함수
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)  # msec
        loop.exec_()
        
    def Apache_def(self):  # 스타트 클릭 시 발생 함수
        flag = 0
        self.bu.setDisabled(True)
        if self.server.isChecked():
            self.sao.setServerTokens()
            self.textBrowser.append("서버 정보 노출(ServerTokens) 설정중...")
            self.timesleep()
        else:
            flag = flag + 1
        if self.server2.isChecked():
            self.sao.setServerSignature()
            self.textBrowser.append("서버 정보 노출(ServerSignature) 설정중...")
            self.timesleep()
        else:
            flag = flag + 1
        if self.sl.isChecked():
            self.sao.setFollowSymLinks()
            self.textBrowser.append("심볼릭 링크 설정중...")
            self.timesleep()
        else:
            flag = flag + 1
        if self.dir.isChecked():
            self.sao.setIndexing()
            self.textBrowser.append("디렉토리 인덱싱 설정중...")
            self.timesleep()
        else:
            flag = flag + 1
        if self.error.isChecked():
            self.sao.setErrorDocument()
            self.textBrowser.append("에러 페이지 설정중...")
            self.timesleep()
        else:
            flag = flag + 1
        if flag == 5:
            self.textBrowser.append("원하시는 보안 설정을 체크해주세요.")
            self.bu.setEnabled(True)
        else:
            e = ApacheMessageBox()
            if e.close():
                self.close()

            self.bu.setEnabled(True)
            self.textBrowser.clear()
            self.server.setChecked(False)
            self.server2.setChecked(False)
            self.error.setChecked(False)
            self.sl.setChecked(False)
            self.dir.setChecked(False)


class Lynis_modal(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 4
        self.Lynisbutton.clicked.connect(self.Lynis_def)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(297, 314)
        Dialog.setModal(True)
        icon = QIcon("icons/lynis.png")
        self.setWindowIcon(icon)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QRect(9, 9, 281, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.Lynisbutton = QPushButton(Dialog)
        self.Lynisbutton.setEnabled(True)
        self.Lynisbutton.setGeometry(QRect(9, 274, 281, 31))
        self.Lynisbutton.setObjectName("Lynisbutton")
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lynis"))
        self.Lynisbutton.setText(_translate("Dialog", "START"))

    def timesleep(self):  # 시간 지연 함수
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)  # msec
        loop.exec_()

    def Lynis_def(self):
        self.Lynisbutton.setDisabled(True)
        t = time.localtime(time.time())
        st = time.strftime('%m%d%H%M%S', t) + ""
        string = "logs/Lynis/Lynis_" + st + ".log"
        self.textBrowser.append("검사를 진행 중입니다...")
        self.timesleep()
        os.system("sudo lynis audit system")
        self.timesleep()
        self.textBrowser.append("검사 완료!")
        os.system("echo '검사 완료'")
        self.textBrowser.append("WARNING")
        l_log = open(string, "w+")
        os.system("cat /var/log/lynis-report.dat | grep 'warning' | sed -e 's/warning\[\]\=//g' > " + string)
        result_log = l_log.read()
        self.textBrowser.append(result_log)
        l_log.close()
        self.textBrowser.append('더욱 자세한 사항을 알고 싶다면 "/var/log/lynis-report.dat"를 참고하십시오!')
        self.Lynisbutton.setEnabled(True)


class ApacheMessageBox(QWidget):  # 대화 상자 클래스
    def __init__(self):
        super().__init__()
        self.title = 'Complete'
        self.left = 600
        self.top = 300
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        QMessageBox.question(self, '설정완료', "설정이 완료되었습니다.", QMessageBox.Yes)


w = windows()
w.show()
app.exec_()

