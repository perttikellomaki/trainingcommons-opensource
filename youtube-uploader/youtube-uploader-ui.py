#!/usr/bin/python

import sys
import re
import subprocess
from PySide import QtGui
import EXIF

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        doc = QtGui.QTextDocument()
        doc.setHtml("Hello world")
        viewer = QtGui.QTextEdit()
        viewer.setDocument(doc)
        viewer.setReadOnly(True)
        chooseFileButton = QtGui.QPushButton("Pick file")
        chooseFileButton.clicked.connect(self.showDialog)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(chooseFileButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(viewer)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Training Commons YouTube uploader')
        self.show()
        
    def showDialog(self):

        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Choose file',
                    '/home')

        exiftool = subprocess.Popen(['exiftool', '-DateTimeOriginal', fname],
                                    shell = False, 
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
        stdout, stderr = exiftool.communicate()
        
        print stdout
        m = re.match("Date/Time Original\s*:\s*(\d*):(\d*):(\d*)\s*(\d*):(\d*):(\d*)", str(stdout))
        year = m.group(1)
        month = m.group(2)
        day = m.group(3)
        hours = m.group(4)
        minutes = m.group(5)
        seconds = m.group(6)

        print year
        print month
        print day
        print hours
        print minutes
        print seconds

        args = ["./youtube-uploader.py",
                "--file=%s" % fname,
                "--title=%s" % "Training Commons upload",
                "--description=Timestamp %s-%s-%s %s:%s:%s" 
                % (year, month, day, hours, minutes, seconds)]

        print args

        uploader = subprocess.Popen(args, shell=False)

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
#
#if __name__ == '__main__':
#  parser = OptionParser()
#  parser.add_option("--file", dest="file", help="Video file to upload")
#  parser.add_option("--title", dest="title", help="Video title",
#    default="Test Title")
#  parser.add_option("--description", dest="description", help="Video description",
#    default="Test Description")
#  parser.add_option("--category", dest="category", help="Video category",
#    default="22")
#  parser.add_option("--keywords", dest="keywords",
#    help="Video keywords, comma separated", default="")
#  parser.add_option("--privacyStatus", dest="privacyStatus", help="Video privacy status",
#    default="unlisted")
#  (options, args) = parser.parse_args()
#
#  if options.file is None or not os.path.exists(options.file):
#    exit("Please specify a valid file using the --file= parameter.")
#  else:
#    initialize_upload(options)
