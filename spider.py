# -*- coding: utf-8 -*-
# --------------------------------------
# Author:vicshine
# Date:2016-04-16
# Desc:spider博客采集器界面
# --------------------------------------
import sys
import time, uuid
from SpiderUI import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from save_chm import MakeChm
from spider_model import *
from s3_51cto import Spider_51CTO
from s3_cnblog import SpiderCnblogs
from s3_sina import SpiderSina
from s3_segmentfault import SpiderSegement
from s3_csdn import Spider_Csdn
from s3_runoob import SpiderRunoob


# 使用多线程操作，确保后台执行采集时前台界面不僵死
class WorkThread(QThread):
    def __int__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.tc = None
        self.mcm = None
        self.sourceUrl = None
        self.type = 1

    def setParam(self, tc, mcm, type, sourceUrl, saveImg, chmDir, delyTime, partlyNum, maxPage):
        self.mutex = QMutex()  # Locker
        self.tc = tc
        self.mcm = mcm
        self.type = type
        self.sourceUrl = sourceUrl
        #        self.tc.set_workHome(htmlDir)
        if (delyTime != -1):
            self.tc.set_dely(delyTime)
        if (maxPage != -1):
            self.tc.set_max_page(maxPage)
        self.mcm.set_save_img(saveImg)
        self.mcm.set_partlyNum(partlyNum)
        self.mcm.set_chm_path(chmDir)

    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        self.tc.get_urls(self.sourceUrl, self.type, self.mcm)
        self.tc.get_posts(self.mcm)
        self.emit(QtCore.SIGNAL('loadingEnd'))

    def log(self, value):
        self.emit(QtCore.SIGNAL("updateLog"), str(value))

    def stop(self):
        self.tc.stop_thread()
        with QMutexLocker(self.mutex):
            self.stoped = True


