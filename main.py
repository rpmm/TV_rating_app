import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPixmap

import urllib.request
from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from fetch_tv_data import get_tv_series_ratings


#An instance of QApplication
app = QApplication(sys.argv) 

# 3. Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle("TV Series Ratings (ALPHA)")
window.setGeometry(1000, 700, 800, 400) # x, y, width, height
layout = QHBoxLayout()
layout_vertical = QVBoxLayout()
layout.addLayout(layout_vertical)

# text widget
# msg = QLabel('Fetch the episode ratings of a TV series')
# msg.setAlignment(Qt.AlignHCenter)
# layout.addWidget(msg)

# Text field
text_field = QLineEdit('Enter series title')
text_field.setAlignment(Qt.AlignHCenter)
text_field.setFixedWidth(200)
layout_vertical.addWidget(text_field)

# For plotting
linecolors = ['r', 'g', 'b', 'c', 'm', 'y', 'w', 'k']

# Update to another tv-show
def update_graph():
    linecolor_counter = 0
    input_name = text_field.text()
    data = get_tv_series_ratings(input_name) # Get data to graph

    # If series data found succesfully
    if data != False:
        graphWidget.clear()
        graphWidget.setTitle(data[0])
        seasons_list = data[1]
        img_url = data[2]

        # Update poster
        data = urllib.request.urlopen(img_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QPixmap(image).scaledToWidth(200)
        label.setPixmap(pixmap)
        
        # Loop through all seasons
        for season_ratings in seasons_list:
            episode_indices = []
            episode_ratings = []
            for episode in season_ratings:
                if season_ratings[episode] != "N/A":
                    episode_indices.append(int(episode))
                    episode_ratings.append(float(season_ratings[episode]))
            
            # Plot season
            pen1 = pg.mkPen(linecolors[linecolor_counter], width = 4)
            graphWidget.setXRange(0, episode_indices[-1]+1, padding=0)
            # graphWidget.plot(episode_indices, episode_ratings, symbol="o", pen=pen1, symbolSize=6)
            graphWidget.plot(episode_indices, episode_ratings, pen=pen1)
            linecolor_counter += 1
    else:
        # Error dialog
        error_dialog = QMessageBox()
        error_dialog.setText('Invalid name!')
        error_dialog.exec_()

# Submit button
submit_btn = QPushButton('Submit')
submit_btn.clicked.connect(update_graph)
submit_btn.setFixedWidth(200)
layout_vertical.addWidget(submit_btn)

# Poster widget
label = QLabel()
pixmap = QPixmap('test.jpg').scaledToWidth(200)
label.setPixmap(pixmap)
layout_vertical.addWidget(label)

# PyQTgraph settings
pg.setConfigOption('background', None)
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Graph settings
graphWidget = pg.PlotWidget()
graphWidget.setLabel('left', 'Episode Rating')
graphWidget.setLabel('bottom', 'Episode Number')
graphWidget.setYRange(0,10.9, padding=0)
# graphWidget.setXRange(0,124, padding=0)
graphWidget.showGrid(x=True, y=True, alpha=0.1)
graphWidget.symbol="x"
graphWidget.symbolSize=6
layout.addWidget(graphWidget)

# Something?
window.setLayout(layout)
window.show() # 4. Show your application's GUI
sys.exit(app.exec_()) # "run the application until the user closes it"