class SpiderClass(QtGui.QDialog, Ui_MainWindow):
    def __init__(self):
        print 'Spider init'
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.sourceUrl = None
        self.type = None
        self.partlyNum = 50
        self.pageNum = 3
        self.saveImg = 0
        self.delyTime = 3
        self.chmDir = None
        self.htmlDir = None
        self.topUrl = ''
        self.tc = SpiderSina(self)
        self.mcm = MakeChm()
        self.wk = None
        self.init()
        self.logFile = open('spider.log', 'w')

    def init(self):
        self.readSettings()
        self.browseChm.clicked.connect(self.showChmDialog)
        #        self.browseHTML.clicked.connect(self.showHTMLDialog)
        self.browseUrl.clicked.connect(self.updateUrl)
        self.startButton.clicked.connect(self.startLoad)
        self.stopButton.clicked.connect(self.stopLoad)
        self.sina_radio.clicked.connect(self.sina_select)
        self.cnblogs_radio.clicked.connect(self.cnblogs_select)
        self.csdn_radio.clicked.connect(self.csdn_select)
        self.cto_radio.clicked.connect(self.cto_select)
        self.seg_radio.clicked.connect(self.seg_select)
        # self.setWindowIcon(QtGui.QIcon(':/favico.ico'))

    # 初始化线程
    def initThread(self):
        self.wk = None
        self.wk = WorkThread()
        self.connect(self.wk, QtCore.SIGNAL("loadingEnd"), self.loadingEnd)

    # 开始线程处理
    def startThread(self):
        self.wk.setParam(self.tc, self.mcm, self.type, self.sourceUrl, self.saveImg, self.chmDir, self.delyTime,
                         self.partlyNum, self.pageNum)
        self.wk.start()

    def stopThread(self):
        self.wk.stop()
        self.disconnect(self.wk, QtCore.SIGNAL("loadingEnd"), self.loadingEnd)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        # self.disconnect(self.wk, QtCore.SIGNAL("updateLog"), self.log)
        # self.disconnect(self.wk, QtCore.SIGNAL("setVideoNum"), self.setVideoNum)
        # self.disconnect(self.wk, QtCore.SIGNAL("insertDownloadUrl"), self.insertDownloadUrl)

    def sina_select(self):
        #self.tc = SpiderSina(self)
        self.tc = SpiderRunoob(self)

    def cnblogs_select(self):
        self.tc = SpiderCnblogs(self)

    def csdn_select(self):
        self.tc = Spider_Csdn(self)

    def cto_select(self):
        self.tc = Spider_51CTO(self)

    def seg_select(self):
        self.tc = SpiderSegement(self)

    def updateUrl(self):
        self.sourceUrl = str(self.urlEdit.text())
        self.webView.load(QtCore.QUrl(self.sourceUrl))
        self.log(u'正在打开网址：' + self.sourceUrl + u'，请耐心等待！')

    def debug(self, log):
        if self.isDebug == 1:
            print log

    def readSettings(self):
        settings = QSettings('SpiderSetting')
        self.chmDir = str(settings.value('chmDir').toString())
        #        self.htmlDir = str(settings.value('htmlDir').toString())
        self.sourceUrl = str(settings.value('sourceUrl').toString())
        self.chmEdit.setText(self.chmDir)
        self.urlEdit.setText(self.sourceUrl)
        # self.htmlEdit.setText(self.htmlDir)

    def writeSettings(self):
        settings = QSettings('SpiderSetting')
        settings.setValue('chmDir', self.chmDir)
        # settings.setValue('htmlDir', self.htmlDir)
        settings.setValue('sourceUrl', self.sourceUrl)

    def showChmDialog(self):
        file_Name = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', self.chmDir)
        if ('' != file_Name):
            self.chmDir = str(file_Name)
        self.chmEdit.setText(self.chmDir)

    #    def showHTMLDialog(self):
    #        #QtGui.QFileDialog.getOpenFileNameAndFilter()
    #        file_Name = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', self.htmlDir)
    #        if ('' != file_Name):
    #            self.htmlDir = str(file_Name)
    #        self.htmlEdit.setText(self.htmlDir)

    def startLoad(self):

        self.log(u'正在获取参数，请稍后！')
        # 获取链接
        self.sourceUrl = str(self.urlEdit.text())
        # 获取链接类型
        type = self.type_combo.currentIndex()
        if (type == 1):
            self.type = 1
        else:
            self.type = 2
        # 获取最大采集页数
        pageNum = self.pageNum_combo.currentIndex() + 1
        if (pageNum == 7):
            self.pageNum = -1
        else:
            self.pageNum = pageNum
        # 获取是否保存图片
        saveImg = self.saveImg_combo.currentIndex()
        self.saveImg = saveImg
        # 获取采集间隔
        delyTime = self.dely_combo.currentIndex() + 1
        if (delyTime == 7):
            self.delyTime = -1
        else:
            self.delyTime = delyTime
        # 获取每个chm文件储存文章数量partlyNum_combo
        partlyNum = self.partlyNum_combo.currentIndex() + 1
        self.partlyNum = partlyNum * 10
        self.log(u'每个chm文件的最大文章个数为：' + str(self.partlyNum))

        # 获取chm地址
        self.chmDir = str(self.chmEdit.text())
        # 获取html地址
        #        self.htmlDir=str(self.htmlEdit.text())

        # 启动线程，开始处理
        self.log(u'参数获取成功，开始采集线程！')
        self.initThread()
        self.startThread()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stopLoad(self):
        self.stopThread()
        self.loadingEnd()

    def loadingEnd(self):
        self.log(u'文章采集完成，线程正常退出！')
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def log(self, log):
        tm = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
        log = '[' + tm + ']:' + log
        self.logLabel.setText(log)
        self.logFile.write(log + '\n')
        self.logFile.flush()

    def setLcdNum(self, num):
        self.lcdNumber.display(num)

    def setTopUrl(self, url):
        self.webView.load(QtCore.QUrl(url))

    def closeEvent(self, QCloseEvent):
        self.writeSettings()
        self.logFile.close()

    def __del__(self):
        self.writeSettings()
        self.logFile.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # splash=QtGui.QSplashScreen(QtGui.QPixmap(':/tumload.png'))
    # splash.show()
    # splash = SplashScreen()
    # splash.effective()
    # splash.effect()
    # splash.effect_show()
    #app.processEvents()
    window = SpiderClass()
    # splash.checkEnd()
    window.show()
    # splash.finish(window)
    sys.exit(app.exec_())
