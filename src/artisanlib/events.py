# -*- coding: utf-8 -*-
#
# ABOUT
# Artisan Events Dialog

# LICENSE
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# AUTHOR
# Marko Luther, 2020

import sys
import platform
import prettytable

from artisanlib.util import uchr
from artisanlib.dialogs import ArtisanResizeablDialog, ArtisanDialog
from artisanlib.widgets import MyQComboBox

from help import eventannotations_help
from help import eventbuttons_help
from help import eventsliders_help

try:
    #pylint: disable = E, W, R, C
    from PyQt6.QtCore import (Qt, pyqtSlot, QSettings, QCoreApplication) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt6.QtGui import (QColor, QFont, QIntValidator) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, # @UnusedImport @Reimport  @UnresolvedImport
                                 QPushButton, QSpinBox, QDoubleSpinBox, QWidget, QTabWidget, QDialogButtonBox, # @UnusedImport @Reimport  @UnresolvedImport
                                 QGridLayout, QGroupBox, QTableWidget, QHeaderView) # @UnusedImport @Reimport  @UnresolvedImport
except Exception:
    #pylint: disable = E, W, R, C
    from PyQt5.QtCore import (Qt, pyqtSlot, QSettings, QCoreApplication) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt5.QtGui import (QColor, QFont, QIntValidator) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, # @UnusedImport @Reimport  @UnresolvedImport
                                 QPushButton, QSpinBox, QDoubleSpinBox, QWidget, QTabWidget, QDialogButtonBox, # @UnusedImport @Reimport  @UnresolvedImport
                                 QGridLayout, QGroupBox, QTableWidget, QHeaderView) # @UnusedImport @Reimport  @UnresolvedImport


class EventsDlg(ArtisanResizeablDialog):
    def __init__(self, parent = None, aw = None, activeTab = 0):
        super().__init__(parent, aw)
        
        self.app = QCoreApplication.instance()
        
        titlefont = QFont()
        titlefont.setBold(True)
        titlefont.setWeight(75)
        self.setWindowTitle(QApplication.translate("Form Caption","Events"))
        self.setModal(True)
        self.helpdialog = None
        settings = QSettings()
        if settings.contains("EventsGeometry"):
            self.restoreGeometry(settings.value("EventsGeometry"))
        
        self.storeState()

        ## TAB 7
        showAnnoLabel = QLabel()
        showAnnoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        showAnnoLabel.setText(QApplication.translate("Label", "Show"))
        showAnnoLabel.setFont(titlefont)
        AnnoLabel = QLabel()
        AnnoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        AnnoLabel.setText(QApplication.translate("Label", "Annotation"))
        AnnoLabel.setFont(titlefont)

        Epreview1Label = QLabel()
        Epreview1Label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        Epreview1Label.setText(QApplication.translate("Label", "Example before FCs"))
        Epreview1Label.setFont(titlefont)
        Epreview2Label = QLabel()
        Epreview2Label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        Epreview2Label.setText(QApplication.translate("Label", "Example after FCs"))
        Epreview2Label.setFont(titlefont)

        self.E1AnnoVisibility = QCheckBox(self.aw.qmc.etypesf(0))
        self.E1AnnoVisibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1AnnoVisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[0]))
        self.E2Annovisibility = QCheckBox(self.aw.qmc.etypesf(1))
        self.E2Annovisibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[1]))
        self.E3Annovisibility = QCheckBox(self.aw.qmc.etypesf(2))
        self.E3Annovisibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[2]))
        self.E4Annovisibility = QCheckBox(self.aw.qmc.etypesf(3))
        self.E4Annovisibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[3]))

        self.E1Edit = QLineEdit(self.aw.qmc.specialeventannotations[0])
        self.E1Edit.setMinimumSize(self.E1Edit.sizeHint())
        self.E1Edit.textChanged.connect(self.changeSpecialeventEdit1)
        self.E1Edit.setToolTip(QApplication.translate("Tooltip", "Definition string for special event annotation"))
        self.E1Preview1 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E1Edit.text(),eventnum=0,applyto="preview",postFCs=False))
        self.E1Preview2 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E1Edit.text(),eventnum=0,applyto="preview",postFCs=True))

        self.E2Edit = QLineEdit(self.aw.qmc.specialeventannotations[1])
        self.E2Edit.setMinimumSize(self.E2Edit.sizeHint())
        self.E2Edit.textChanged.connect(self.changeSpecialeventEdit2)
        self.E2Edit.setToolTip(QApplication.translate("Tooltip", "Definition string for special event annotation"))
        self.E2Preview1 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E2Edit.text(),eventnum=0,applyto="preview",postFCs=False))
        self.E2Preview2 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E2Edit.text(),eventnum=0,applyto="preview",postFCs=True))

        self.E3Edit = QLineEdit(self.aw.qmc.specialeventannotations[2])
        self.E3Edit.setMinimumSize(self.E3Edit.sizeHint())
        self.E3Edit.textChanged.connect(self.changeSpecialeventEdit3)
        self.E3Edit.setToolTip(QApplication.translate("Tooltip", "Definition string for special event annotation"))
        self.E3Preview1 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E3Edit.text(),eventnum=0,applyto="preview",postFCs=False))
        self.E3Preview2 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E3Edit.text(),eventnum=0,applyto="preview",postFCs=True))

        self.E4Edit = QLineEdit(self.aw.qmc.specialeventannotations[3])
        self.E4Edit.setMinimumSize(self.E4Edit.sizeHint())
        self.E4Edit.textChanged.connect(self.changeSpecialeventEdit4)
        self.E4Edit.setToolTip(QApplication.translate("Tooltip", "Definition string for special event annotation"))
        self.E4Preview1 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E4Edit.text(),eventnum=0,applyto="preview",postFCs=False))
        self.E4Preview2 = QLabel(self.aw.qmc.parseSpecialeventannotation(self.E4Edit.text(),eventnum=0,applyto="preview",postFCs=True))

        #tab 7
        eventannoLayout = QGridLayout()
        eventannoLayout.addWidget(showAnnoLabel, 0,0,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(AnnoLabel,     0,1,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(Epreview1Label,0,2,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(Epreview2Label,0,3,Qt.AlignmentFlag.AlignLeft)

        eventannoLayout.addWidget(self.E1AnnoVisibility,1,0)
        eventannoLayout.addWidget(self.E2Annovisibility,2,0)
        eventannoLayout.addWidget(self.E3Annovisibility,3,0)
        eventannoLayout.addWidget(self.E4Annovisibility,4,0)

        eventannoLayout.addWidget(self.E1Edit,1,1)
        eventannoLayout.addWidget(self.E2Edit,2,1)
        eventannoLayout.addWidget(self.E3Edit,3,1)
        eventannoLayout.addWidget(self.E4Edit,4,1)
        eventannoLayout.addWidget(self.E1Preview1,1,2,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E2Preview1,2,2,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E3Preview1,3,2,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E4Preview1,4,2,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E1Preview2,1,3,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E2Preview2,2,3,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E3Preview2,3,3,Qt.AlignmentFlag.AlignLeft)
        eventannoLayout.addWidget(self.E4Preview2,4,3,Qt.AlignmentFlag.AlignLeft)

        eventannoLayout.setColumnStretch(0,0)
        eventannoLayout.setColumnStretch(1,10)
        eventannoLayout.setColumnStretch(2,0)
        eventannoLayout.setColumnStretch(3,0)

        overlapeditLabel = QLabel(QApplication.translate("Label", "Allowed Annotation Overlap"))
        self.overlapEdit = QSpinBox()
        self.overlapEdit.setRange(0,100)    #(min,max)
        self.overlapEdit.setMinimumWidth(80)
        self.overlapEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.overlapEdit.setValue(self.aw.qmc.overlappct)
        self.overlapEdit.setSuffix(" %")
        
        helpcurveDialogButton = QDialogButtonBox()
        helpButton = helpcurveDialogButton.addButton(QDialogButtonBox.StandardButton.Help)
        self.setButtonTranslations(helpButton,"Help",QApplication.translate("Button","Help"))
        helpButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        helpButton.clicked.connect(self.showEventannotationhelp)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(overlapeditLabel)
        buttonLayout.addWidget(self.overlapEdit)
        buttonLayout.addStretch()
        buttonLayout.addWidget(helpButton)
        entryLayout = QHBoxLayout()
        entryLayout.addLayout(eventannoLayout)
        #entryLayout.addStretch()
        tab7Layout = QVBoxLayout()
        tab7Layout.addLayout(entryLayout)
        tab7Layout.addStretch()
        tab7Layout.addSpacing(10)
        tab7Layout.addLayout(buttonLayout)
        
        C7Widget = QWidget()
        C7Widget.setLayout(tab7Layout)

        ## TAB 1
        self.eventsbuttonflag = QCheckBox(QApplication.translate("CheckBox","Button"))
        self.eventsbuttonflag.setChecked(bool(self.aw.eventsbuttonflag))
        self.eventsbuttonflag.stateChanged.connect(self.eventsbuttonflagChanged)
        self.annotationsflagbox = QCheckBox(QApplication.translate("CheckBox","Annotations"))
        self.annotationsflagbox.setChecked(bool(self.aw.qmc.annotationsflag))
        self.annotationsflagbox.stateChanged.connect(self.annotationsflagChanged)
        self.showeventsonbtbox = QCheckBox(QApplication.translate("CheckBox","Show on BT"))
        self.showeventsonbtbox.setChecked(bool(self.aw.qmc.showeventsonbt))
        self.showeventsonbtbox.stateChanged.connect(self.showeventsonbtChanged)
        
        self.eventsclampflag = QCheckBox(QApplication.translate("CheckBox","Snap"))
        self.eventsclampflag.setChecked(bool(self.aw.qmc.clampEvents))
        self.eventsclampflag.stateChanged.connect(self.eventsclampflagChanged)
        self.eventslabelsflag = QCheckBox(QApplication.translate("CheckBox","Descr."))
        self.eventslabelsflag.setChecked(bool(self.aw.qmc.renderEventsDescr))
        self.eventslabelsflag.stateChanged.connect(self.eventslabelsflagChanged)
        self.eventslabelscharsSpinner = QSpinBox()
        self.eventslabelscharsSpinner.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.eventslabelscharsSpinner.setSingleStep(1)
        self.eventslabelscharsSpinner.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.eventslabelscharsSpinner.setRange(1,20)
        self.eventslabelscharsSpinner.setValue(self.aw.qmc.eventslabelschars)
        
        if self.aw.qmc.eventsGraphflag not in [2,3,4]:
            self.eventsclampflag.setEnabled(False)
        self.minieventsflag = QCheckBox(QApplication.translate("CheckBox","Mini Editor"))
        self.minieventsflag.setToolTip(QApplication.translate("Tooltip","Allows to enter a description of the last event"))
        self.minieventsflag.setChecked(bool(self.aw.minieventsflag))
        self.minieventsflag.stateChanged.connect(self.minieventsflagChanged)
        barstylelabel = QLabel(QApplication.translate("Label","Markers"))
        barstyles = ["",
                    QApplication.translate("ComboBox","Flag"),
                    QApplication.translate("ComboBox","Bar"),
                    QApplication.translate("ComboBox","Step"),
                    QApplication.translate("ComboBox","Step+"),
                    QApplication.translate("ComboBox","Combo")]
                    
        self.bartypeComboBox =  QComboBox()
        self.bartypeComboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#        self.bartypeComboBox.setMaximumWidth(80)
        self.bartypeComboBox.addItems(barstyles)
        if not self.aw.qmc.eventsshowflag:
            self.bartypeComboBox.setCurrentIndex(0)
        else:
            self.bartypeComboBox.setCurrentIndex(self.aw.qmc.eventsGraphflag+1)
        self.bartypeComboBox.currentIndexChanged.connect(self.eventsGraphTypeflagChanged)
        typelabel1 = QLabel("1")
        typelabel2 = QLabel("2")
        typelabel3 = QLabel("3")
        typelabel4 = QLabel("4")
        typelabel5 = QLabel("5")
        self.showEtype1 = QCheckBox()
        self.showEtype2 = QCheckBox()
        self.showEtype3 = QCheckBox()
        self.showEtype4 = QCheckBox()
        self.showEtype5 = QCheckBox()
        self.showEtype1.setChecked(self.aw.qmc.showEtypes[0])
        self.showEtype2.setChecked(self.aw.qmc.showEtypes[1])
        self.showEtype3.setChecked(self.aw.qmc.showEtypes[2])
        self.showEtype4.setChecked(self.aw.qmc.showEtypes[3])
        self.showEtype5.setChecked(self.aw.qmc.showEtypes[4])
        self.showEtype1.stateChanged.connect(self.changeShowEtypes0)         #toggle
        self.showEtype2.stateChanged.connect(self.changeShowEtypes1)         #toggle
        self.showEtype3.stateChanged.connect(self.changeShowEtypes2)         #toggle
        self.showEtype4.stateChanged.connect(self.changeShowEtypes3)         #toggle
        self.showEtype5.stateChanged.connect(self.changeShowEtypes4)         #toggle
        self.etype0 = QLineEdit(self.aw.qmc.etypesf(0))
        self.etype0.setCursorPosition(0)
        self.etype1 = QLineEdit(self.aw.qmc.etypesf(1))
        self.etype1.setCursorPosition(0)
        self.etype2 = QLineEdit(self.aw.qmc.etypesf(2))
        self.etype2.setCursorPosition(0)
        self.etype3 = QLineEdit(self.aw.qmc.etypesf(3))
        self.etype3.setCursorPosition(0)
        self.etype4 = QLabel("--      ")
        self.etype0.setMaximumWidth(60)
        self.etype1.setMaximumWidth(60)
        self.etype2.setMaximumWidth(60)
        self.etype3.setMaximumWidth(60)
        self.E1colorButton = QPushButton(self.aw.qmc.etypesf(0))
        self.E1colorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2colorButton = QPushButton(self.aw.qmc.etypesf(1))
        self.E2colorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3colorButton = QPushButton(self.aw.qmc.etypesf(2))
        self.E3colorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4colorButton = QPushButton(self.aw.qmc.etypesf(3))
        self.E4colorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1colorButton.clicked.connect(self.setcoloreventline0)
        self.E2colorButton.clicked.connect(self.setcoloreventline1)
        self.E3colorButton.clicked.connect(self.setcoloreventline2)
        self.E4colorButton.clicked.connect(self.setcoloreventline3)
        self.E1textcolorButton = QPushButton(self.aw.qmc.etypesf(0))
        self.E1textcolorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2textcolorButton = QPushButton(self.aw.qmc.etypesf(1))
        self.E2textcolorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3textcolorButton = QPushButton(self.aw.qmc.etypesf(2))
        self.E3textcolorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4textcolorButton = QPushButton(self.aw.qmc.etypesf(3))
        self.E4textcolorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1textcolorButton.clicked.connect(self.setcoloreventtext0)
        self.E2textcolorButton.clicked.connect(self.setcoloreventtext1)
        self.E3textcolorButton.clicked.connect(self.setcoloreventtext2)
        self.E4textcolorButton.clicked.connect(self.setcoloreventtext3)
        #marker selection for comboboxes
        self.markers = ["",
                        QApplication.translate("Marker","Circle"),
                        QApplication.translate("Marker","Square"),
                        QApplication.translate("Marker","Pentagon"),
                        QApplication.translate("Marker","Diamond"),
                        QApplication.translate("Marker","Star"),
                        QApplication.translate("Marker","Hexagon 1"),
                        QApplication.translate("Marker","Hexagon 2"),
                        QApplication.translate("Marker","+"),
                        QApplication.translate("Marker","x"),
                        QApplication.translate("Marker","None")]
        #keys interpreted by matplotlib. Must match order of self.markers 
        self.markervals = [None,"o","s","p","D","*","h","H","+","x","None"]
        #Marker type
        self.marker1typeComboBox =  QComboBox()
        self.marker1typeComboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.marker1typeComboBox.addItems(self.markers)
        if self.aw.qmc.EvalueMarker[0] in self.markervals:
            self.marker1typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[0]))
        else:
            self.marker1typeComboBox.setCurrentIndex(0) # set to first empty entry
        self.marker1typeComboBox.currentIndexChanged.connect(self.seteventmarker0)
        self.marker2typeComboBox =  QComboBox()
        self.marker2typeComboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.marker2typeComboBox.addItems(self.markers)
        if self.aw.qmc.EvalueMarker[1] in self.markervals:
            self.marker2typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[1]))
        else:
            self.marker2typeComboBox.setCurrentIndex(0) # set to first empty entry
        self.marker2typeComboBox.currentIndexChanged.connect(self.seteventmarker1)
        self.marker3typeComboBox =  QComboBox()
        self.marker3typeComboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.marker3typeComboBox.addItems(self.markers)
        if self.aw.qmc.EvalueMarker[2] in self.markervals:
            self.marker3typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[2]))
        else:
            self.marker3typeComboBox.setCurrentIndex(0) # set to first empty entry
        self.marker3typeComboBox.currentIndexChanged.connect(self.seteventmarker2)
        self.marker4typeComboBox =  QComboBox()
        self.marker4typeComboBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.marker4typeComboBox.addItems(self.markers)
        if self.aw.qmc.EvalueMarker[3] in self.markervals:
            self.marker4typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[3]))
        else:
            self.marker4typeComboBox.setCurrentIndex(0) # set to first empty entry
        self.marker4typeComboBox.currentIndexChanged.connect(self.seteventmarker3)
        valuecolorlabel = QLabel(QApplication.translate("Label","Color"))
        valuecolorlabel.setFont(titlefont)
        valuetextcolorlabel = QLabel(QApplication.translate("Label","Text Color"))
        valuetextcolorlabel.setFont(titlefont)
        valuesymbollabel = QLabel(QApplication.translate("Label","Marker"))
        valuesymbollabel.setFont(titlefont)
        valuethicknesslabel = QLabel(QApplication.translate("Label","Thickness"))
        valuethicknesslabel.setFont(titlefont)
        valuealphalabel = QLabel(QApplication.translate("Label","Opacity"))
        valuealphalabel.setFont(titlefont)
        valuesizelabel = QLabel(QApplication.translate("Label","Size"))
        valuesizelabel.setFont(titlefont)
        valuecolorlabel.setMaximumSize(80,20)
        valuetextcolorlabel.setMaximumSize(80,20)
        valuesymbollabel.setMaximumSize(70,20)
        valuethicknesslabel.setMaximumSize(80,20)
        valuealphalabel.setMaximumSize(80,20)
        valuesizelabel.setMaximumSize(80,20)
        self.E1thicknessSpinBox = QSpinBox()
        self.E1thicknessSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1thicknessSpinBox.setSingleStep(1)
        self.E1thicknessSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1thicknessSpinBox.setRange(1,10)
        self.E1thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[0])
        self.E1thicknessSpinBox.valueChanged.connect(self.setElinethickness0)
        self.E2thicknessSpinBox = QSpinBox()
        self.E2thicknessSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2thicknessSpinBox.setSingleStep(1)
        self.E2thicknessSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2thicknessSpinBox.setRange(1,10)
        self.E2thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[1])
        self.E2thicknessSpinBox.valueChanged.connect(self.setElinethickness1)
        self.E3thicknessSpinBox = QSpinBox()
        self.E3thicknessSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3thicknessSpinBox.setSingleStep(1)
        self.E3thicknessSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3thicknessSpinBox.setRange(1,10)
        self.E3thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[2])
        self.E3thicknessSpinBox.valueChanged.connect(self.setElinethickness2)
        self.E4thicknessSpinBox = QSpinBox()
        self.E4thicknessSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4thicknessSpinBox.setSingleStep(1)
        self.E4thicknessSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4thicknessSpinBox.setRange(1,10)
        self.E4thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[3])
        self.E4thicknessSpinBox.valueChanged.connect(self.setElinethickness3)
        self.E1alphaSpinBox = QDoubleSpinBox()
        self.E1alphaSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1alphaSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1alphaSpinBox.setRange(.1,1.)
        self.E1alphaSpinBox.setSingleStep(.1)
        self.E1alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[0])
        self.E1alphaSpinBox.valueChanged.connect(self.setElinealpha0)
        self.E2alphaSpinBox = QDoubleSpinBox()
        self.E2alphaSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2alphaSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2alphaSpinBox.setRange(.1,1.)
        self.E2alphaSpinBox.setSingleStep(.1)
        self.E2alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[1])
        self.E1alphaSpinBox.valueChanged.connect(self.setElinealpha1)
        self.E3alphaSpinBox = QDoubleSpinBox()
        self.E3alphaSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3alphaSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3alphaSpinBox.setRange(.1,1.)
        self.E3alphaSpinBox.setSingleStep(.1)
        self.E3alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[2])
        self.E3alphaSpinBox.valueChanged.connect(self.setElinealpha2)
        self.E4alphaSpinBox = QDoubleSpinBox()
        self.E4alphaSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4alphaSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4alphaSpinBox.setRange(.1,1.)
        self.E4alphaSpinBox.setSingleStep(.1)
        self.E4alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[3])
        self.E4alphaSpinBox.valueChanged.connect(self.setElinealpha3)
        #Marker size
        self.E1sizeSpinBox = QSpinBox()
        self.E1sizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1sizeSpinBox.setSingleStep(1)
        self.E1sizeSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1sizeSpinBox.setRange(1,14)
        self.E1sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[0])
        self.E1sizeSpinBox.valueChanged.connect(self.setEmarkersize0)
        self.E2sizeSpinBox = QSpinBox()
        self.E2sizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2sizeSpinBox.setSingleStep(1)
        self.E2sizeSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2sizeSpinBox.setRange(1,14)
        self.E2sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[1])
        self.E2sizeSpinBox.valueChanged.connect(self.setEmarkersize1)
        self.E3sizeSpinBox = QSpinBox()
        self.E3sizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3sizeSpinBox.setSingleStep(1)
        self.E3sizeSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3sizeSpinBox.setRange(1,14)
        self.E3sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[2])
        self.E3sizeSpinBox.valueChanged.connect(self.setEmarkersize2)
        self.E4sizeSpinBox = QSpinBox()
        self.E4sizeSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4sizeSpinBox.setSingleStep(1)
        self.E4sizeSpinBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4sizeSpinBox.setRange(1,14)
        self.E4sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[3])
        self.E4sizeSpinBox.valueChanged.connect(self.setEmarkersize3)
        self.autoCharge = QCheckBox(QApplication.translate("CheckBox","Auto CHARGE"))
        self.autoCharge.setChecked(self.aw.qmc.autoChargeFlag)
        self.autoCharge.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if self.app.artisanviewerMode:
            self.autoCharge.setEnabled(False)
        self.autoDrop = QCheckBox(QApplication.translate("CheckBox","Auto DROP"))
        self.autoDrop.setChecked(self.aw.qmc.autoDropFlag)
        self.autoDrop.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if self.app.artisanviewerMode:
            self.autoDrop.setEnabled(False)
        self.markTP = QCheckBox(QApplication.translate("CheckBox","Mark TP"))
        self.markTP.setChecked(self.aw.qmc.markTPflag)
        self.markTP.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        #show met 
        self.ShowMet = QCheckBox(QApplication.translate("CheckBox", "Mark MET"))
        self.ShowMet.setChecked(self.aw.qmc.showmet)
        self.ShowMet.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ShowMet.stateChanged.connect(self.changeShowMet)         #toggle
        self.ShowTimeguide = QCheckBox(QApplication.translate("CheckBox", "Show Time Guide"))
        self.ShowTimeguide.setChecked(self.aw.qmc.showtimeguide)
        self.ShowTimeguide.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ShowTimeguide.stateChanged.connect(self.changeShowTimeguide)

        # connect the ArtisanDialog standard OK/Cancel buttons
        self.dialogbuttons.accepted.connect(self.updatetypes)
        self.dialogbuttons.rejected.connect(self.restoreState)
        
       
        ###  TAB 2
        #number of buttons per row
        self.nbuttonslabel = QLabel(QApplication.translate("Label","Max buttons per row"))
        self.nbuttonsSpinBox = QSpinBox()
        self.nbuttonsSpinBox.setMaximumWidth(100)
        self.nbuttonsSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nbuttonsSpinBox.setRange(2,30)
        self.nbuttonsSpinBox.setValue(self.aw.buttonlistmaxlen)
        self.nbuttonsSpinBox.valueChanged.connect(self.setbuttonlistmaxlen)
        nbuttonsSizeLabel = QLabel(QApplication.translate("Label","Button size"))
        self.nbuttonsSizeBox = MyQComboBox()
        size_items = [
                    QApplication.translate("ComboBox", "tiny"),
                    QApplication.translate("ComboBox", "small"),
                    QApplication.translate("ComboBox", "large")
                ]
        self.nbuttonsSizeBox.addItems(size_items)
        self.nbuttonsSizeBox.setCurrentIndex(self.aw.buttonsize)
        #table for showing events
        self.eventbuttontable = QTableWidget()
        self.eventbuttontable.setTabKeyNavigation(True)
        self.eventbuttontable.itemSelectionChanged.connect(self.selectionChanged)
        self.createEventbuttonTable()
        self.copyeventbuttonTableButton = QPushButton(QApplication.translate("Button", "Copy Table"))
        self.copyeventbuttonTableButton.setToolTip(QApplication.translate("Tooltip","Copy table to clipboard, OPTION or ALT click for tabular text"))
        self.copyeventbuttonTableButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.copyeventbuttonTableButton.clicked.connect(self.copyEventButtonTabletoClipboard)
        addButton = QPushButton(QApplication.translate("Button","Add"))
        addButton.setToolTip(QApplication.translate("Tooltip","Add new extra Event button"))
        #addButton.setMaximumWidth(100)
        addButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        addButton.clicked.connect(self.addextraeventbuttonSlot)
        delButton = QPushButton(QApplication.translate("Button","Delete"))
        delButton.setToolTip(QApplication.translate("Tooltip","Delete the last extra Event button"))
        #delButton.setMaximumWidth(100)
        delButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        delButton.clicked.connect(self.delextraeventbutton)
        self.insertButton = QPushButton(QApplication.translate("Button","Insert"))
        self.insertButton.clicked.connect(self.insertextraeventbuttonSlot)
        self.insertButton.setMinimumWidth(80)
        self.insertButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.insertButton.setEnabled(False)
        helpDialogButton = QDialogButtonBox()
        helpButton = helpDialogButton.addButton(QDialogButtonBox.StandardButton.Help)
        helpButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        helpButton.setToolTip(QApplication.translate("Tooltip","Show help"))
        self.setButtonTranslations(helpButton,"Help",QApplication.translate("Button","Help"))
        helpButton.clicked.connect(self.showEventbuttonhelp)
        #color patterns
        #flag that prevents changing colors too fast
        self.changingcolorflag = False
        colorpatternlabel = QLabel(QApplication.translate("Label","Color Pattern"))
        self.colorSpinBox = QSpinBox()
        self.colorSpinBox.setWrapping(True)
        self.colorSpinBox.setMaximumWidth(100)
        self.colorSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.colorSpinBox.setRange(0,359)
        self.colorSpinBox.valueChanged.connect(self.colorizebuttons)
        ## tab4
        transferpalettebutton = QPushButton(QApplication.translate("Button","<< Store Palette"))
        transferpalettebutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        setpalettebutton = QPushButton(QApplication.translate("Button","Activate Palette >>"))
        setpalettebutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        transferpalettecurrentLabel = QLabel(QApplication.translate("Label","current:"))
        self.transferpalettecurrentLabelEdit = QLineEdit(self.aw.buttonpalette_label)

        
        self.transferpalettecombobox = QComboBox()
        self.transferpalettecombobox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # next line needed to avoid truncation of entries on Mac OS X under Qt 5.12.1-5.12.3
        # https://bugreports.qt.io/browse/QTBUG-73653
        self.transferpalettecombobox.setMinimumWidth(120)
        self.updatePalettePopup()
        
        transferpalettebutton.clicked.connect(self.transferbuttonstoSlot)
        self.switchPaletteByNumberKey = QCheckBox(QApplication.translate("CheckBox","Switch Using Number Keys + Cmd"))
        self.switchPaletteByNumberKey.setChecked(self.aw.buttonpalette_shortcuts)
        self.switchPaletteByNumberKey.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        setpalettebutton.clicked.connect(self.setbuttonsfrom)
        backupbutton = QPushButton(QApplication.translate("Button","Save"))
        backupbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        restorebutton = QPushButton(QApplication.translate("Button","Load"))
        restorebutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        backupbutton.setToolTip(QApplication.translate("Tooltip","Backup all palettes to a text file"))
        restorebutton.setToolTip(QApplication.translate("Tooltip","Restore all palettes from a text file"))
        backupbutton.setMaximumWidth(140)
        restorebutton.setMaximumWidth(140)
        backupbutton.clicked.connect(self.backuppaletteeventbuttonsSlot)
        restorebutton.clicked.connect(self.restorepaletteeventbuttons)
        ## tab5
        eventtitlelabel = QLabel(QApplication.translate("Label","Event"))
        eventtitlelabel.setFont(titlefont)
        actiontitlelabel = QLabel(QApplication.translate("Label","Action"))
        actiontitlelabel.setFont(titlefont)
        commandtitlelabel = QLabel(QApplication.translate("Label","Command"))
        commandtitlelabel.setFont(titlefont)
        offsettitlelabel = QLabel(QApplication.translate("Label","Offset"))
        offsettitlelabel.setFont(titlefont)
        factortitlelabel = QLabel(QApplication.translate("Label","Factor"))
        factortitlelabel.setFont(titlefont)
        min_titlelabel = QLabel(QApplication.translate("Label","Min"))
        min_titlelabel.setFont(titlefont)
        max_titlelabel = QLabel(QApplication.translate("Label","Max"))
        max_titlelabel.setFont(titlefont)
        sliderBernoullititlelabel = QLabel(QApplication.translate("Label","Bernoulli"))
        sliderBernoullititlelabel.setFont(titlefont)
        slidercoarsetitlelabel = QLabel(QApplication.translate("Label","Coarse"))
        slidercoarsetitlelabel.setFont(titlefont)
        quantifieractiontitlelabel = QLabel(QApplication.translate("Label","Action"))
        quantifieractiontitlelabel.setFont(titlefont)
        quantifieractiontitlelabel.setToolTip(QApplication.translate("Tooltip","Triggered quantifier fires slider action"))
        quantifierSVtitlelabel = QLabel(QApplication.translate("Label","SV"))
        quantifierSVtitlelabel.setFont(titlefont)
        quantifierSVtitlelabel.setToolTip(QApplication.translate("Tooltip","No processing delay if source delivers the set value (SV) instead of the process value (PV)"))
        slidertemptitlelabel = QLabel(QApplication.translate("Label","Temp"))
        slidertemptitlelabel.setFont(titlefont)
        sliderunittitlelabel = QLabel(QApplication.translate("Label","Unit"))
        sliderunittitlelabel.setFont(titlefont)
        self.E1visibility = QCheckBox(self.aw.qmc.etypesf(0))
        self.E1visibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1visibility.setChecked(bool(self.aw.eventslidervisibilities[0]))
        self.E2visibility = QCheckBox(self.aw.qmc.etypesf(1))
        self.E2visibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2visibility.setChecked(bool(self.aw.eventslidervisibilities[1]))
        self.E3visibility = QCheckBox(self.aw.qmc.etypesf(2))
        self.E3visibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3visibility.setChecked(bool(self.aw.eventslidervisibilities[2]))
        self.E4visibility = QCheckBox(self.aw.qmc.etypesf(3))
        self.E4visibility.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4visibility.setChecked(bool(self.aw.eventslidervisibilities[3]))
        self.sliderActionTypes = ["",#QApplication.translate("ComboBox", "None"),
                       QApplication.translate("ComboBox", "Serial Command"),
                       QApplication.translate("ComboBox", "Modbus Command"),
                       QApplication.translate("ComboBox", "DTA Command"),
                       QApplication.translate("ComboBox", "Call Program"),
                       QApplication.translate("ComboBox", "Hottop Heater"),
                       QApplication.translate("ComboBox", "Hottop Fan"),
                       QApplication.translate("ComboBox", "Hottop Command"),
                       QApplication.translate("ComboBox", "Fuji Command"),
                       QApplication.translate("ComboBox", "PWM Command"),
                       QApplication.translate("ComboBox", "VOUT Command"),
                       QApplication.translate("ComboBox", "IO Command"),
                       QApplication.translate("ComboBox", "S7 Command"),
                       QApplication.translate("ComboBox", "Aillio R1 Heater"),
                       QApplication.translate("ComboBox", "Aillio R1 Fan"),
                       QApplication.translate("ComboBox", "Aillio R1 Drum"),
                       QApplication.translate("ComboBox", "Artisan Command"),
                       QApplication.translate("ComboBox", "RC Command"),
                       QApplication.translate("ComboBox", "WebSocket Command")]
        self.E1action = QComboBox()
        self.E1action.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.E1action.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1action.addItems(self.sliderActionTypes)
        self.E1action.setCurrentIndex(self.aw.eventslideractions[0])
        self.E2action = QComboBox()
        self.E2action.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.E2action.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2action.addItems(self.sliderActionTypes)
        self.E2action.setCurrentIndex(self.aw.eventslideractions[1])
        self.E3action = QComboBox()
        self.E3action.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.E3action.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3action.addItems(self.sliderActionTypes)
        self.E3action.setCurrentIndex(self.aw.eventslideractions[2])
        self.E4action = QComboBox()
        self.E4action.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.E4action.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4action.addItems(self.sliderActionTypes)
        self.E4action.setCurrentIndex(self.aw.eventslideractions[3])
        self.E1command = QLineEdit(self.aw.eventslidercommands[0])
        self.E2command = QLineEdit(self.aw.eventslidercommands[1])
        self.E3command = QLineEdit(self.aw.eventslidercommands[2])
        self.E4command = QLineEdit(self.aw.eventslidercommands[3])
        self.E1offset = QDoubleSpinBox()
        self.E1offset.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1offset.setRange(-9999,9999)
        self.E1offset.setDecimals(1)
        self.E1offset.setValue(self.aw.eventslideroffsets[0])
        self.E2offset = QDoubleSpinBox()
        self.E2offset.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2offset.setRange(-9999,9999)
        self.E2offset.setDecimals(1)
        self.E2offset.setValue(self.aw.eventslideroffsets[1])
        self.E3offset = QDoubleSpinBox()
        self.E3offset.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3offset.setRange(-9999,9999)
        self.E3offset.setDecimals(1)
        self.E3offset.setValue(self.aw.eventslideroffsets[2])
        self.E4offset = QDoubleSpinBox()
        self.E4offset.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4offset.setRange(-9999,9999)
        self.E4offset.setDecimals(1)
        self.E4offset.setValue(self.aw.eventslideroffsets[3])
        self.E1factor = QDoubleSpinBox()
        self.E1factor.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1factor.setRange(-999,999)
        self.E1factor.setDecimals(3)
        self.E1factor.setValue(self.aw.eventsliderfactors[0])
        self.E1factor.setMaximumWidth(70)
        self.E2factor = QDoubleSpinBox()
        self.E2factor.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2factor.setRange(-999,999)
        self.E2factor.setDecimals(3)
        self.E2factor.setValue(self.aw.eventsliderfactors[1])
        self.E2factor.setMaximumWidth(70)
        self.E3factor = QDoubleSpinBox()
        self.E3factor.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3factor.setRange(-999,999)
        self.E3factor.setDecimals(3)
        self.E3factor.setValue(self.aw.eventsliderfactors[2])
        self.E3factor.setMaximumWidth(70)
        self.E4factor = QDoubleSpinBox()
        self.E4factor.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4factor.setRange(-999,999)
        self.E4factor.setDecimals(3)
        self.E4factor.setValue(self.aw.eventsliderfactors[3])
        self.E4factor.setMaximumWidth(70)
        self.E1_min = QSpinBox()
        self.E1_min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1_min.setRange(0,self.aw.eventsMaxValue)
        self.E1_min.setValue(self.aw.eventslidermin[0])
        self.E2_min = QSpinBox()
        self.E2_min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2_min.setRange(0,self.aw.eventsMaxValue)
        self.E2_min.setValue(self.aw.eventslidermin[1])
        self.E3_min = QSpinBox()
        self.E3_min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3_min.setRange(0,self.aw.eventsMaxValue)
        self.E3_min.setValue(self.aw.eventslidermin[2])
        self.E4_min = QSpinBox()
        self.E4_min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4_min.setRange(0,self.aw.eventsMaxValue)
        self.E4_min.setValue(self.aw.eventslidermin[3])
        self.E1_max = QSpinBox()
        self.E1_max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1_max.setRange(0,self.aw.eventsMaxValue)
        self.E1_max.setValue(self.aw.eventslidermax[0])
        self.E2_max = QSpinBox()
        self.E2_max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2_max.setRange(0,self.aw.eventsMaxValue)
        self.E2_max.setValue(self.aw.eventslidermax[1])
        self.E3_max = QSpinBox()
        self.E3_max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3_max.setRange(0,self.aw.eventsMaxValue)
        self.E3_max.setValue(self.aw.eventslidermax[2])
        self.E4_max = QSpinBox()
        self.E4_max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4_max.setRange(0,self.aw.eventsMaxValue)
        self.E4_max.setValue(self.aw.eventslidermax[3])
        
        # https://www.home-barista.com/home-roasting/coffee-roasting-best-practices-scott-rao-t65601-70.html#p724654
        bernoulli_tooltip_text = QApplication.translate("Tooltip", "Applies the Bernoulli's gas law to the values computed\nby applying the given factor and offset to the slider value\nassuming that the gas pressureand not the gas flow is controlled.\nTo reduce heat (or gas flow) by 50% the gas pressure\nhas to be reduced by 4 times.")
        self.E1slider_bernoulli = QCheckBox()
        self.E1slider_bernoulli.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[0]))
        self.E1slider_bernoulli.setToolTip(bernoulli_tooltip_text)
        self.E2slider_bernoulli = QCheckBox()
        self.E2slider_bernoulli.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[1]))
        self.E2slider_bernoulli.setToolTip(bernoulli_tooltip_text)
        self.E3slider_bernoulli = QCheckBox()
        self.E3slider_bernoulli.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[2]))
        self.E3slider_bernoulli.setToolTip(bernoulli_tooltip_text)
        self.E4slider_bernoulli = QCheckBox()
        self.E4slider_bernoulli.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[3]))
        self.E4slider_bernoulli.setToolTip(bernoulli_tooltip_text)
        slider_coarse_tooltip_text = QApplication.translate("Tooltip", "Slider steps in multiple of 10 otherwise 1")
        self.E1slider_coarse = QCheckBox()
        self.E1slider_coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1slider_coarse.setChecked(bool(self.aw.eventslidercoarse[0]))
        self.E1slider_coarse.setToolTip(slider_coarse_tooltip_text)
        self.E2slider_coarse = QCheckBox()
        self.E2slider_coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2slider_coarse.setChecked(bool(self.aw.eventslidercoarse[1]))
        self.E2slider_coarse.setToolTip(slider_coarse_tooltip_text)
        self.E3slider_coarse = QCheckBox()
        self.E3slider_coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3slider_coarse.setChecked(bool(self.aw.eventslidercoarse[2]))
        self.E3slider_coarse.setToolTip(slider_coarse_tooltip_text)
        self.E4slider_coarse = QCheckBox()
        self.E4slider_coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4slider_coarse.setChecked(bool(self.aw.eventslidercoarse[3]))
        self.E4slider_coarse.setToolTip(slider_coarse_tooltip_text)
        slider_temp_tooltip_text = QApplication.translate("Tooltip", "Slider values interpreted as temperatures")
        self.E1slider_temp = QCheckBox()
        self.E1slider_temp.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1slider_temp.setChecked(bool(self.aw.eventslidertemp[0]))
        self.E1slider_temp.setToolTip(slider_temp_tooltip_text)
        self.E2slider_temp = QCheckBox()
        self.E2slider_temp.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2slider_temp.setChecked(bool(self.aw.eventslidertemp[1]))
        self.E2slider_temp.setToolTip(slider_temp_tooltip_text)
        self.E3slider_temp = QCheckBox()
        self.E3slider_temp.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3slider_temp.setChecked(bool(self.aw.eventslidertemp[2]))
        self.E3slider_temp.setToolTip(slider_temp_tooltip_text)
        self.E4slider_temp = QCheckBox()
        self.E4slider_temp.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4slider_temp.setChecked(bool(self.aw.eventslidertemp[3]))
        self.E4slider_temp.setToolTip(slider_temp_tooltip_text)
        maxwidth = 40
        slider_unit_tooltip_text = QApplication.translate("Tooltip", "Unit to be added to generated event descriptions")
        self.E1unit = QLineEdit(self.aw.eventsliderunits[0])
        self.E1unit.setMaximumWidth(maxwidth)
        self.E1unit.setToolTip(slider_unit_tooltip_text)
        self.E2unit = QLineEdit(self.aw.eventsliderunits[1])
        self.E2unit.setMaximumWidth(maxwidth)
        self.E2unit.setToolTip(slider_unit_tooltip_text)
        self.E3unit = QLineEdit(self.aw.eventsliderunits[2])
        self.E3unit.setMaximumWidth(maxwidth)
        self.E3unit.setToolTip(slider_unit_tooltip_text)
        self.E4unit = QLineEdit(self.aw.eventsliderunits[3])
        self.E4unit.setMaximumWidth(maxwidth)
        self.E4unit.setToolTip(slider_unit_tooltip_text)
        helpsliderDialogButton = QDialogButtonBox()
        helpsliderbutton = helpsliderDialogButton.addButton(QDialogButtonBox.StandardButton.Help)
        helpsliderbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setButtonTranslations(helpsliderbutton,"Help",QApplication.translate("Button","Help"))
        helpsliderbutton.clicked.connect(self.showSliderHelp)
        ## tab4
        qeventtitlelabel = QLabel(QApplication.translate("Label","Event"))
        qeventtitlelabel.setFont(titlefont)
        sourcetitlelabel = QLabel(QApplication.translate("Label","Source"))
        sourcetitlelabel.setFont(titlefont)
        mintitlelabel = QLabel(QApplication.translate("Label","Min"))
        mintitlelabel.setFont(titlefont)
        maxtitlelabel = QLabel(QApplication.translate("Label","Max"))
        maxtitlelabel.setFont(titlefont)
        coarsetitlelabel = QLabel(QApplication.translate("Label","Coarse"))
        coarsetitlelabel.setFont(titlefont)
        self.E1active = QCheckBox(self.aw.qmc.etypesf(0))
        self.E1active.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1active.setChecked(bool(self.aw.eventquantifieractive[0]))
        self.E2active = QCheckBox(self.aw.qmc.etypesf(1))
        self.E2active.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2active.setChecked(bool(self.aw.eventquantifieractive[1]))
        self.E3active = QCheckBox(self.aw.qmc.etypesf(2))
        self.E3active.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3active.setChecked(bool(self.aw.eventquantifieractive[2]))
        self.E4active = QCheckBox(self.aw.qmc.etypesf(3))
        self.E4active.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4active.setChecked(bool(self.aw.eventquantifieractive[3]))
        self.E1coarse = QCheckBox()
        self.E1coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1coarse.setChecked(bool(self.aw.eventquantifiercoarse[0]))
        self.E2coarse = QCheckBox()
        self.E2coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2coarse.setChecked(bool(self.aw.eventquantifiercoarse[1]))
        self.E3coarse = QCheckBox()
        self.E3coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3coarse.setChecked(bool(self.aw.eventquantifiercoarse[2]))
        self.E4coarse = QCheckBox()
        self.E4coarse.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4coarse.setChecked(bool(self.aw.eventquantifiercoarse[3]))
        self.E1quantifieraction = QCheckBox()
        self.E1quantifieraction.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1quantifieraction.setChecked(bool(self.aw.eventquantifieraction[0]))
        self.E2quantifieraction = QCheckBox()
        self.E2quantifieraction.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2quantifieraction.setChecked(bool(self.aw.eventquantifieraction[1]))
        self.E3quantifieraction = QCheckBox()
        self.E3quantifieraction.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3quantifieraction.setChecked(bool(self.aw.eventquantifieraction[2]))
        self.E4quantifieraction = QCheckBox()
        self.E4quantifieraction.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4quantifieraction.setChecked(bool(self.aw.eventquantifieraction[3]))
        self.E1quantifierSV = QCheckBox()
        self.E1quantifierSV.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E1quantifierSV.setChecked(bool(self.aw.eventquantifierSV[0]))
        self.E2quantifierSV = QCheckBox()
        self.E2quantifierSV.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E2quantifierSV.setChecked(bool(self.aw.eventquantifierSV[1]))
        self.E3quantifierSV = QCheckBox()
        self.E3quantifierSV.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E3quantifierSV.setChecked(bool(self.aw.eventquantifierSV[2]))
        self.E4quantifierSV = QCheckBox()
        self.E4quantifierSV.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.E4quantifierSV.setChecked(bool(self.aw.eventquantifierSV[3]))
        
        self.curvenames = []
        self.curvenames.append(QApplication.translate("ComboBox","ET"))
        self.curvenames.append(QApplication.translate("ComboBox","BT"))
        for i in range(len(self.aw.qmc.extradevices)):
            self.curvenames.append(str(i) + "xT1: " + self.aw.qmc.extraname1[i])
            self.curvenames.append(str(i) + "xT2: " + self.aw.qmc.extraname2[i])
        self.E1SourceComboBox = QComboBox()
        self.E1SourceComboBox.addItems(self.curvenames)
        if self.aw.eventquantifiersource[0] < len(self.curvenames):
            self.E1SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[0])
        self.E2SourceComboBox = QComboBox()
        self.E2SourceComboBox.addItems(self.curvenames)
        if self.aw.eventquantifiersource[1] < len(self.curvenames):
            self.E2SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[1])
        self.E3SourceComboBox = QComboBox()
        self.E3SourceComboBox.addItems(self.curvenames)
        if self.aw.eventquantifiersource[2] < len(self.curvenames):
            self.E3SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[2])
        self.E4SourceComboBox = QComboBox()
        self.E4SourceComboBox.addItems(self.curvenames)
        if self.aw.eventquantifiersource[3] < len(self.curvenames):
            self.E4SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[3])
        self.E1min = QSpinBox()
        self.E1min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1min.setRange(-99999,99999)
        self.E1min.setValue(self.aw.eventquantifiermin[0])
        self.E2min = QSpinBox()
        self.E2min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2min.setRange(-99999,99999)
        self.E2min.setValue(self.aw.eventquantifiermin[1])
        self.E3min = QSpinBox()
        self.E3min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3min.setRange(-99999,99999)
        self.E3min.setValue(self.aw.eventquantifiermin[2])
        self.E4min = QSpinBox()
        self.E4min.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4min.setRange(-99999,99999)
        self.E4min.setValue(self.aw.eventquantifiermin[3])
        self.E1max = QSpinBox()
        self.E1max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E1max.setRange(-99999,99999)
        self.E1max.setValue(self.aw.eventquantifiermax[0])
        self.E2max = QSpinBox()
        self.E2max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E2max.setRange(-99999,99999)
        self.E2max.setValue(self.aw.eventquantifiermax[1])
        self.E3max = QSpinBox()
        self.E3max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E3max.setRange(-99999,99999)
        self.E3max.setValue(self.aw.eventquantifiermax[2])
        self.E4max = QSpinBox()
        self.E4max.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.E4max.setRange(-99999,99999)
        self.E4max.setValue(self.aw.eventquantifiermax[3])
        applyDialogButton = QDialogButtonBox()
        applyquantifierbutton = applyDialogButton.addButton(QDialogButtonBox.StandardButton.Apply)
        self.setButtonTranslations(applyquantifierbutton,"Apply",QApplication.translate("Button","Apply"))
        applyquantifierbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        applyquantifierbutton.clicked.connect(self.applyQuantifiers)
        self.clusterEventsFlag = QCheckBox(QApplication.translate("Label","Cluster"))
        self.clusterEventsFlag.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clusterEventsFlag.setChecked(bool(self.aw.clusterEventsFlag))
        ### LAYOUTS
        #### tab1 layout
        bartypeLayout = QHBoxLayout()
        bartypeLayout.addWidget(barstylelabel)
        bartypeLayout.addWidget(self.bartypeComboBox,Qt.AlignmentFlag.AlignLeft)
        FlagsLayout = QHBoxLayout()
        FlagsLayout.addStretch()
        FlagsLayout.addWidget(self.eventsbuttonflag)
        FlagsLayout.addSpacing(5)
        FlagsLayout.addWidget(self.minieventsflag)
        FlagsLayout.addSpacing(5)
        FlagsLayout.addWidget(self.showeventsonbtbox)
        FlagsLayout.addSpacing(5)
        FlagsLayout.addWidget(self.annotationsflagbox)
        FlagsLayout.addStretch()
#        FlagsLayout.addWidget(self.eventsshowflagbox)
#        FlagsLayout.addSpacing(10)
        FlagsLayout.addLayout(bartypeLayout)
        FlagsLayout.addSpacing(10)
        FlagsLayout.addWidget(self.eventsclampflag)
        FlagsLayout.addSpacing(5)
        FlagsLayout.addWidget(self.eventslabelsflag)
        FlagsLayout.addSpacing(5)
        FlagsLayout.addWidget(self.eventslabelscharsSpinner)
        FlagsLayout.addStretch()
        
        FlagsLayout2 = QHBoxLayout()
        FlagsLayout2.addWidget(self.autoCharge)
        FlagsLayout2.addSpacing(15)
        FlagsLayout2.addWidget(self.autoDrop)
        FlagsLayout2.addSpacing(15)
        FlagsLayout2.addWidget(self.markTP)
        FlagsLayout2.addSpacing(15)
        FlagsLayout2.addWidget(self.ShowMet)
        FlagsLayout2.addSpacing(15)
        FlagsLayout2.addWidget(self.ShowTimeguide)

        typeLayout = QGridLayout()
        typeLayout.addWidget(typelabel1,0,0)
        typeLayout.addWidget(self.showEtype1,0,1)
        typeLayout.addWidget(self.etype0,0,2)
        typeLayout.addWidget(typelabel2,0,3)
        typeLayout.addWidget(self.showEtype2,0,4)
        typeLayout.addWidget(self.etype1,0,5)
        typeLayout.addWidget(typelabel3,0,6)
        typeLayout.addWidget(self.showEtype3,0,7)
        typeLayout.addWidget(self.etype2,0,8)
        typeLayout.addWidget(typelabel4,0,9)
        typeLayout.addWidget(self.showEtype4,0,10)
        typeLayout.addWidget(self.etype3,0,11)
        typeLayout.addWidget(typelabel5,0,12)
        typeLayout.addWidget(self.showEtype5,0,13)
        typeLayout.addWidget(self.etype4,0,14)
        buttonLayout = QHBoxLayout()
        buttonLayout.addLayout(FlagsLayout2)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.dialogbuttons)
        typeHBox = QHBoxLayout()
        typeHBox.addLayout(typeLayout)
        typeHBox.addStretch()
        TypeGroupLayout = QGroupBox(QApplication.translate("GroupBox","Event Types"))
        TypeGroupLayout.setLayout(typeHBox)
        self.buttonActionTypes = ["",#QApplication.translate("ComboBox", "None"),
                       QApplication.translate("ComboBox", "Serial Command"),
                       QApplication.translate("ComboBox", "Call Program"),
                       QApplication.translate("ComboBox", "Modbus Command"),
                       QApplication.translate("ComboBox", "DTA Command"),
                       QApplication.translate("ComboBox", "IO Command"),
                       QApplication.translate("ComboBox", "Hottop Heater"),
                       QApplication.translate("ComboBox", "Hottop Fan"),
                       QApplication.translate("ComboBox", "Hottop Command"),
                       QApplication.translate("ComboBox", "p-i-d"),
                       QApplication.translate("ComboBox", "Fuji Command"),
                       QApplication.translate("ComboBox", "PWM Command"),
                       QApplication.translate("ComboBox", "VOUT Command"),
                       QApplication.translate("ComboBox", "S7 Command"),
                       QApplication.translate("ComboBox", "Aillio R1 Heater"),
                       QApplication.translate("ComboBox", "Aillio R1 Fan"),
                       QApplication.translate("ComboBox", "Aillio R1 Drum"),
                       QApplication.translate("ComboBox", "Aillio R1 Command"),
                       QApplication.translate("ComboBox", "Artisan Command"),
                       QApplication.translate("ComboBox", "RC Command"),
                       QApplication.translate("ComboBox", "Multiple Event"),
                       QApplication.translate("ComboBox", "WebSocket Command")]
        self.CHARGEbutton = QCheckBox(QApplication.translate("CheckBox", "CHARGE"))
        self.CHARGEbutton.setChecked(bool(self.aw.qmc.buttonvisibility[0]))
        self.CHARGEbuttonActionType = QComboBox()
        self.CHARGEbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.CHARGEbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.CHARGEbuttonActionType.addItems(self.buttonActionTypes)
        self.CHARGEbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[0])
        self.CHARGEbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[0])
        self.CHARGEbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.DRYbutton = QCheckBox(QApplication.translate("CheckBox", "DRY END"))
        self.DRYbutton.setChecked(bool(self.aw.qmc.buttonvisibility[1]))
        self.DRYbuttonActionType = QComboBox()
        self.DRYbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.DRYbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.DRYbuttonActionType.addItems(self.buttonActionTypes)
        self.DRYbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[1])
        self.DRYbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[1])
        self.DRYbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.FCSbutton = QCheckBox(QApplication.translate("CheckBox", "FC START"))
        self.FCSbutton.setChecked(bool(self.aw.qmc.buttonvisibility[2]))
        self.FCSbuttonActionType = QComboBox()
        self.FCSbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.FCSbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.FCSbuttonActionType.addItems(self.buttonActionTypes)
        self.FCSbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[2])
        self.FCSbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[2])
        self.FCSbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.FCEbutton = QCheckBox(QApplication.translate("CheckBox", "FC END"))
        self.FCEbutton.setChecked(bool(self.aw.qmc.buttonvisibility[3]))
        self.FCEbuttonActionType = QComboBox()
        self.FCEbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.FCEbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.FCEbuttonActionType.addItems(self.buttonActionTypes)
        self.FCEbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[3])
        self.FCEbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[3])
        self.FCEbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.SCSbutton = QCheckBox(QApplication.translate("CheckBox", "SC START"))
        self.SCSbutton.setChecked(bool(self.aw.qmc.buttonvisibility[4]))
        self.SCSbuttonActionType = QComboBox()
        self.SCSbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.SCSbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.SCSbuttonActionType.addItems(self.buttonActionTypes)
        self.SCSbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[4])
        self.SCSbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[4])
        self.SCSbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.SCEbutton = QCheckBox(QApplication.translate("CheckBox", "SC END"))
        self.SCEbutton.setChecked(bool(self.aw.qmc.buttonvisibility[5]))
        self.SCEbuttonActionType = QComboBox()
        self.SCEbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.SCEbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.SCEbuttonActionType.addItems(self.buttonActionTypes)
        self.SCEbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[5])
        self.SCEbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[5])
        self.SCEbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.DROPbutton = QCheckBox(QApplication.translate("CheckBox", "DROP"))
        self.DROPbutton.setChecked(bool(self.aw.qmc.buttonvisibility[6]))
        self.DROPbuttonActionType = QComboBox()
        self.DROPbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.DROPbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.DROPbuttonActionType.addItems(self.buttonActionTypes)
        self.DROPbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[6])
        self.DROPbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[6])
        self.DROPbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.COOLbutton = QCheckBox(QApplication.translate("CheckBox", "COOL END"))
        self.COOLbutton.setChecked(bool(self.aw.qmc.buttonvisibility[7]))
        self.COOLbuttonActionType = QComboBox()
        self.COOLbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.COOLbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.COOLbuttonActionType.addItems(self.buttonActionTypes)
        self.COOLbuttonActionType.setCurrentIndex(self.aw.qmc.buttonactions[7])
        self.COOLbuttonActionString = QLineEdit(self.aw.qmc.buttonactionstrings[7])
        self.COOLbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.ONbuttonLabel = QLabel(QApplication.translate("Label", "ON"))
        self.ONbuttonActionType = QComboBox()
        self.ONbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.ONbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ONbuttonActionType.addItems(self.buttonActionTypes)
        self.ONbuttonActionType.setCurrentIndex(self.aw.qmc.extrabuttonactions[0])
        self.ONbuttonActionString = QLineEdit(self.aw.qmc.extrabuttonactionstrings[0])
        self.ONbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.OFFbuttonActionType = QComboBox()
        self.OFFbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.OFFbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.OFFbuttonActionType.addItems(self.buttonActionTypes)
        self.OFFbuttonActionType.setCurrentIndex(self.aw.qmc.extrabuttonactions[1])
        self.OFFbuttonActionString = QLineEdit(self.aw.qmc.extrabuttonactionstrings[1])
        self.OFFbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.OFFbuttonLabel = QLabel(QApplication.translate("Label", "OFF"))
        self.SAMPLINGbuttonActionType = QComboBox()
        self.SAMPLINGbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.SAMPLINGbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.SAMPLINGbuttonActionType.addItems(self.buttonActionTypes)
        self.SAMPLINGbuttonActionType.setCurrentIndex(self.aw.qmc.extrabuttonactions[2])
        self.SAMPLINGbuttonActionType.setMinimumContentsLength(3)
        self.SAMPLINGbuttonActionType.setMinimumWidth(self.SAMPLINGbuttonActionType.minimumSizeHint().width())
        self.SAMPLINGbuttonActionString = QLineEdit(self.aw.qmc.extrabuttonactionstrings[2])
        self.SAMPLINGbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.SAMPLINGbuttonActionInterval = QComboBox()
        self.SAMPLINGbuttonActionInterval.setToolTip(QApplication.translate("Tooltip", "Interval"))
        self.SAMPLINGbuttonActionInterval.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        buttonActionIntervals = ["sync", "1.0s", "1.5s", "2.0s", "2.5s", "3.0s", "3.5s", "4.0s", "4.5s", "5.0s", "10s", "20s", "30s", "45s", "1min"]
        self.sampling_delays = [0,1000,1500,2000,2500,3000,3500,4000,4500,5000,10000,20000,30000,45000,60000]
        self.SAMPLINGbuttonActionInterval.addItems(buttonActionIntervals)
        self.SAMPLINGbuttonActionInterval.setMaximumWidth(70)
        try:
            self.SAMPLINGbuttonActionInterval.setCurrentIndex(self.sampling_delays.index(self.aw.qmc.extra_event_sampling_delay))
        except Exception: # pylint: disable=broad-except
            pass
        self.RESETbuttonLabel = QLabel(QApplication.translate("Label", "RESET"))
        self.RESETbuttonActionType = QComboBox()
        self.RESETbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.RESETbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.RESETbuttonActionType.addItems(self.buttonActionTypes)
        self.RESETbuttonActionType.setCurrentIndex(self.aw.qmc.xextrabuttonactions[0])
        self.RESETbuttonActionString = QLineEdit(self.aw.qmc.xextrabuttonactionstrings[0])
        self.RESETbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        self.STARTbuttonLabel = QLabel(QApplication.translate("Label", "START"))
        self.STARTbuttonActionType = QComboBox()
        self.STARTbuttonActionType.setToolTip(QApplication.translate("Tooltip", "Action Type"))
        self.STARTbuttonActionType.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.STARTbuttonActionType.addItems(self.buttonActionTypes)
        self.STARTbuttonActionType.setCurrentIndex(self.aw.qmc.xextrabuttonactions[1])
        self.STARTbuttonActionString = QLineEdit(self.aw.qmc.xextrabuttonactionstrings[1])
        self.STARTbuttonActionString.setToolTip(QApplication.translate("Tooltip", "Action String"))
        defaultButtonsLayout = QGridLayout()
        defaultButtonsLayout.addWidget(self.RESETbuttonLabel,0,0,Qt.AlignmentFlag.AlignRight)
        defaultButtonsLayout.addWidget(self.RESETbuttonActionType,0,1)
        defaultButtonsLayout.addWidget(self.RESETbuttonActionString,0,2)        
        defaultButtonsLayout.addWidget(self.ONbuttonLabel,1,0,Qt.AlignmentFlag.AlignRight)
        defaultButtonsLayout.addWidget(self.ONbuttonActionType,1,1)
        defaultButtonsLayout.addWidget(self.ONbuttonActionString,1,2)
        defaultButtonsLayout.addWidget(self.OFFbuttonLabel,2,0,Qt.AlignmentFlag.AlignRight)
        defaultButtonsLayout.addWidget(self.OFFbuttonActionType,2,1)
        defaultButtonsLayout.addWidget(self.OFFbuttonActionString,2,2)
        defaultButtonsLayout.addWidget(self.STARTbuttonLabel,3,0,Qt.AlignmentFlag.AlignRight)
        defaultButtonsLayout.addWidget(self.STARTbuttonActionType,3,1)
        defaultButtonsLayout.addWidget(self.STARTbuttonActionString,3,2)        
        defaultButtonsLayout.addWidget(self.CHARGEbutton,4,0)
        defaultButtonsLayout.addWidget(self.CHARGEbuttonActionType,4,1)
        defaultButtonsLayout.addWidget(self.CHARGEbuttonActionString,4,2)
        defaultButtonsLayout.addWidget(self.DRYbutton,5,0)
        defaultButtonsLayout.addWidget(self.DRYbuttonActionType,5,1)
        defaultButtonsLayout.addWidget(self.DRYbuttonActionString,5,2)
        defaultButtonsLayout.addWidget(self.FCSbutton,0,4)
        defaultButtonsLayout.addWidget(self.FCSbuttonActionType,0,5)
        defaultButtonsLayout.addWidget(self.FCSbuttonActionString,0,6)
        defaultButtonsLayout.addWidget(self.FCEbutton,1,4)
        defaultButtonsLayout.addWidget(self.FCEbuttonActionType,1,5)
        defaultButtonsLayout.addWidget(self.FCEbuttonActionString,1,6)
        defaultButtonsLayout.addWidget(self.SCSbutton,2,4)
        defaultButtonsLayout.addWidget(self.SCSbuttonActionType,2,5)
        defaultButtonsLayout.addWidget(self.SCSbuttonActionString,2,6)
        defaultButtonsLayout.addWidget(self.SCEbutton,3,4)
        defaultButtonsLayout.addWidget(self.SCEbuttonActionType,3,5)
        defaultButtonsLayout.addWidget(self.SCEbuttonActionString,3,6)
        defaultButtonsLayout.addWidget(self.DROPbutton,4,4)
        defaultButtonsLayout.addWidget(self.DROPbuttonActionType,4,5)
        defaultButtonsLayout.addWidget(self.DROPbuttonActionString,4,6)
        defaultButtonsLayout.addWidget(self.COOLbutton,5,4)
        defaultButtonsLayout.addWidget(self.COOLbuttonActionType,5,5)
        defaultButtonsLayout.addWidget(self.COOLbuttonActionString,5,6)
        defaultButtonsLayout.setContentsMargins(5,5,5,5)
        defaultButtonsLayout.setHorizontalSpacing(10)
        defaultButtonsLayout.setVerticalSpacing(5)
        defaultButtonsLayout.setColumnMinimumWidth(3,20)
        ButtonGroupLayout = QGroupBox(QApplication.translate("GroupBox","Default Buttons"))
        ButtonGroupLayout.setLayout(defaultButtonsLayout)
        if self.app.artisanviewerMode:
            ButtonGroupLayout.setEnabled(False)
        
        samplingLayout = QHBoxLayout()
        samplingLayout.addStretch()
        samplingLayout.addWidget(self.SAMPLINGbuttonActionType)
        samplingLayout.addWidget(self.SAMPLINGbuttonActionString)
        samplingLayout.addWidget(self.SAMPLINGbuttonActionInterval)
        samplingLayout.addStretch()
        SamplingGroupLayout = QGroupBox(QApplication.translate("GroupBox","Sampling"))
        SamplingGroupLayout.setLayout(samplingLayout)
        if self.app.artisanviewerMode:
            SamplingGroupLayout.setEnabled(False)
        topLineLayout = QHBoxLayout()
        topLineLayout.addWidget(TypeGroupLayout)
        topLineLayout.addWidget(SamplingGroupLayout)
        tab1layout = QVBoxLayout()
        tab1layout.addLayout(FlagsLayout)
        tab1layout.addLayout(topLineLayout)
        tab1layout.addWidget(ButtonGroupLayout)
        tab1layout.addStretch()
        FlagsLayout.setContentsMargins(0,10,0,0)
        FlagsLayout.setSpacing(10)
        topLineLayout.setContentsMargins(0,0,0,0)
        tab1layout.setSpacing(2)
        tab1layout.setContentsMargins(0,0,0,0)
        nbuttonslayout = QHBoxLayout()
        nbuttonslayout.addWidget(self.nbuttonslabel)
        nbuttonslayout.addWidget(self.nbuttonsSpinBox)
        nbuttonslayout.addSpacing(10)
        nbuttonslayout.addWidget(nbuttonsSizeLabel)
        nbuttonslayout.addWidget(self.nbuttonsSizeBox)
        nbuttonslayout.addSpacing(10)
        nbuttonslayout.addWidget(colorpatternlabel)
        nbuttonslayout.addWidget(self.colorSpinBox)
        nbuttonslayout.addStretch()
        tab2buttonlayout = QHBoxLayout()
        tab2buttonlayout.addWidget(addButton)
        tab2buttonlayout.addWidget(self.insertButton)
        tab2buttonlayout.addWidget(delButton)
        tab2buttonlayout.addWidget(self.copyeventbuttonTableButton)
        tab2buttonlayout.addStretch()
        tab2buttonlayout.addWidget(helpDialogButton)
        ### tab2 layout
        tab2layout = QVBoxLayout()
        tab2layout.addWidget(self.eventbuttontable)
        tab2layout.addLayout(nbuttonslayout)
        tab2layout.addLayout(tab2buttonlayout)
        tab2layout.setSpacing(5)
        tab2layout.setContentsMargins(0,10,0,5)
        ### tab4 layout
        paletteGrid = QGridLayout()
        paletteGrid.addWidget(transferpalettebutton,0,1)
        paletteGrid.addWidget(self.transferpalettecombobox,1,0)
        paletteGrid.addWidget(transferpalettecurrentLabel,1,2)
        paletteGrid.addWidget(self.transferpalettecurrentLabelEdit,1,3)
        paletteGrid.addWidget(setpalettebutton,2,1)
        paletteBox = QHBoxLayout()
        paletteBox.addStretch()
        paletteBox.addLayout(paletteGrid)
        paletteBox.addStretch()
        paletteFlags = QHBoxLayout()
        paletteFlags.addStretch()
        paletteFlags.addWidget(self.switchPaletteByNumberKey)
        paletteFlags.addStretch()
        paletteManagementBox = QVBoxLayout()
        paletteManagementBox.addLayout(paletteBox)
        paletteManagementBox.addLayout(paletteFlags)
        paletteGroupLayout = QGroupBox(QApplication.translate("GroupBox","Management"))
        paletteGroupLayout.setLayout(paletteManagementBox)
        paletteButtons = QHBoxLayout()
        paletteButtons.addStretch()
        paletteButtons.addWidget(restorebutton)
        paletteButtons.addWidget(backupbutton)
        tab3layout = QVBoxLayout()
        tab3layout.addWidget(paletteGroupLayout)
        tab3layout.addLayout(paletteButtons)
        tab3layout.addStretch()
        ###
        valueLayout = QGridLayout()
        valueLayout.addWidget(valuecolorlabel,0,0)
        valueLayout.addWidget(valuetextcolorlabel,0,1)
        valueLayout.addWidget(valuesymbollabel,0,2)
        valueLayout.addWidget(valuethicknesslabel,0,3)
        valueLayout.addWidget(valuealphalabel,0,4)
        valueLayout.addWidget(valuesizelabel,0,5)
        valueLayout.addWidget(self.E1colorButton,1,0)
        valueLayout.addWidget(self.E1textcolorButton,1,1)
        valueLayout.addWidget(self.marker1typeComboBox,1,2)
        valueLayout.addWidget(self.E1thicknessSpinBox,1,3)
        valueLayout.addWidget(self.E1alphaSpinBox,1,4)
        valueLayout.addWidget(self.E1sizeSpinBox,1,5)
        valueLayout.addWidget(self.E2colorButton,2,0)
        valueLayout.addWidget(self.E2textcolorButton,2,1)
        valueLayout.addWidget(self.marker2typeComboBox,2,2)
        valueLayout.addWidget(self.E2thicknessSpinBox,2,3)
        valueLayout.addWidget(self.E2alphaSpinBox,2,4)
        valueLayout.addWidget(self.E2sizeSpinBox,2,5)
        valueLayout.addWidget(self.E3colorButton,3,0)
        valueLayout.addWidget(self.E3textcolorButton,3,1)
        valueLayout.addWidget(self.marker3typeComboBox,3,2)
        valueLayout.addWidget(self.E3thicknessSpinBox,3,3)
        valueLayout.addWidget(self.E3alphaSpinBox,3,4)
        valueLayout.addWidget(self.E3sizeSpinBox,3,5)
        valueLayout.addWidget(self.E4colorButton,4,0)
        valueLayout.addWidget(self.E4textcolorButton,4,1)
        valueLayout.addWidget(self.marker4typeComboBox,4,2)
        valueLayout.addWidget(self.E4thicknessSpinBox,4,3)
        valueLayout.addWidget(self.E4alphaSpinBox,4,4)
        valueLayout.addWidget(self.E4sizeSpinBox,4,5)
        valueHLayout = QHBoxLayout()
        valueHLayout.addStretch()
        valueHLayout.addLayout(valueLayout)
        valueHLayout.addStretch()
        ### tab5 layout
        tab5Layout = QGridLayout()
        tab5Layout.addWidget(eventtitlelabel,0,0)
        tab5Layout.addWidget(actiontitlelabel,0,1)
        tab5Layout.addWidget(commandtitlelabel,0,2)
        tab5Layout.addWidget(offsettitlelabel,0,3)
        tab5Layout.addWidget(factortitlelabel,0,4)
        tab5Layout.addWidget(min_titlelabel,0,5)
        tab5Layout.addWidget(max_titlelabel,0,6)
        tab5Layout.addWidget(sliderBernoullititlelabel,0,7)
        tab5Layout.addWidget(slidercoarsetitlelabel,0,8)
        tab5Layout.addWidget(slidertemptitlelabel,0,9)
        tab5Layout.addWidget(sliderunittitlelabel,0,10)
        tab5Layout.addWidget(self.E1visibility,1,0)
        tab5Layout.addWidget(self.E2visibility,2,0)
        tab5Layout.addWidget(self.E3visibility,3,0)
        tab5Layout.addWidget(self.E4visibility,4,0)
        tab5Layout.addWidget(self.E1action,1,1)
        tab5Layout.addWidget(self.E2action,2,1)
        tab5Layout.addWidget(self.E3action,3,1)
        tab5Layout.addWidget(self.E4action,4,1)
        tab5Layout.addWidget(self.E1command,1,2)
        tab5Layout.addWidget(self.E2command,2,2)
        tab5Layout.addWidget(self.E3command,3,2)
        tab5Layout.addWidget(self.E4command,4,2)
        tab5Layout.addWidget(self.E1offset,1,3)
        tab5Layout.addWidget(self.E2offset,2,3)
        tab5Layout.addWidget(self.E3offset,3,3)
        tab5Layout.addWidget(self.E4offset,4,3)
        tab5Layout.addWidget(self.E1factor,1,4)
        tab5Layout.addWidget(self.E2factor,2,4)
        tab5Layout.addWidget(self.E3factor,3,4)
        tab5Layout.addWidget(self.E4factor,4,4)
        tab5Layout.addWidget(self.E1_min,1,5)
        tab5Layout.addWidget(self.E2_min,2,5)
        tab5Layout.addWidget(self.E3_min,3,5)
        tab5Layout.addWidget(self.E4_min,4,5)
        tab5Layout.addWidget(self.E1_max,1,6)
        tab5Layout.addWidget(self.E2_max,2,6)
        tab5Layout.addWidget(self.E3_max,3,6)
        tab5Layout.addWidget(self.E4_max,4,6)
        tab5Layout.addWidget(self.E1slider_bernoulli,1,7,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E2slider_bernoulli,2,7,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E3slider_bernoulli,3,7,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E4slider_bernoulli,4,7,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E1slider_coarse,1,8,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E2slider_coarse,2,8,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E3slider_coarse,3,8,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E4slider_coarse,4,8,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E1slider_temp,1,9,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E2slider_temp,2,9,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E3slider_temp,3,9,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E4slider_temp,4,9,Qt.AlignmentFlag.AlignCenter)
        tab5Layout.addWidget(self.E1unit,1,10)
        tab5Layout.addWidget(self.E2unit,2,10)
        tab5Layout.addWidget(self.E3unit,3,10)
        tab5Layout.addWidget(self.E4unit,4,10)
        SliderHelpHBox = QHBoxLayout()
        SliderHelpHBox.addStretch()
        SliderHelpHBox.addWidget(helpsliderDialogButton)
        C5VBox = QVBoxLayout()
        C5VBox.addLayout(tab5Layout)
        C5VBox.addStretch()
        C5VBox.addLayout(SliderHelpHBox)
        ### tab6 layout
        tab6Layout = QGridLayout()
        tab6Layout.addWidget(qeventtitlelabel,0,0,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(sourcetitlelabel,0,1,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(quantifierSVtitlelabel,0,2,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(mintitlelabel,0,3,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(maxtitlelabel,0,4,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(coarsetitlelabel,0,5,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(quantifieractiontitlelabel,0,6,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E1active,1,0)
        tab6Layout.addWidget(self.E2active,2,0)
        tab6Layout.addWidget(self.E3active,3,0)
        tab6Layout.addWidget(self.E4active,4,0)
        tab6Layout.addWidget(self.E1SourceComboBox,1,1)
        tab6Layout.addWidget(self.E2SourceComboBox,2,1)
        tab6Layout.addWidget(self.E3SourceComboBox,3,1)
        tab6Layout.addWidget(self.E4SourceComboBox,4,1)
        tab6Layout.addWidget(self.E1quantifierSV,1,2,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E2quantifierSV,2,2,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E3quantifierSV,3,2,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E4quantifierSV,4,2,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E1min,1,3)
        tab6Layout.addWidget(self.E2min,2,3)
        tab6Layout.addWidget(self.E3min,3,3)
        tab6Layout.addWidget(self.E4min,4,3)
        tab6Layout.addWidget(self.E1max,1,4)
        tab6Layout.addWidget(self.E2max,2,4)
        tab6Layout.addWidget(self.E3max,3,4)
        tab6Layout.addWidget(self.E4max,4,4)
        tab6Layout.addWidget(self.E1coarse,1,5,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E2coarse,2,5,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E3coarse,3,5,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E4coarse,4,5,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E1quantifieraction,1,6,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E2quantifieraction,2,6,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E3quantifieraction,3,6,Qt.AlignmentFlag.AlignCenter)
        tab6Layout.addWidget(self.E4quantifieraction,4,6,Qt.AlignmentFlag.AlignCenter)
        QuantifierApplyHBox = QHBoxLayout()
        QuantifierApplyHBox.addStretch()
        QuantifierApplyHBox.addWidget(self.clusterEventsFlag)
        QuantifierApplyHBox.addStretch()
        QuantifierApplyHBox.addWidget(applyquantifierbutton)
        C6HBox = QHBoxLayout()
        C6HBox.addStretch()
        C6HBox.addLayout(tab6Layout)
        C6HBox.addStretch()
        C6VBox = QVBoxLayout()
        C6VBox.addLayout(C6HBox)
        C6VBox.addStretch()
        C6VBox.addLayout(QuantifierApplyHBox)
###########################################
        #tab layout
        self.TabWidget = QTabWidget()
        self.TabWidget.currentChanged.connect(self.tabSwitched)
        C1Widget = QWidget()
        C1Widget.setLayout(tab1layout)
        self.TabWidget.addTab(C1Widget,QApplication.translate("Tab","Config"))
        C1Widget.setContentsMargins(5, 0, 5, 0)
        C2Widget = QWidget()
        C2Widget.setLayout(tab2layout)
        if self.app.artisanviewerMode:
            C2Widget.setEnabled(False)
        self.TabWidget.addTab(C2Widget,QApplication.translate("Tab","Buttons"))
        C5Widget = QWidget()
        C5Widget.setLayout(C5VBox)
        if self.app.artisanviewerMode:
            C5Widget.setEnabled(False)
        self.TabWidget.addTab(C5Widget,QApplication.translate("Tab","Sliders"))
        C6Widget = QWidget()
        C6Widget.setLayout(C6VBox)
        self.TabWidget.addTab(C6Widget,QApplication.translate("Tab","Quantifiers"))
        C3Widget = QWidget()
        C3Widget.setLayout(tab3layout)
        self.TabWidget.addTab(C3Widget,QApplication.translate("Tab","Palettes"))
        valueVLayout = QVBoxLayout()
        valueVLayout.addLayout(valueHLayout)
        valueVLayout.addStretch()
        C4Widget = QWidget()
        C4Widget.setLayout(valueVLayout)
        self.TabWidget.addTab(C4Widget,QApplication.translate("Tab","Style"))

        self.TabWidget.addTab(C7Widget,QApplication.translate("Tab","Annotations"))

        self.TabWidget.setCurrentIndex(activeTab)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.TabWidget)
        mainLayout.setSpacing(5)
        mainLayout.setContentsMargins(5, 15, 5, 5)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        if platform.system() == 'Windows':
            self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok)
        else:
            self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok).setFocus()

    @pyqtSlot(str)
    def changeSpecialeventEdit1(self):
        self.specialeventEditchanged(1)
    @pyqtSlot(str)
    def changeSpecialeventEdit2(self):
        self.specialeventEditchanged(2)
    @pyqtSlot(str)
    def changeSpecialeventEdit3(self):
        self.specialeventEditchanged(3)
    @pyqtSlot(str)
    def changeSpecialeventEdit4(self):
        self.specialeventEditchanged(4)
    
    def specialeventEditchanged(self,n):
        if n == 1:
            self.E1Preview1.setText(self.aw.qmc.parseSpecialeventannotation(self.E1Edit.text(),eventnum=0,applyto="preview",postFCs=False))
            self.E1Preview2.setText(self.aw.qmc.parseSpecialeventannotation(self.E1Edit.text(),eventnum=0,applyto="preview",postFCs=True))
            self.aw.qmc.specialeventannotations[0] = self.E1Edit.text()
        if n == 2:
            self.E2Preview1.setText(self.aw.qmc.parseSpecialeventannotation(self.E2Edit.text(),eventnum=0,applyto="preview",postFCs=False))
            self.E2Preview2.setText(self.aw.qmc.parseSpecialeventannotation(self.E2Edit.text(),eventnum=0,applyto="preview",postFCs=True))
            self.aw.qmc.specialeventannotations[1] = self.E2Edit.text()
        if n == 3:
            self.E3Preview1.setText(self.aw.qmc.parseSpecialeventannotation(self.E3Edit.text(),eventnum=0,applyto="preview",postFCs=False))
            self.E3Preview2.setText(self.aw.qmc.parseSpecialeventannotation(self.E3Edit.text(),eventnum=0,applyto="preview",postFCs=True))
            self.aw.qmc.specialeventannotations[2] = self.E3Edit.text()
        if n == 4:
            self.E4Preview1.setText(self.aw.qmc.parseSpecialeventannotation(self.E4Edit.text(),eventnum=0,applyto="preview",postFCs=False))
            self.E4Preview2.setText(self.aw.qmc.parseSpecialeventannotation(self.E4Edit.text(),eventnum=0,applyto="preview",postFCs=True))
            self.aw.qmc.specialeventannotations[3] = self.E4Edit.text()

    @pyqtSlot(bool)
    def backuppaletteeventbuttonsSlot(self,_):
        self.aw.backuppaletteeventbuttons(self.aw.buttonpalette,self.aw.buttonpalettemaxlen)
        self.transferpalettecombobox.setCurrentIndex(-1)

    @pyqtSlot(bool)
    def restorepaletteeventbuttons(self,_):
        filename = self.aw.ArtisanOpenFileDialog(msg=QApplication.translate("Message","Load Palettes"),path=self.aw.profilepath)
        if filename:
            maxlen = self.aw.loadPalettes(filename,self.aw.buttonpalette)
            if maxlen is not None:
                self.aw.buttonpalettemaxlen = maxlen
            self.updatePalettePopup()

    def selectionChanged(self):
        selected = self.eventbuttontable.selectedRanges()
        if selected and len(selected) > 0:
            self.insertButton.setEnabled(True)
        else:
            self.insertButton.setEnabled(False)

    @pyqtSlot(int)
    def changeShowMet(self,_):
        self.aw.qmc.showmet = not self.aw.qmc.showmet
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        
    @pyqtSlot(int)
    def changeShowTimeguide(self,_):
        self.aw.qmc.showtimeguide = not self.aw.qmc.showtimeguide

    @pyqtSlot(bool)
    def applyQuantifiers(self,_):
        self.saveQuantifierSettings()
        # recompute the 4 event quantifier linspaces
        self.aw.computeLinespaces()
        # remove previous quantifier events
        # recompute quantifier events
        redraw = False
        for i in range(4):
            if self.aw.eventquantifieractive[i]:
                temp,timex = self.aw.quantifier2tempandtime(i)
                if temp:
                    # a temp curve exists
                    linespace = self.aw.eventquantifierlinspaces[i]
                    if self.aw.eventquantifiercoarse[i]:
                        linespacethreshold = abs(linespace[1] - linespace[0]) * self.aw.eventquantifierthresholdcoarse
                    else:
                        linespacethreshold = abs(linespace[1] - linespace[0]) * self.aw.eventquantifierthresholdfine
                    # loop over that data and classify each value
                    ld = None # last digitized value
                    lt = None # last digitized temp value
                    for ii in range(len(temp)):
                        t = temp[ii]
                        if t != -1: # -1 is an error value
                            d = self.aw.digitize(t,linespace,self.aw.eventquantifiercoarse[i],self.aw.eventslidermin[i])
                            if d is not None and (ld is None or ld != d):
                                # take only changes
                                # and only if significantly different than previous to avoid fluktuation
                                if ld is None or lt is None or linespacethreshold < abs(t - lt):
                                    # establish this one
                                    ld = d
                                    lt = t
                                    # add to event table
                                    self.aw.qmc.specialevents.append(self.aw.qmc.time2index(timex[ii]))
                                    self.aw.qmc.specialeventstype.append(i)
                                    self.aw.qmc.specialeventsStrings.append("Q"+ self.aw.qmc.eventsvalues(float(d+1)))
                                    self.aw.qmc.specialeventsvalue.append(float(d+1))
                                    self.aw.qmc.fileDirty()
                    redraw = True
        if self.aw.clusterEventsFlag:
            self.aw.clusterEvents(True)
        if redraw:
            self.aw.qmc.redraw(recomputeAllDeltas=False)

    @pyqtSlot(int)
    def tabSwitched(self,i):
        self.closeHelp()
        if i == 0:
            self.saveSliderSettings()
            self.saveQuantifierSettings()
        elif i == 1: # switched to Button tab
            self.createEventbuttonTable()
            self.saveSliderSettings()
            self.saveQuantifierSettings()
            self.saveAnnotationsSettings()
        elif i == 2: # switched to Slider tab
            self.saveQuantifierSettings()
            self.saveAnnotationsSettings()
        elif i == 3: # switched to Quantifier tab
            self.saveSliderSettings()
            self.saveAnnotationsSettings()
        elif i == 4: # switched to Palette tab
            # store slider settings from Slider tab to global variables
            # store sliders
            self.saveSliderSettings()
            self.saveQuantifierSettings()
#            # store buttons (not done here anymore: buttons are saved on leaving the dialog with OK)
#            self.savetableextraeventbutton()
            self.saveAnnotationsSettings()
        elif i == 5: # switched to Style tab
            self.updateStyleTab()
            self.saveSliderSettings()
            self.saveQuantifierSettings()
            self.saveAnnotationsSettings()
        elif i == 6: # switched to Annotations tab
            self.updateAnnotationsTab()
            self.saveQuantifierSettings()

    def updateQuantifierTab(self):
        self.E1active.setText(self.etype0.text())
        self.E2active.setText(self.etype1.text())
        self.E3active.setText(self.etype2.text())
        self.E4active.setText(self.etype3.text())
        self.E1active.setChecked(bool(self.aw.eventquantifieractive[0]))
        self.E2active.setChecked(bool(self.aw.eventquantifieractive[1]))
        self.E3active.setChecked(bool(self.aw.eventquantifieractive[2]))
        self.E4active.setChecked(bool(self.aw.eventquantifieractive[3]))
        self.E1coarse.setChecked(bool(self.aw.eventquantifiercoarse[0]))
        self.E2coarse.setChecked(bool(self.aw.eventquantifiercoarse[1]))
        self.E3coarse.setChecked(bool(self.aw.eventquantifiercoarse[2]))
        self.E4coarse.setChecked(bool(self.aw.eventquantifiercoarse[3]))
        self.E1quantifieraction.setChecked(bool(self.aw.eventquantifieraction[0]))
        self.E2quantifieraction.setChecked(bool(self.aw.eventquantifieraction[1]))
        self.E3quantifieraction.setChecked(bool(self.aw.eventquantifieraction[2]))
        self.E4quantifieraction.setChecked(bool(self.aw.eventquantifieraction[3]))
        self.E1quantifierSV.setChecked(bool(self.aw.eventquantifierSV[0]))
        self.E2quantifierSV.setChecked(bool(self.aw.eventquantifierSV[1]))
        self.E3quantifierSV.setChecked(bool(self.aw.eventquantifierSV[2]))
        self.E4quantifierSV.setChecked(bool(self.aw.eventquantifierSV[3]))
        if self.aw.eventquantifiersource[0] < len(self.curvenames):
            self.E1SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[0])
        if self.aw.eventquantifiersource[1] < len(self.curvenames):
            self.E2SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[1])
        if self.aw.eventquantifiersource[2] < len(self.curvenames):
            self.E3SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[2])
        if self.aw.eventquantifiersource[3] < len(self.curvenames):
            self.E4SourceComboBox.setCurrentIndex(self.aw.eventquantifiersource[3])
        self.E1min.setValue(self.aw.eventquantifiermin[0])
        self.E2min.setValue(self.aw.eventquantifiermin[1])
        self.E3min.setValue(self.aw.eventquantifiermin[2])        
        self.E4min.setValue(self.aw.eventquantifiermin[3])
        self.E1max.setValue(self.aw.eventquantifiermax[0])
        self.E2max.setValue(self.aw.eventquantifiermax[1])
        self.E3max.setValue(self.aw.eventquantifiermax[2])
        self.E4max.setValue(self.aw.eventquantifiermax[3])

    def updateStyleTab(self):
        # update color button texts
        self.E1colorButton.setText(self.etype0.text())
        self.E2colorButton.setText(self.etype1.text())
        self.E3colorButton.setText(self.etype2.text())
        self.E4colorButton.setText(self.etype3.text())
        self.E1textcolorButton.setText(self.etype0.text())
        self.E2textcolorButton.setText(self.etype1.text())
        self.E3textcolorButton.setText(self.etype2.text())
        self.E4textcolorButton.setText(self.etype3.text())
        self.E1colorButton.setMinimumWidth(max(self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok).width(),self.E1textcolorButton.minimumSizeHint().width()))
        self.E1textcolorButton.setMinimumWidth(max(self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok).width(),self.E1textcolorButton.minimumSizeHint().width()))
        self.E1colorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[0] + "; color: " + self.aw.qmc.EvalueTextColor[0] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E2colorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[1] + "; color: " + self.aw.qmc.EvalueTextColor[1] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E3colorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[2] + "; color: " + self.aw.qmc.EvalueTextColor[2] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E4colorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[3] + "; color: " + self.aw.qmc.EvalueTextColor[3] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E1textcolorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[0] + "; color: " + self.aw.qmc.EvalueTextColor[0] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E2textcolorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[1] + "; color: " + self.aw.qmc.EvalueTextColor[1] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E3textcolorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[2] + "; color: " + self.aw.qmc.EvalueTextColor[2] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        self.E4textcolorButton.setStyleSheet("background-color: " + self.aw.qmc.EvalueColor[3] + "; color: " + self.aw.qmc.EvalueTextColor[3] + "; border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;")
        
        # update markers
        if self.aw.qmc.EvalueMarker[0] in self.markervals:
            self.marker1typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[0]))
        else:
            self.marker1typeComboBox.setCurrentIndex(0)
        if self.aw.qmc.EvalueMarker[1] in self.markervals:
            self.marker2typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[1]))
        else:
            self.marker2typeComboBox.setCurrentIndex(0)
        if self.aw.qmc.EvalueMarker[2] in self.markervals:
            self.marker3typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[2]))
        else:
            self.marker3typeComboBox.setCurrentIndex(0)
        if self.aw.qmc.EvalueMarker[3] in self.markervals:
            self.marker4typeComboBox.setCurrentIndex(self.markervals.index(self.aw.qmc.EvalueMarker[3]))
        else:
            self.marker4typeComboBox.setCurrentIndex(0)
        # line thickness
        self.E1thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[0])
        self.E2thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[1])
        self.E3thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[2])
        self.E4thicknessSpinBox.setValue(self.aw.qmc.Evaluelinethickness[3])
        # opacity
        self.E1alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[0])
        self.E2alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[1])
        self.E3alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[2])
        self.E4alphaSpinBox.setValue(self.aw.qmc.Evaluealpha[3])
        # marker sizes
        self.E1sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[0])
        self.E2sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[1])
        self.E3sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[2])
        self.E4sizeSpinBox.setValue(self.aw.qmc.EvalueMarkerSize[3])

    def updateSliderTab(self):
        # set event names
        self.E1visibility.setText(self.etype0.text())
        self.E2visibility.setText(self.etype1.text())
        self.E3visibility.setText(self.etype2.text())
        self.E4visibility.setText(self.etype3.text())
        # set slider visibility
        self.E1visibility.setChecked(bool(self.aw.eventslidervisibilities[0]))
        self.E2visibility.setChecked(bool(self.aw.eventslidervisibilities[1]))
        self.E3visibility.setChecked(bool(self.aw.eventslidervisibilities[2]))
        self.E4visibility.setChecked(bool(self.aw.eventslidervisibilities[3]))
        # set slider action
        self.E1action.setCurrentIndex(self.aw.eventslideractions[0])
        self.E2action.setCurrentIndex(self.aw.eventslideractions[1])
        self.E3action.setCurrentIndex(self.aw.eventslideractions[2])
        self.E4action.setCurrentIndex(self.aw.eventslideractions[3])
        # set slider command
        self.E1command.setText(self.aw.eventslidercommands[0])
        self.E2command.setText(self.aw.eventslidercommands[1])
        self.E3command.setText(self.aw.eventslidercommands[2])
        self.E4command.setText(self.aw.eventslidercommands[3])
        # set slider offset
        self.E1offset.setValue(self.aw.eventslideroffsets[0])
        self.E2offset.setValue(self.aw.eventslideroffsets[1])
        self.E3offset.setValue(self.aw.eventslideroffsets[2])
        self.E4offset.setValue(self.aw.eventslideroffsets[3])
        # set slider factors
        self.E1factor.setValue(self.aw.eventsliderfactors[0])
        self.E2factor.setValue(self.aw.eventsliderfactors[1])
        self.E3factor.setValue(self.aw.eventsliderfactors[2])
        self.E4factor.setValue(self.aw.eventsliderfactors[3])
        # set slider min
        self.E1_min.setValue(self.aw.eventslidermin[0])
        self.E2_min.setValue(self.aw.eventslidermin[1])
        self.E3_min.setValue(self.aw.eventslidermin[2])
        self.E4_min.setValue(self.aw.eventslidermin[3])
        # set slider max
        self.E1_max.setValue(self.aw.eventslidermax[0])
        self.E2_max.setValue(self.aw.eventslidermax[1])
        self.E3_max.setValue(self.aw.eventslidermax[2])
        self.E4_max.setValue(self.aw.eventslidermax[3])
        # set slider Bernoulli
        self.E1slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[0]))
        self.E2slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[1]))
        self.E3slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[2]))
        self.E4slider_bernoulli.setChecked(bool(self.aw.eventsliderBernoulli[3]))
        # set slider coarse
        self.E1slider_coarse.setChecked(bool(self.aw.eventslidercoarse[0]))
        self.E2slider_coarse.setChecked(bool(self.aw.eventslidercoarse[1]))
        self.E3slider_coarse.setChecked(bool(self.aw.eventslidercoarse[2]))
        self.E4slider_coarse.setChecked(bool(self.aw.eventslidercoarse[3]))
        # set slider temp
        self.E1slider_temp.setChecked(bool(self.aw.eventslidertemp[0]))
        self.E2slider_temp.setChecked(bool(self.aw.eventslidertemp[1]))
        self.E3slider_temp.setChecked(bool(self.aw.eventslidertemp[2]))
        self.E4slider_temp.setChecked(bool(self.aw.eventslidertemp[3]))
        # set slider units
        self.E1unit.setText(self.aw.eventsliderunits[0])
        self.E2unit.setText(self.aw.eventsliderunits[1])
        self.E3unit.setText(self.aw.eventsliderunits[2])
        self.E4unit.setText(self.aw.eventsliderunits[3])
        
    def updateAnnotationsTab(self):
        # set event names
        self.E1AnnoVisibility.setText(self.etype0.text())
        self.E2Annovisibility.setText(self.etype1.text())
        self.E3Annovisibility.setText(self.etype2.text())
        self.E4Annovisibility.setText(self.etype3.text())
        # set annotation visibility
        self.E1AnnoVisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[0]))
        self.E2Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[1]))
        self.E3Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[2]))
        self.E4Annovisibility.setChecked(bool(self.aw.qmc.specialeventannovisibilities[3]))

    @pyqtSlot(int)
    def setElinethickness0(self,_):
        self.setElinethickness(0)
    @pyqtSlot(int)
    def setElinethickness1(self,_):
        self.setElinethickness(1)
    @pyqtSlot(int)
    def setElinethickness2(self,_):
        self.setElinethickness(2)
    @pyqtSlot(int)
    def setElinethickness3(self,_):
        self.setElinethickness(3)
        
    def setElinethickness(self,val):
        self.E1thicknessSpinBox.setDisabled(True)
        self.E2thicknessSpinBox.setDisabled(True)
        self.E3thicknessSpinBox.setDisabled(True)
        self.E4thicknessSpinBox.setDisabled(True)
        if val == 0:
            self.aw.qmc.Evaluelinethickness[0] = self.E1thicknessSpinBox.value()
        if val == 1:
            self.aw.qmc.Evaluelinethickness[1] = self.E2thicknessSpinBox.value()
        if val == 2:
            self.aw.qmc.Evaluelinethickness[2] = self.E3thicknessSpinBox.value()
        if val == 3:
            self.aw.qmc.Evaluelinethickness[3] = self.E4thicknessSpinBox.value()
        self.E1thicknessSpinBox.setDisabled(False)
        self.E2thicknessSpinBox.setDisabled(False)
        self.E3thicknessSpinBox.setDisabled(False)
        self.E4thicknessSpinBox.setDisabled(False)
        self.aw.qmc.redraw()

    @pyqtSlot(int)
    def setEmarkersize0(self,_):
        self.setEmarkersize(0)
    @pyqtSlot(int)
    def setEmarkersize1(self,_):
        self.setEmarkersize(1)
    @pyqtSlot(int)
    def setEmarkersize2(self,_):
        self.setEmarkersize(2)
    @pyqtSlot(int)
    def setEmarkersize3(self,_):
        self.setEmarkersize(3)

    def setEmarkersize(self,val):
        self.E1sizeSpinBox.setDisabled(True)
        self.E2sizeSpinBox.setDisabled(True)
        self.E3sizeSpinBox.setDisabled(True)
        self.E4sizeSpinBox.setDisabled(True)
        if val == 0:
            self.aw.qmc.EvalueMarkerSize[0] = self.E1sizeSpinBox.value()
        if val == 1:
            self.aw.qmc.EvalueMarkerSize[1] = self.E2sizeSpinBox.value()
        if val == 2:
            self.aw.qmc.EvalueMarkerSize[2] = self.E3sizeSpinBox.value()
        if val == 3:
            self.aw.qmc.EvalueMarkerSize[3] = self.E4sizeSpinBox.value()
        self.E1sizeSpinBox.setDisabled(False)
        self.E2sizeSpinBox.setDisabled(False)
        self.E3sizeSpinBox.setDisabled(False)
        self.E4sizeSpinBox.setDisabled(False)
        self.aw.qmc.redraw()

    @pyqtSlot(float)
    def setElinealpha0(self,_):
        self.setElinealpha(0)
    @pyqtSlot(float)
    def setElinealpha1(self,_):
        self.setElinealpha(1)
    @pyqtSlot(float)
    def setElinealpha2(self,_):
        self.setElinealpha(2)
    @pyqtSlot(float)
    def setElinealpha3(self,_):
        self.setElinealpha(3)

    def setElinealpha(self,val):
        self.E1alphaSpinBox.setDisabled(True)
        self.E2alphaSpinBox.setDisabled(True)
        self.E3alphaSpinBox.setDisabled(True)
        self.E4alphaSpinBox.setDisabled(True)
        if val == 0:
            self.aw.qmc.Evaluealpha[0] = self.E1alphaSpinBox.value()
        if val == 1:
            self.aw.qmc.Evaluealpha[1] = self.E2alphaSpinBox.value()
        if val == 2:
            self.aw.qmc.Evaluealpha[2] = self.E3alphaSpinBox.value()
        if val == 3:
            self.aw.qmc.Evaluealpha[3] = self.E4alphaSpinBox.value()
        self.E1alphaSpinBox.setDisabled(False)
        self.E2alphaSpinBox.setDisabled(False)
        self.E3alphaSpinBox.setDisabled(False)
        self.E4alphaSpinBox.setDisabled(False)
        self.aw.qmc.redraw()

    @pyqtSlot(bool)
    def transferbuttonstoSlot(self,_):
        self.transferbuttonsto()
    
    def transferbuttonsto(self,pindex=None):
        if pindex is None:
            pindex = self.transferpalettecombobox.currentIndex()
        if 0 <= pindex < 10:
            copy = []
            copy.append(self.extraeventstypes[:])
            copy.append(self.extraeventsvalues[:])
            copy.append(self.extraeventsactions[:])
            copy.append(self.extraeventsvisibility[:])
            copy.append(self.extraeventsactionstrings[:])
            copy.append(self.extraeventslabels[:])
            copy.append(self.extraeventsdescriptions[:])
            copy.append(self.extraeventbuttoncolor[:])
            copy.append(self.extraeventbuttontextcolor[:])
            # added slider settings
            copy.append(self.aw.eventslidervisibilities[:])
            copy.append(self.aw.eventslideractions[:])
            copy.append(self.aw.eventslidercommands[:])
            copy.append(self.aw.eventslideroffsets[:])
            copy.append(self.aw.eventsliderfactors[:])
            # added quantifier settings
            copy.append(self.aw.eventquantifieractive[:])
            copy.append(self.aw.eventquantifiersource[:])
            copy.append(self.aw.eventquantifiermin[:])
            copy.append(self.aw.eventquantifiermax[:])
            copy.append(self.aw.eventquantifiercoarse[:])
            # added slider min/max
            copy.append(self.aw.eventslidermin[:])
            copy.append(self.aw.eventslidermax[:])
            # added slider coarse
            copy.append(self.aw.eventslidercoarse[:])
            # added slider temp
            copy.append(self.aw.eventslidertemp[:])
            # added slider unit
            copy.append(self.aw.eventsliderunits[:])
            # added slider Bernoulli
            copy.append(self.aw.eventsliderBernoulli[:])
            # added palette label
            copy.append(self.transferpalettecurrentLabelEdit.text())
            # added quantifier actions
            copy.append(self.aw.eventquantifieraction[:])
            # added quantifier SV
            copy.append(self.aw.eventquantifierSV[:])
            
            self.aw.buttonpalette[pindex] = copy
            self.aw.buttonpalettemaxlen[pindex] = self.aw.buttonlistmaxlen
            self.transferpalettecombobox.setCurrentIndex(-1)
            self.updatePalettePopup()


    def localSetbuttonsfrom(self,pindex):
        copy = self.aw.buttonpalette[pindex][:]
        if len(copy):
            self.extraeventstypes = copy[0][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventsvalues = copy[1][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventsactions = copy[2][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventsvisibility = copy[3][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventsactionstrings = copy[4][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventslabels = copy[5][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventsdescriptions = copy[6][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventbuttoncolor = copy[7][:] # pylint: disable=attribute-defined-outside-init
            self.extraeventbuttontextcolor = copy[8][:] # pylint: disable=attribute-defined-outside-init
            # added slider settings
            if len(copy)>9 and len(copy[9]) == 4:
                self.aw.eventslidervisibilities = copy[9][:]
            else:
                self.aw.eventslidervisibilities = [0,0,0,0]
            if len(copy)>10 and len(copy[10]) == 4:
                self.aw.eventslideractions = copy[10][:]
            else:
                self.aw.eventslideractions = [0,0,0,0]
            if len(copy)>11 and len(copy[11]) == 4:
                self.aw.eventslidercommands = copy[11][:]
            else:
                self.aw.eventslidercommands = ["","","",""]
            if len(copy)>12 and len(copy[12]) == 4:
                self.aw.eventslideroffsets = copy[12][:]
            else:
                self.aw.eventslideroffsets = [0,0,0,0]
            if len(copy)>13 and len(copy[13]) == 4:
                self.aw.eventsliderfactors = copy[13][:]
            else:
                self.aw.eventsliderfactors = [1.0,1.0,1.0,1.0]
            # quantifiers
            if len(copy)>14 and len(copy[14]) == 4:
                self.aw.eventquantifieractive = copy[14][:]
            else:
                self.aw.eventquantifieractive = [0,0,0,0]
            if len(copy)>15 and len(copy[15]) == 4:
                self.aw.eventquantifiersource = copy[15][:]
            else:
                self.aw.eventquantifiersource = [0,0,0,0]
            if len(copy)>16 and len(copy[16]) == 4:
                self.aw.eventquantifiermin = copy[16][:]
            else:
                self.aw.eventquantifiermin = [0,0,0,0]
            if len(copy)>17 and len(copy[17]) == 4:
                self.aw.eventquantifiermax = copy[17][:]
            else:
                self.aw.eventquantifiermax = [100,100,100,100]
            if len(copy)>18 and len(copy[18]) == 4:
                self.aw.eventquantifiercoarse = copy[18][:]
            else:
                self.aw.eventquantifiercoarse = [0,0,0,0]
            # slider min/max
            if len(copy)>19 and len(copy[19]) == 4:
                self.aw.eventslidermin = copy[19][:]
            else:
                self.aw.eventslidermin = [0,0,0,0]
            if len(copy)>20 and len(copy[20]) == 4:
                self.aw.eventslidermax = copy[20][:]
            else:
                self.aw.eventslidermax = [100,100,100,100]
            # slider coarse
            if len(copy)>21 and len(copy[21]) == 4:
                self.aw.eventslidercoarse = copy[21][:]
            else:
                self.aw.eventslidercoarse = [0,0,0,0]
            # slide temp
            if len(copy)>22 and len(copy[22]) == 4:
                self.aw.eventslidertemp = copy[22][:]
            else:
                self.aw.eventslidertemp = [0,0,0,0]
            # slider units
            if len(copy)>23 and len(copy[23]) == 4:
                self.aw.eventsliderunits = copy[23][:]
            else:
                self.aw.eventsliderunits = ["","","",""]
            # slider bernoulli
            if len(copy)>24 and len(copy[24]) == 4:
                self.aw.eventsliderBernoulli = copy[24][:]
            else:
                self.aw.eventsliderBernoulli = [0,0,0,0]
            # palette label
            if len(copy)>25:
                self.aw.buttonpalette_label = copy[25]
            else:
                self.aw.buttonpalette_label = self.aw.buttonpalette_default_label
            if len(copy)>26 and len(copy[26]) == 4:
                self.aw.eventquantifieraction = copy[26][:]
            else:
                self.aw.eventquantifieraction = [0,0,0,0]
            if len(copy)>27 and len(copy[27]) == 4:
                self.aw.eventquantifierSV = copy[27][:]
            else:
                self.aw.eventquantifierSV = [0,0,0,0]
            
            self.aw.buttonlistmaxlen = self.aw.buttonpalettemaxlen[pindex]
            
            return 1  #success
        return 0  #failed

    @pyqtSlot(bool)
    def setbuttonsfrom(self,_):
        pindex = self.transferpalettecombobox.currentIndex()
        if 0 <= pindex < 10:
            answer = self.localSetbuttonsfrom(pindex)
            if answer:
                self.nbuttonsSpinBox.setValue(self.aw.buttonlistmaxlen)
                self.transferpalettecurrentLabelEdit.setText(self.aw.buttonpalette_label)
                self.updatePalettePopup()
                self.updateSliderTab()
                self.updateQuantifierTab()
                self.createEventbuttonTable()
                self.transferpalettecombobox.setCurrentIndex(-1)
    
    def updatePalettePopup(self):
        self.transferpalettecombobox.clear()
        palettelist = []
        for i in range(len(self.aw.buttonpalette)):
            palettelist.append("#{} {}".format(str(i),self.aw.buttonpalette[i][25]))
        self.transferpalettecombobox.addItems(palettelist)
        self.transferpalettecombobox.setCurrentIndex(-1)

    #applys a pattern of colors
    @pyqtSlot(int)
    def colorizebuttons(self,pattern=0):
        if self.changingcolorflag:
            n = self.colorSpinBox.value()
            self.colorSpinBox.setValue(n-1)
            return
        self.changingcolorflag = True

        if not pattern:
            pattern = self.colorSpinBox.value()

        ncolumns = self.aw.buttonlistmaxlen
        nbuttons = len(self.extraeventstypes)

        nrows,extra = divmod(nbuttons,ncolumns)

        step = pattern
        bcolor = []

        if extra:
            nrows += 1
        gap = int(-1*(230-50)/ncolumns)
        #Color
        for i in range(nrows):
            for f in range(230,50,gap):
                color = QColor()
                color.setHsv(step,255,f,255)
                bcolor.append(str(color.name()))
            step += pattern*2

        #Apply Colors in Right Order
        for i in range(nbuttons):
            visualIndex = self.eventbuttontable.visualRow(i)
            self.extraeventbuttoncolor[i] = bcolor[visualIndex]
            #Choose text color
            if self.aw.colorDifference("white",bcolor[visualIndex]) > self.aw.colorDifference("black",bcolor[visualIndex]):
                self.extraeventbuttontextcolor[i] = "white"
            else:
                self.extraeventbuttontextcolor[i] = "black"
        self.changingcolorflag = False
        self.createEventbuttonTable()

    @pyqtSlot(int)
    def seteventmarker0(self,_):
        self.seteventmarker(0)
    @pyqtSlot(int)
    def seteventmarker1(self,_):
        self.seteventmarker(1)
    @pyqtSlot(int)
    def seteventmarker2(self,_):
        self.seteventmarker(2)
    @pyqtSlot(int)
    def seteventmarker3(self,_):
        self.seteventmarker(3)

    def seteventmarker(self,m):
        if m == 0 and self.marker1typeComboBox.currentIndex() != 0:
            self.aw.qmc.EvalueMarker[m] = str(self.markervals[self.marker1typeComboBox.currentIndex()])
        if m == 1 and self.marker2typeComboBox.currentIndex() != 0:
            self.aw.qmc.EvalueMarker[m] = str(self.markervals[self.marker2typeComboBox.currentIndex()])
        if m == 2 and self.marker3typeComboBox.currentIndex() != 0:
            self.aw.qmc.EvalueMarker[m] = str(self.markervals[self.marker3typeComboBox.currentIndex()])
        if m == 3 and self.marker4typeComboBox.currentIndex() != 0:
            self.aw.qmc.EvalueMarker[m] = str(self.markervals[self.marker4typeComboBox.currentIndex()])
        self.aw.qmc.redraw()

    @pyqtSlot(bool)
    def setcoloreventline0(self,_):
        self.setcoloreventline(0)
    @pyqtSlot(bool)
    def setcoloreventline1(self,_):
        self.setcoloreventline(1)
    @pyqtSlot(bool)
    def setcoloreventline2(self,_):
        self.setcoloreventline(2)
    @pyqtSlot(bool)
    def setcoloreventline3(self,_):
        self.setcoloreventline(3)
    
    def setcoloreventline(self,b):
        colorf = self.aw.colordialog(QColor(self.aw.qmc.EvalueColor[b]))
        if colorf.isValid():
            colorname = str(colorf.name())
            self.aw.qmc.EvalueColor[b] = colorname
            self.aw.updateSliderColors()
            self.updateStyleTab()
            self.aw.qmc.redraw()

    @pyqtSlot(bool)
    def setcoloreventtext0(self,_):
        self.setcoloreventtext(0)
    @pyqtSlot(bool)
    def setcoloreventtext1(self,_):
        self.setcoloreventtext(1)
    @pyqtSlot(bool)
    def setcoloreventtext2(self,_):
        self.setcoloreventtext(2)
    @pyqtSlot(bool)
    def setcoloreventtext3(self,_):
        self.setcoloreventtext(3)
    
    def setcoloreventtext(self,b):
        colorf = self.aw.colordialog(QColor(self.aw.qmc.EvalueTextColor[b]))
        if colorf.isValid():
            colorname = str(colorf.name())
            self.aw.qmc.EvalueTextColor[b] = colorname
            self.aw.updateSliderColors()
            self.updateStyleTab()
            self.aw.qmc.redraw()

    @pyqtSlot(int)
    def setbuttonlistmaxlen(self,_):
        self.aw.buttonlistmaxlen = self.nbuttonsSpinBox.value()

    def createEventbuttonTable(self):
        columns = 10
        if self.eventbuttontable is not None and self.eventbuttontable.columnCount() == columns:
            # rows have been already established
            # save the current columnWidth to reset them afte table creation
            self.aw.eventbuttontablecolumnwidths = [self.eventbuttontable.columnWidth(c) for c in range(self.eventbuttontable.columnCount())]
        
        self.nbuttonsSpinBox.setValue(self.aw.buttonlistmaxlen)
        nbuttons = len(self.extraeventstypes)

        # self.eventbuttontable.clear() # this crashes Ubuntu 16.04
#        if ndata != 0:
#            self.eventbuttontable.clearContents() # this crashes Ubuntu 16.04 if device table is empty and also sometimes else
#        self.eventbuttontable.clearSelection() # this seems to work also for Ubuntu 16.04

        self.eventbuttontable.setRowCount(nbuttons)
        self.eventbuttontable.setColumnCount(columns)
        self.eventbuttontable.setHorizontalHeaderLabels([QApplication.translate("Table","Label"),
                                                         QApplication.translate("Table","Description"),
                                                         QApplication.translate("Table","Type"),
                                                         QApplication.translate("Table","Value"),
                                                         QApplication.translate("Table","Action"),
                                                         QApplication.translate("Table","Documentation"),
                                                         QApplication.translate("Table","Visibility"),
                                                         QApplication.translate("Table","Color"),
                                                         QApplication.translate("Table","Text Color"),""])
        self.eventbuttontable.setAlternatingRowColors(True)
        self.eventbuttontable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.eventbuttontable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.eventbuttontable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.eventbuttontable.setShowGrid(True)

        self.eventbuttontable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        #Enable Drag Sorting
        self.eventbuttontable.setDragEnabled(False) # content not dragable, only vertical header!
        self.eventbuttontable.verticalHeader().setSectionsMovable(True)
        self.eventbuttontable.verticalHeader().setDragDropMode(QTableWidget.DragDropMode.InternalMove)

        visibility = [QApplication.translate("ComboBox","OFF"),
                      QApplication.translate("ComboBox","ON")]

        std_extra_events = [self.etype0.text(),self.etype1.text(),self.etype2.text(),self.etype3.text(),"--"]
        std_extra_events += [uchr(177) + e for e in std_extra_events[:-1]] # chr(241)
        std_extra_events.insert(0,QApplication.translate("Label", "")) # we prepend the empty item that does not create an event entry


        for i in range(nbuttons):
            #label
            labeledit = QLineEdit(self.extraeventslabels[i].replace(chr(10),"\\n"))
            labeledit.editingFinished.connect(self.setlabeleventbutton)

            #Description
            descriptionedit = QLineEdit(self.extraeventsdescriptions[i])
            descriptionedit.editingFinished.connect(self.setdescriptioneventbutton)

            #Type
            typeComboBox = MyQComboBox()
            typeComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            typeComboBox.addItems(std_extra_events)
            if self.extraeventstypes[i] == 9:  # we add an offset of +1 here to jump over the new EVENT entry
                idx = 5
            elif self.extraeventstypes[i] == 4:
                idx = 0
            else:
                idx = self.extraeventstypes[i]+1

            typeComboBox.setCurrentIndex(idx)
            typeComboBox.currentIndexChanged.connect(self.settypeeventbutton)

            #Values
            valueEdit = QLineEdit()
#            valueEdit.setValidator(QRegExpValidator(QRegExp(r"^100|\-?\d?\d?$"),self)) # QRegExp(r"^100|\d?\d?$"),self))
            valueEdit.setValidator(QIntValidator(-999, 999, valueEdit))
            valueEdit.setText(self.aw.qmc.eventsvalues(self.extraeventsvalues[i]))
            valueEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
            valueEdit.editingFinished.connect(self.setvalueeventbutton)

            #Action
            actionComboBox = MyQComboBox()
            actionComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            actionComboBox.addItems(["",
                                     QApplication.translate("ComboBox","Serial Command"),
                                     QApplication.translate("ComboBox","Call Program"),
                                     QApplication.translate("ComboBox","Multiple Event"),
                                     QApplication.translate("ComboBox","Modbus Command"),
                                     QApplication.translate("ComboBox","DTA Command"),
                                     QApplication.translate("ComboBox","IO Command"),
                                     QApplication.translate("ComboBox","Hottop Heater"),
                                     QApplication.translate("ComboBox","Hottop Fan"),
                                     QApplication.translate("ComboBox","Hottop Command"),
                                     QApplication.translate("ComboBox","p-i-d"),
                                     QApplication.translate("ComboBox","Fuji Command"),
                                     QApplication.translate("ComboBox","PWM Command"),
                                     QApplication.translate("ComboBox","VOUT Command"),
                                     QApplication.translate("ComboBox","S7 Command"),
                                     QApplication.translate("ComboBox","Aillio R1 Heater"),
                                     QApplication.translate("ComboBox","Aillio R1 Fan"),
                                     QApplication.translate("ComboBox","Aillio R1 Drum"),
                                     QApplication.translate("ComboBox","Aillio R1 Command"),
                                     QApplication.translate("ComboBox","Artisan Command"),
                                     QApplication.translate("ComboBox","RC Command"),
                                     QApplication.translate("ComboBox","WebSocket Command")])
            act = self.extraeventsactions[i]
            if act > 7:
                act = act - 1
            actionComboBox.setCurrentIndex(act)
            actionComboBox.currentIndexChanged.connect(self.setactioneventbutton)

            #Action Description
            actiondescriptionedit = QLineEdit(self.extraeventsactionstrings[i])
            actiondescriptionedit.editingFinished.connect(self.setactiondescriptioneventbutton)

            #Visibility
            visibilityComboBox =  MyQComboBox()
            visibilityComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            visibilityComboBox.addItems(visibility)
            visibilityComboBox.setCurrentIndex(self.extraeventsvisibility[i])
            visibilityComboBox.currentIndexChanged.connect(self.setvisibilitytyeventbutton)
            #Color
            self.colorButton = QPushButton("Select")
            self.colorButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.colorButton.clicked.connect(self.setbuttoncolor)
            label = self.extraeventslabels[i][:]
            et = self.extraeventstypes[i]
            if 4 < et < 9:
                et = et - 5
            if et < 4:
                label = label.replace("\\t",self.aw.qmc.etypes[et])
            self.colorButton.setText(label)
            self.colorButton.setStyleSheet("background-color: %s; color: %s;"%(self.extraeventbuttoncolor[i],self.extraeventbuttontextcolor[i]))
            #Text Color
            self.colorTextButton = QPushButton("Select")
            self.colorTextButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.colorTextButton.clicked.connect(self.setbuttontextcolor)
            self.colorTextButton.setText(label)
            self.colorTextButton.setStyleSheet("background-color: %s; color: %s;"%(self.extraeventbuttoncolor[i],self.extraeventbuttontextcolor[i]))
            #Empty Cell
            emptyCell = QLabel("")
            #add widgets to the table
            self.eventbuttontable.setCellWidget(i,0,labeledit)
            self.eventbuttontable.setCellWidget(i,1,descriptionedit)
            self.eventbuttontable.setCellWidget(i,2,typeComboBox)
            self.eventbuttontable.setCellWidget(i,3,valueEdit)
            self.eventbuttontable.setCellWidget(i,4,actionComboBox)
            self.eventbuttontable.setCellWidget(i,5,actiondescriptionedit)
            self.eventbuttontable.setCellWidget(i,6,visibilityComboBox)
            self.eventbuttontable.setCellWidget(i,7,self.colorButton)
            self.eventbuttontable.setCellWidget(i,8,self.colorTextButton)
            self.eventbuttontable.setCellWidget(i,9,emptyCell)

        self.eventbuttontable.horizontalHeader().setStretchLastSection(False)
        self.eventbuttontable.resizeColumnsToContents()
        self.eventbuttontable.horizontalHeader().setStretchLastSection(True)
        self.eventbuttontable.setColumnWidth(0,70)
        self.eventbuttontable.setColumnWidth(1,80)
        self.eventbuttontable.setColumnWidth(2,100)
        self.eventbuttontable.setColumnWidth(3,50)
        self.eventbuttontable.setColumnWidth(4,150)
        self.eventbuttontable.setColumnWidth(5,100)
        self.eventbuttontable.setColumnWidth(6,80)
        self.eventbuttontable.setColumnWidth(7,80)
        self.eventbuttontable.setColumnWidth(8,80)


        # remember the columnwidth
        for i in range(len(self.aw.eventbuttontablecolumnwidths)):
            try:
                self.eventbuttontable.setColumnWidth(i,self.aw.eventbuttontablecolumnwidths[i])
            except Exception: # pylint: disable=broad-except
                pass

    @pyqtSlot(bool)
    def copyEventButtonTabletoClipboard(self,_=False):
        nrows = self.eventbuttontable.rowCount() 
        ncols = self.eventbuttontable.columnCount() - 1 #there is a dummy column at the end on the right
        clipboard = ""
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.AltModifier:  #alt click
            tbl = prettytable.PrettyTable()
            fields = []
            fields.append(" ")  # this column shows the row number
            for c in range(ncols):
                fields.append(self.eventbuttontable.horizontalHeaderItem(c).text())
            tbl.field_names = fields
            for r in range(nrows):
                rows = []
                rows.append(str(r+1))
                rows.append(self.eventbuttontable.cellWidget(r,0).text())
                rows.append(self.eventbuttontable.cellWidget(r,1).text())
                rows.append(self.eventbuttontable.cellWidget(r,2).currentText())
                rows.append(self.eventbuttontable.cellWidget(r,3).text())
                rows.append(self.eventbuttontable.cellWidget(r,4).currentText())
                rows.append(self.eventbuttontable.cellWidget(r,5).text())
                rows.append(self.eventbuttontable.cellWidget(r,6).currentText())
                rows.append(self.eventbuttontable.cellWidget(r,7).palette().button().color().name())
                rows.append(self.eventbuttontable.cellWidget(r,8).palette().button().color().name())
                tbl.add_row(rows)
            clipboard = tbl.get_string()
        else:
            clipboard += " " + '\t'  # this column shows the row number
            for c in range(ncols):
                clipboard += self.eventbuttontable.horizontalHeaderItem(c).text()
                if c != (ncols-1):
                    clipboard += '\t'
            clipboard += '\n'
            for r in range(nrows):
                clipboard += str(r+1) + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,0).text() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,1).text() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,2).currentText() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,3).text() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,4).currentText() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,5).text() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,6).currentText() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,7).palette().button().color().name() + '\t'
                clipboard += self.eventbuttontable.cellWidget(r,8).palette().button().color().name() + '\n'
        # copy to the system clipboard
        sys_clip = QApplication.clipboard()
        sys_clip.setText(clipboard)
        self.aw.sendmessage(QApplication.translate("Message","Event Button table copied to clipboard"))


    def savetableextraeventbutton(self):
        maxButton = len(self.extraeventstypes)
        #Clean Lists:
        #Labels
        self.aw.extraeventslabels         = [None] * maxButton
        #Description
        self.aw.extraeventsdescriptions   = [None] * maxButton
        #Types
        self.aw.extraeventstypes          = [None] * maxButton
        #Values
        self.aw.extraeventsvalues         = [None] * maxButton
        #Actions
        self.aw.extraeventsactions        = [None] * maxButton
        #Action Description
        self.aw.extraeventsactionstrings  = [None] * maxButton
        #Visibility
        self.aw.extraeventsvisibility     = [None] * maxButton
        #Color
        self.aw.extraeventbuttoncolor     = [None] * maxButton
        #Text Color
        self.aw.extraeventbuttontextcolor = [None] * maxButton

        #Sorting buttons based on the visualRow
        for i in range(maxButton):
            visualIndex = self.eventbuttontable.visualRow(i)

            #Labels
            self.aw.extraeventslabels[visualIndex]         = self.extraeventslabels[i]
            #Description
            self.aw.extraeventsdescriptions[visualIndex]   = self.extraeventsdescriptions[i]
            #Types
            self.aw.extraeventstypes[visualIndex]          = self.extraeventstypes[i]
            #Values
            self.aw.extraeventsvalues[visualIndex]         = self.extraeventsvalues[i]
            #Actions
            self.aw.extraeventsactions[visualIndex]        = self.extraeventsactions[i]
            #Action Description
            self.aw.extraeventsactionstrings[visualIndex]  = self.extraeventsactionstrings[i]
            #Visibility
            self.aw.extraeventsvisibility[visualIndex]     = self.extraeventsvisibility[i]
            #Color
            self.aw.extraeventbuttoncolor[visualIndex]     = self.extraeventbuttoncolor[i]
            #Text Color
            self.aw.extraeventbuttontextcolor[visualIndex] = self.extraeventbuttontextcolor[i]

        #Apply Event Button Changes
        self.aw.settooltip()
        self.aw.realignbuttons()
        self.aw.update_extraeventbuttons_visibility()

    @pyqtSlot()
    def setlabeleventbutton(self):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),0)
        if i is not None:
            labeledit = self.eventbuttontable.cellWidget(i,0)
            label = labeledit.text()
            label = label.replace("\\n", chr(10))
    
            if i < len(self.extraeventslabels):
                et = self.extraeventstypes[i]
                if 4 < et < 9:
                    et = et - 5
                self.extraeventslabels[i] = label
                if et < 4:
                    label = label[:].replace("\\t",self.aw.qmc.etypes[et])
    
            #Update Color Buttons
            self.eventbuttontable.cellWidget(i,7).setText(label)
            self.eventbuttontable.cellWidget(i,8).setText(label)

    @pyqtSlot()
    def setdescriptioneventbutton(self):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),1)
        if i is not None:
            descriptionedit = self.eventbuttontable.cellWidget(i,1)
            if i < len(self.extraeventsdescriptions):
                self.extraeventsdescriptions[i] = descriptionedit.text()

    @pyqtSlot(int)
    def settypeeventbutton(self,_):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),2)
        if i is not None:
            typecombobox = self.eventbuttontable.cellWidget(i,2)
            evType = typecombobox.currentIndex() - 1 # we remove again the offset of 1 here to jump over the new EVENT entry
            if i < len(self.extraeventstypes):
                if evType == -1:
                    evType = 4 # and map the first entry to 4
                elif evType == 4:
                    evType = 9 # and map the entry 4 to 9
                self.extraeventstypes[i] = evType

            labeledit = self.eventbuttontable.cellWidget(i,0)
            label = labeledit.text()
            label = label.replace("\\n", chr(10))
    
            if i < len(self.extraeventslabels):
                et = self.extraeventstypes[i]
                if 4 < et < 9:
                    et = et - 5
                self.extraeventslabels[i] = label
                if et < 4:
                    label = label[:].replace("\\t",self.aw.qmc.etypes[et])
    
            #Update Color Buttons
            self.eventbuttontable.cellWidget(i,7).setText(label)
            self.eventbuttontable.cellWidget(i,8).setText(label)
    
    @pyqtSlot()
    def setvalueeventbutton(self):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),3)
        if i is not None:
            valueedit = self.eventbuttontable.cellWidget(i,3)
            if i < len(self.extraeventsvalues):
                self.extraeventsvalues[i] = self.aw.qmc.str2eventsvalue(str(valueedit.text()))
    
    @pyqtSlot(int)
    def setactioneventbutton(self,_):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),4)
        if i is not None:
            actioncombobox = self.eventbuttontable.cellWidget(i,4)
            if i < len(self.extraeventsactions):
                self.extraeventsactions[i] = actioncombobox.currentIndex()
                if self.extraeventsactions[i] > 6: # increase action type as 7=CallProgramWithArg is not available for buttons
                    self.extraeventsactions[i] = self.extraeventsactions[i] + 1

    @pyqtSlot()
    def setactiondescriptioneventbutton(self):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),5)
        if i is not None:
            actiondescriptionedit = self.eventbuttontable.cellWidget(i,5)
            if i < len(self.extraeventsactionstrings):
                self.extraeventsactionstrings[i] = actiondescriptionedit.text()

    @pyqtSlot(int)
    def setvisibilitytyeventbutton(self,_):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),6)
        if i is not None:
            actioncombobox = self.eventbuttontable.cellWidget(i,6)
            if i < len(self.extraeventsvisibility):
                self.extraeventsvisibility[i] = actioncombobox.currentIndex()

    @pyqtSlot(bool)
    def setbuttoncolor(self,_):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),7)
        if i is not None and i < len(self.extraeventbuttoncolor):
            colorf = self.aw.colordialog(QColor(self.extraeventbuttoncolor[i]))
            if colorf.isValid():
                self.extraeventbuttoncolor[i] = str(colorf.name())
                textColor = self.extraeventbuttontextcolor[i]
                backColor =  self.extraeventbuttoncolor[i]
                label = self.extraeventslabels[i]
                style = "background-color: %s; color: %s;"%(backColor,textColor)
                self.eventbuttontable.cellWidget(i,7).setStyleSheet(style)
                self.eventbuttontable.cellWidget(i,8).setStyleSheet(style)
                self.aw.checkColors([(QApplication.translate("Label","Event button")+" "+ label, backColor, " "+QApplication.translate("Label","its text"), textColor)])

    @pyqtSlot(bool)
    def setbuttontextcolor(self,_):
        i = self.aw.findWidgetsRow(self.eventbuttontable,self.sender(),8)
        if i is not None and i < len(self.extraeventbuttontextcolor):
            colorf = self.aw.colordialog(QColor(self.extraeventbuttontextcolor[i]))
            if colorf.isValid():
                self.extraeventbuttontextcolor[i] = str(colorf.name())
                textColor = self.extraeventbuttontextcolor[i]
                backColor =  self.extraeventbuttoncolor[i]
                label = self.extraeventslabels[i]
                style = "background-color: %s; color: %s;"%(backColor,textColor)
                self.eventbuttontable.cellWidget(i,7).setStyleSheet(style)
                self.eventbuttontable.cellWidget(i,8).setStyleSheet(style)
                self.aw.checkColors([(QApplication.translate("Label","Event button")+" "+ label, backColor, " "+QApplication.translate("Label","its text"),textColor)])

    def disconnectTableItemActions(self):
        for x in range(self.eventbuttontable.rowCount()):
            try:
                self.eventbuttontable.cellWidget(x,0).editingFinished.disconnect() # label edit
                self.eventbuttontable.cellWidget(x,1).editingFinished.disconnect() # description edit
                self.eventbuttontable.cellWidget(x,2).currentIndexChanged.disconnect() # type combo
                self.eventbuttontable.cellWidget(x,3).editingFinished.disconnect() # value edit
                self.eventbuttontable.cellWidget(x,4).currentIndexChanged.disconnect() # action combo
                self.eventbuttontable.cellWidget(x,5).editingFinished.disconnect() # action description
                self.eventbuttontable.cellWidget(x,6).currentIndexChanged.disconnect() # visibility combo
                self.eventbuttontable.cellWidget(x,7).clicked.disconnect() # color button
                self.eventbuttontable.cellWidget(x,8).clicked.disconnect() # color text button
            except Exception: # pylint: disable=broad-except
                pass

    @pyqtSlot(bool)
    def delextraeventbutton(self,_):
        self.disconnectTableItemActions() # we ensure that signals from to be deleted items are not fired anymore
        bindex = len(self.extraeventstypes)-1
        selected = self.eventbuttontable.selectedRanges()

        if len(selected) > 0:
            bindex = selected[0].topRow()

        if bindex >= 0:
            self.extraeventslabels.pop(bindex)
            self.extraeventsdescriptions.pop(bindex)
            self.extraeventstypes.pop(bindex)
            self.extraeventsvalues.pop(bindex)
            self.extraeventsactions.pop(bindex)
            self.extraeventsactionstrings.pop(bindex)
            self.extraeventsvisibility.pop(bindex)
            self.extraeventbuttoncolor.pop(bindex)
            self.extraeventbuttontextcolor.pop(bindex)

            self.createEventbuttonTable()
            # workaround a table redrawbug in PyQt 5.14.2 on macOS
            if len(self.extraeventstypes) > 1:
                self.repaint()

    @pyqtSlot(bool)
    def addextraeventbuttonSlot(self,_):
        self.insertextraeventbutton()

    @pyqtSlot(bool)
    def insertextraeventbuttonSlot(self,_):
        self.insertextraeventbutton(True)

    def insertextraeventbutton(self,insert=False):
        if len(self.extraeventstypes) >= self.aw.buttonlistmaxlen * 4: # max 4 rows of buttons of buttonlistmaxlen
            return
        try:
            if type(QApplication.focusWidget()) == QLineEdit:
                QApplication.focusWidget().editingFinished.emit()
        except Exception: # pylint: disable=broad-except
            pass

        bindex = len(self.extraeventstypes)
        selected = self.eventbuttontable.selectedRanges()

        # defaults for new entries
        event_description = ""
        event_type = 4
        event_value = 0
        event_action = 0
        event_string = ""
        event_visibility = 1
        event_buttoncolor = "#808080"
        event_textcolor = "white"
        event_label = "E"
        
        if len(selected) > 0:
            selected_idx = selected[0].topRow()
            if insert:
                bindex = selected_idx
            try:
                event_description = self.extraeventsdescriptions[selected_idx]
                event_type = self.extraeventstypes[selected_idx]
                event_value = self.extraeventsvalues[selected_idx]
                event_action = self.extraeventsactions[selected_idx]
                event_string = self.extraeventsactionstrings[selected_idx]
                event_visibility = self.extraeventsvisibility[selected_idx]
                event_buttoncolor = self.extraeventbuttoncolor[selected_idx]
                event_textcolor = self.extraeventbuttontextcolor[selected_idx]
                event_label = self.extraeventslabels[selected_idx]
            except Exception: # pylint: disable=broad-except
                pass

        if bindex >= 0:
            self.extraeventsdescriptions.insert(bindex,event_description)
            self.extraeventstypes.insert(bindex,event_type)
            self.extraeventsvalues.insert(bindex,event_value)
            self.extraeventsactions.insert(bindex,event_action)
            self.extraeventsactionstrings.insert(bindex,event_string)
            self.extraeventsvisibility.insert(bindex,event_visibility)
            self.extraeventbuttoncolor.insert(bindex,event_buttoncolor)
            self.extraeventbuttontextcolor.insert(bindex,event_textcolor)
            self.extraeventslabels.insert(bindex,event_label)

            self.createEventbuttonTable()
            # workaround a table redrawbug in PyQt 5.14.2 on macOS
            if len(self.extraeventstypes) > 1:
                self.repaint()

    @pyqtSlot(int)
    def eventsbuttonflagChanged(self,_):
        if self.eventsbuttonflag.isChecked():
            self.aw.buttonEVENT.setVisible(True)
            self.aw.eventsbuttonflag = 1
        else:
            self.aw.buttonEVENT.setVisible(False)
            self.aw.eventsbuttonflag = 0

    @pyqtSlot(int)
    def eventsclampflagChanged(self,_):
        if self.eventsclampflag.isChecked():
            self.aw.qmc.clampEvents = True
        else:
            self.aw.qmc.clampEvents = False
        self.aw.qmc.redraw(recomputeAllDeltas=False)

    @pyqtSlot(int)
    def eventslabelsflagChanged(self,_):
        if self.eventslabelsflag.isChecked():
            self.aw.qmc.renderEventsDescr = True
        else:
            self.aw.qmc.renderEventsDescr = False
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        
    @pyqtSlot(int)
    def annotationsflagChanged(self,_):
        if self.annotationsflagbox.isChecked():
            self.aw.qmc.annotationsflag = 1
        else:
            self.aw.qmc.annotationsflag = 0
            # we clear the custom annotation positions on deactivation
            self.aw.qmc.l_annotations_dict = {}
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        
    @pyqtSlot(int)
    def showeventsonbtChanged(self,_):  
        if self.showeventsonbtbox.isChecked():
            self.aw.qmc.showeventsonbt = True
        else:
            self.aw.qmc.showeventsonbt = False
        self.aw.qmc.l_event_flags_dict = {} # clear the custom event flag position cache
        self.aw.qmc.redraw(recomputeAllDeltas=False)
    
    @pyqtSlot(int)
    def changeShowEtypes0(self,_):
        self.changeShowEtypes(0)
    @pyqtSlot(int)
    def changeShowEtypes1(self,_):
        self.changeShowEtypes(1)
    @pyqtSlot(int)
    def changeShowEtypes2(self,_):
        self.changeShowEtypes(2)
    @pyqtSlot(int)
    def changeShowEtypes3(self,_):
        self.changeShowEtypes(3)
    @pyqtSlot(int)
    def changeShowEtypes4(self,_):
        self.changeShowEtypes(4)
    
    def changeShowEtypes(self,etype):
        self.aw.qmc.showEtypes[etype] = not self.aw.qmc.showEtypes[etype]
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        
    @pyqtSlot(int)
    def minieventsflagChanged(self,_):
        if self.minieventsflag.isChecked():
            self.aw.minieventsflag = 1
        else:
            self.aw.minieventsflag = 0
        if self.aw.qmc.flagon:
            self.aw.update_minieventline_visibility()

    @pyqtSlot(int)
    def eventsGraphTypeflagChanged(self,_):
        self.aw.qmc.eventsGraphflag = self.bartypeComboBox.currentIndex() - 1
        if self.aw.qmc.eventsGraphflag > 1:
            self.eventsclampflag.setEnabled(True)
        else:
            self.eventsclampflag.setEnabled(False)
        if self.aw.qmc.eventsGraphflag == -1:
            # we clear the custom annotation positions on deactivation
            self.aw.qmc.l_event_flags_dict = {}
            self.aw.qmc.eventsGraphflag = 0
            self.aw.qmc.eventsshowflag = 0
        else:
            self.aw.qmc.eventsshowflag = 1
        self.aw.qmc.redraw(recomputeAllDeltas=False)

    def saveSliderSettings(self):
        self.aw.eventslidervisibilities[0] = int(self.E1visibility.isChecked())
        self.aw.eventslidervisibilities[1] = int(self.E2visibility.isChecked())
        self.aw.eventslidervisibilities[2] = int(self.E3visibility.isChecked())
        self.aw.eventslidervisibilities[3] = int(self.E4visibility.isChecked())
        self.aw.eventslideractions[0] = int(self.E1action.currentIndex())
        self.aw.eventslideractions[1] = int(self.E2action.currentIndex())
        self.aw.eventslideractions[2] = int(self.E3action.currentIndex())
        self.aw.eventslideractions[3] = int(self.E4action.currentIndex())
        self.aw.eventslidercommands[0] = self.E1command.text()
        self.aw.eventslidercommands[1] = self.E2command.text()
        self.aw.eventslidercommands[2] = self.E3command.text()
        self.aw.eventslidercommands[3] = self.E4command.text()
        self.aw.eventslideroffsets[0] = int(self.E1offset.value())
        self.aw.eventslideroffsets[1] = int(self.E2offset.value())
        self.aw.eventslideroffsets[2] = int(self.E3offset.value())
        self.aw.eventslideroffsets[3] = int(self.E4offset.value())
        self.aw.eventsliderfactors[0] = float(self.E1factor.value())
        if self.aw.eventsliderfactors[0] == 0: # a zero does not make much sense and might be a user error
            self.aw.eventsliderfactors[0] = 1.0
        self.aw.eventsliderfactors[1] = float(self.E2factor.value())
        if self.aw.eventsliderfactors[1] == 1: # a zero does not make much sense and might be a user error
            self.aw.eventsliderfactors[1] = 1.0
        self.aw.eventsliderfactors[2] = float(self.E3factor.value())
        if self.aw.eventsliderfactors[2] == 1: # a zero does not make much sense and might be a user error
            self.aw.eventsliderfactors[2] = 1.0
        self.aw.eventsliderfactors[3] = float(self.E4factor.value())
        if self.aw.eventsliderfactors[3] == 1: # a zero does not make much sense and might be a user error
            self.aw.eventsliderfactors[3] = 1.0
        self.aw.eventslidermin[0] = int(min(self.E1_min.value(),self.E1_max.value()))
        self.aw.eventslidermin[1] = int(min(self.E2_min.value(),self.E2_max.value()))
        self.aw.eventslidermin[2] = int(min(self.E3_min.value(),self.E3_max.value()))
        self.aw.eventslidermin[3] = int(min(self.E4_min.value(),self.E4_max.value()))
        self.aw.eventslidermax[0] = int(max(self.E1_min.value(),self.E1_max.value()))
        self.aw.eventslidermax[1] = int(max(self.E2_min.value(),self.E2_max.value()))
        self.aw.eventslidermax[2] = int(max(self.E3_min.value(),self.E3_max.value()))
        self.aw.eventslidermax[3] = int(max(self.E4_min.value(),self.E4_max.value()))
        self.aw.eventsliderBernoulli[0] = int(self.E1slider_bernoulli.isChecked())
        self.aw.eventsliderBernoulli[1] = int(self.E2slider_bernoulli.isChecked())
        self.aw.eventsliderBernoulli[2] = int(self.E3slider_bernoulli.isChecked())
        self.aw.eventsliderBernoulli[3] = int(self.E4slider_bernoulli.isChecked())
        self.aw.eventslidercoarse[0] = int(self.E1slider_coarse.isChecked())
        self.aw.eventslidercoarse[1] = int(self.E2slider_coarse.isChecked())
        self.aw.eventslidercoarse[2] = int(self.E3slider_coarse.isChecked())
        self.aw.eventslidercoarse[3] = int(self.E4slider_coarse.isChecked())
        self.aw.eventslidertemp[0] = int(self.E1slider_temp.isChecked())
        self.aw.eventslidertemp[1] = int(self.E2slider_temp.isChecked())
        self.aw.eventslidertemp[2] = int(self.E3slider_temp.isChecked())
        self.aw.eventslidertemp[3] = int(self.E4slider_temp.isChecked())
        self.aw.eventsliderunits[0] = self.E1unit.text()
        self.aw.eventsliderunits[1] = self.E2unit.text()
        self.aw.eventsliderunits[2] = self.E3unit.text()
        self.aw.eventsliderunits[3] = self.E4unit.text()
        self.aw.updateSliderMinMax()
        self.aw.slidersAction.setEnabled(any(self.aw.eventslidervisibilities) or self.aw.pidcontrol.svSlider)

    def saveQuantifierSettings(self):
        self.aw.clusterEventsFlag = bool(self.clusterEventsFlag.isChecked())
        self.aw.eventquantifieractive[0] = int(self.E1active.isChecked())
        self.aw.eventquantifieractive[1] = int(self.E2active.isChecked())
        self.aw.eventquantifieractive[2] = int(self.E3active.isChecked())
        self.aw.eventquantifieractive[3] = int(self.E4active.isChecked())
        self.aw.eventquantifiercoarse[0] = int(self.E1coarse.isChecked())
        self.aw.eventquantifiercoarse[1] = int(self.E2coarse.isChecked())
        self.aw.eventquantifiercoarse[2] = int(self.E3coarse.isChecked())
        self.aw.eventquantifiercoarse[3] = int(self.E4coarse.isChecked())
        self.aw.eventquantifieraction[0] = int(self.E1quantifieraction.isChecked())
        self.aw.eventquantifieraction[1] = int(self.E2quantifieraction.isChecked())
        self.aw.eventquantifieraction[2] = int(self.E3quantifieraction.isChecked())
        self.aw.eventquantifieraction[3] = int(self.E4quantifieraction.isChecked())
        self.aw.eventquantifierSV[0] = int(self.E1quantifierSV.isChecked())
        self.aw.eventquantifierSV[1] = int(self.E2quantifierSV.isChecked())
        self.aw.eventquantifierSV[2] = int(self.E3quantifierSV.isChecked())
        self.aw.eventquantifierSV[3] = int(self.E4quantifierSV.isChecked())
        self.aw.eventquantifiersource[0] = int(self.E1SourceComboBox.currentIndex())
        self.aw.eventquantifiersource[1] = int(self.E2SourceComboBox.currentIndex())
        self.aw.eventquantifiersource[2] = int(self.E3SourceComboBox.currentIndex())
        self.aw.eventquantifiersource[3] = int(self.E4SourceComboBox.currentIndex())
        self.aw.eventquantifiermin[0] = int(self.E1min.value())
        self.aw.eventquantifiermin[1] = int(self.E2min.value())
        self.aw.eventquantifiermin[2] = int(self.E3min.value())
        self.aw.eventquantifiermin[3] = int(self.E4min.value())
        self.aw.eventquantifiermax[0] = int(self.E1max.value())
        self.aw.eventquantifiermax[1] = int(self.E2max.value())
        self.aw.eventquantifiermax[2] = int(self.E3max.value())
        self.aw.eventquantifiermax[3] = int(self.E4max.value())
        self.aw.computeLinespaces()

    def saveAnnotationsSettings(self):
        checkedvisibilities = [0,0,0,0]
        #the following line does not work
        #checkedvisibilities = [int(self.E1AnnoVisibility.isChecked()),int(self.E3AnnoVisibility.isChecked()),int(self.E3AnnoVisibility.isChecked()),int(self.E4AnnoVisibility.isChecked())]
        checkedvisibilities[0] = int(self.E1AnnoVisibility.isChecked())
        checkedvisibilities[1] = int(self.E2Annovisibility.isChecked())
        checkedvisibilities[2] = int(self.E3Annovisibility.isChecked())
        checkedvisibilities[3] = int(self.E4Annovisibility.isChecked())
        if self.aw.qmc.specialeventannovisibilities == checkedvisibilities:
            redraw = False
        else:
            redraw = True
        self.aw.qmc.specialeventannovisibilities[0] = int(self.E1AnnoVisibility.isChecked())
        self.aw.qmc.specialeventannovisibilities[1] = int(self.E2Annovisibility.isChecked())
        self.aw.qmc.specialeventannovisibilities[2] = int(self.E3Annovisibility.isChecked())
        self.aw.qmc.specialeventannovisibilities[3] = int(self.E4Annovisibility.isChecked())
        if redraw:
            self.aw.qmc.redraw(recomputeAllDeltas=False)
    
    #the inverse to restoreState
    def storeState(self):
        # event configurations
        self.eventsbuttonflagstored = self.aw.eventsbuttonflag
        self.eventsshowflagstored = self.aw.qmc.eventsshowflag
        self.annotationsflagstored = self.aw.qmc.annotationsflag
        self.showeventsonbtstored = self.aw.qmc.showeventsonbt
        self.showEtypesstored = self.aw.qmc.showEtypes[:]
        self.minieventsflagstored = self.aw.minieventsflag
        self.eventsGraphflagstored = self.aw.qmc.eventsGraphflag
        self.etypesstored = self.aw.qmc.etypes
        self.etypeComboBoxstored = self.aw.etypeComboBox
        self.autoChargeFlagstored = self.aw.qmc.autoChargeFlag
        self.autoDropFlagstored = self.aw.qmc.autoDropFlag
        self.markTPFlagstored = self.aw.qmc.markTPflag
        # buttons
        self.extraeventslabels = self.aw.extraeventslabels[:]
        self.extraeventsdescriptions = self.aw.extraeventsdescriptions[:]
        self.extraeventstypes = self.aw.extraeventstypes[:]
        self.extraeventsvalues = self.aw.extraeventsvalues[:]
        self.extraeventsactions = self.aw.extraeventsactions[:]
        self.extraeventsactionstrings = self.aw.extraeventsactionstrings[:]
        self.extraeventsvisibility = self.aw.extraeventsvisibility[:]
        self.extraeventbuttoncolor = self.aw.extraeventbuttoncolor[:]
        self.extraeventbuttontextcolor = self.aw.extraeventbuttontextcolor[:]
        self.buttonlistmaxlen = self.aw.buttonlistmaxlen
        # sliders
        self.eventslidervisibilities = self.aw.eventslidervisibilities[:]
        self.eventslideractions = self.aw.eventslideractions[:]
        self.eventslidercommands = self.aw.eventslidercommands[:]
        self.eventslideroffsets = self.aw.eventslideroffsets[:]
        self.eventsliderfactors = self.aw.eventsliderfactors[:]
        self.eventslidermin = self.aw.eventslidermin[:]
        self.eventslidermax = self.aw.eventslidermax[:]
        self.eventsliderBernoulli = self.aw.eventsliderBernoulli[:]
        self.eventslidercoarse = self.aw.eventslidercoarse[:]
        self.eventslidertemp = self.aw.eventslidertemp[:]
        self.eventsliderunits = self.aw.eventsliderunits[:]
        # quantifiers
        self.eventquantifieractive = self.aw.eventquantifieractive[:]
        self.eventquantifiersource = self.aw.eventquantifiersource[:]
        self.eventquantifiermin = self.aw.eventquantifiermin[:]
        self.eventquantifiermax = self.aw.eventquantifiermax[:]
        self.eventquantifiercoarse = self.aw.eventquantifiercoarse[:]
        self.eventquantifieraction = self.aw.eventquantifieraction[:]
        self.eventquantifierSV = self.aw.eventquantifierSV[:]
        # palettes
        self.buttonpalette = self.aw.buttonpalette[:]
        self.buttonpalettemaxlen = self.aw.buttonpalettemaxlen
        self.buttonpalette_label = self.aw.buttonpalette_label
        # styles
        self.EvalueColor = self.aw.qmc.EvalueColor[:]
        self.EvalueMarker = self.aw.qmc.EvalueMarker[:]
        self.Evaluelinethickness = self.aw.qmc.Evaluelinethickness[:]
        self.Evaluealpha = self.aw.qmc.Evaluealpha[:]
        self.EvalueMarkerSize = self.aw.qmc.EvalueMarkerSize[:]
        # event annotations
        self.specialeventannovisibilities = self.aw.qmc.specialeventannovisibilities[:]
        self.specialeventannotations = self.aw.qmc.specialeventannotations[:]

    #called from Cancel button
    @pyqtSlot()
    def restoreState(self):
        # event configurations
        self.aw.eventsbuttonflag = self.eventsbuttonflagstored
        self.aw.qmc.eventsshowflag = self.eventsshowflagstored
        self.aw.qmc.annotationsflag = self.annotationsflagstored
        self.aw.qmc.showeventsonbt = self.showeventsonbtstored
        self.aw.qmc.showEtypes = self.showEtypesstored[:]
        self.aw.minieventsflag = self.minieventsflagstored
        self.aw.qmc.eventsGraphflag = self.eventsGraphflagstored
        self.aw.qmc.etypes = self.etypesstored
        self.aw.etypeComboBox = self.etypeComboBoxstored
        self.aw.qmc.autoChargeFlag = self.autoChargeFlagstored
        self.aw.qmc.autoDropFlag = self.autoDropFlagstored
        self.aw.qmc.markTPflag = self.markTPFlagstored
        # buttons saved only if ok is pressed, so no restore needed
        self.aw.buttonlistmaxlen = self.buttonlistmaxlen
        # sliders
        self.aw.eventslidervisibilities = self.eventslidervisibilities
        self.aw.eventslideractions = self.eventslideractions
        self.aw.eventslidercommands = self.eventslidercommands
        self.aw.eventslideroffsets = self.eventslideroffsets
        self.aw.eventsliderfactors = self.eventsliderfactors
        self.aw.eventslidermin = self.eventslidermin
        self.aw.eventslidermax = self.eventslidermax
        self.aw.eventsliderBernoulli = self.eventsliderBernoulli
        self.aw.eventslidercoarse = self.eventslidercoarse
        self.aw.eventslidertemp = self.eventslidertemp
        self.aw.eventsliderunits = self.eventsliderunits
        # quantifiers
        self.aw.eventquantifieractive = self.eventquantifieractive
        self.aw.eventquantifiersource = self.eventquantifiersource
        self.aw.eventquantifiermin = self.eventquantifiermin
        self.aw.eventquantifiermax = self.eventquantifiermax
        self.aw.eventquantifiercoarse = self.eventquantifiercoarse
        self.aw.eventquantifieraction = self.eventquantifieraction
        # palettes
        self.aw.buttonpalette = self.buttonpalette
        self.aw.buttonpalettemaxlen = self.buttonpalettemaxlen
        self.aw.buttonpalette_label = self.buttonpalette_label
        # styles
        self.aw.qmc.EvalueColor = self.EvalueColor
        self.aw.qmc.EvalueMarker = self.EvalueMarker
        self.aw.qmc.Evaluelinethickness = self.Evaluelinethickness
        self.aw.qmc.Evaluealpha = self.Evaluealpha
        self.aw.qmc.EvalueMarkerSize = self.EvalueMarkerSize
        # event annotations
        self.aw.qmc.specialeventannovisibilities = self.specialeventannovisibilities[:]
        self.aw.qmc.specialeventannotations = self.specialeventannotations[:]
        self.close()

    #called from OK button
    @pyqtSlot()
    def updatetypes(self):
        try:
            self.closeHelp()
            self.aw.buttonsize = self.nbuttonsSizeBox.currentIndex()
            self.aw.buttonpalette_label = self.transferpalettecurrentLabelEdit.text()
            self.savetableextraeventbutton()
            # save column widths
            self.aw.eventbuttontablecolumnwidths = [self.eventbuttontable.columnWidth(c) for c in range(self.eventbuttontable.columnCount())]
            #save default buttons
            self.aw.qmc.buttonvisibility[0] = self.CHARGEbutton.isChecked()
            self.aw.buttonCHARGE.setVisible(bool(self.aw.qmc.buttonvisibility[0]))
            self.aw.qmc.buttonvisibility[1] = self.DRYbutton.isChecked()
            self.aw.buttonDRY.setVisible(bool(self.aw.qmc.buttonvisibility[1]))
            self.aw.qmc.buttonvisibility[2] = self.FCSbutton.isChecked()
            self.aw.buttonFCs.setVisible(bool(self.aw.qmc.buttonvisibility[2]))
            self.aw.qmc.buttonvisibility[3] = self.FCEbutton.isChecked()
            self.aw.buttonFCe.setVisible(bool(self.aw.qmc.buttonvisibility[3]))
            self.aw.qmc.buttonvisibility[4] = self.SCSbutton.isChecked()
            self.aw.buttonSCs.setVisible(bool(self.aw.qmc.buttonvisibility[4]))
            self.aw.qmc.buttonvisibility[5] = self.SCEbutton.isChecked()
            self.aw.buttonSCe.setVisible(bool(self.aw.qmc.buttonvisibility[5]))
            self.aw.qmc.buttonvisibility[6] = self.DROPbutton.isChecked()
            self.aw.buttonDROP.setVisible(bool(self.aw.qmc.buttonvisibility[6]))
            self.aw.qmc.buttonvisibility[7] = self.COOLbutton.isChecked()
            self.aw.buttonCOOL.setVisible(bool(self.aw.qmc.buttonvisibility[7]))
            #save sliders   
            self.saveSliderSettings()
            self.saveQuantifierSettings()
            # save palette label
            self.aw.buttonpalette_label = self.transferpalettecurrentLabelEdit.text()
            #
            self.aw.qmc.buttonactions[0] = self.CHARGEbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[1] = self.DRYbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[2] = self.FCSbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[3] = self.FCEbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[4] = self.SCSbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[5] = self.SCEbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[6] = self.DROPbuttonActionType.currentIndex()
            self.aw.qmc.buttonactions[7] = self.COOLbuttonActionType.currentIndex()
            self.aw.qmc.extrabuttonactions[0] = self.ONbuttonActionType.currentIndex()
            self.aw.qmc.extrabuttonactions[1] = self.OFFbuttonActionType.currentIndex()
            self.aw.qmc.extrabuttonactions[2] = self.SAMPLINGbuttonActionType.currentIndex()
            self.aw.qmc.xextrabuttonactions[0] = self.RESETbuttonActionType.currentIndex()
            self.aw.qmc.xextrabuttonactions[1] = self.STARTbuttonActionType.currentIndex()
            self.aw.qmc.buttonactionstrings[0] = self.CHARGEbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[1] = self.DRYbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[2] = self.FCSbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[3] = self.FCEbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[4] = self.SCSbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[5] = self.SCEbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[6] = self.DROPbuttonActionString.text()
            self.aw.qmc.buttonactionstrings[7] = self.COOLbuttonActionString.text()
            self.aw.qmc.extrabuttonactionstrings[0] = self.ONbuttonActionString.text()
            self.aw.qmc.extrabuttonactionstrings[1] = self.OFFbuttonActionString.text()
            self.aw.qmc.extrabuttonactionstrings[2] = self.SAMPLINGbuttonActionString.text()
            try:
                self.aw.qmc.extra_event_sampling_delay = self.sampling_delays[self.SAMPLINGbuttonActionInterval.currentIndex()]
            except Exception: # pylint: disable=broad-except
                pass
            self.aw.qmc.xextrabuttonactionstrings[0] = self.RESETbuttonActionString.text()
            self.aw.qmc.xextrabuttonactionstrings[1] = self.STARTbuttonActionString.text()
            
            self.aw.qmc.eventslabelschars = self.eventslabelscharsSpinner.value()
            
            self.aw.qmc.overlappct = int(self.overlapEdit.value())
            
            self.aw.buttonpalette_shortcuts = self.switchPaletteByNumberKey.isChecked()
            #save etypes
            if len(self.etype0.text()) and len(self.etype1.text()) and len(self.etype2.text()) and len(self.etype3.text()):
                self.aw.qmc.etypes[0] = self.etype0.text()
                self.aw.qmc.etypes[1] = self.etype1.text()
                self.aw.qmc.etypes[2] = self.etype2.text()
                self.aw.qmc.etypes[3] = self.etype3.text()
                colorPairsToCheck = []
                for i in range(len(self.aw.qmc.EvalueColor)):
                    colorPairsToCheck.append(
                        (self.aw.qmc.etypes[i] + " Event", self.aw.qmc.EvalueColor[i], 'Background', self.aw.qmc.palette['background']),
                    )
                    colorPairsToCheck.append(
                        (self.aw.qmc.etypes[i] + " Text", self.aw.qmc.EvalueTextColor[i], self.aw.qmc.etypes[i] + " Event", self.aw.qmc.EvalueColor[i]),
                    )
                self.aw.checkColors(colorPairsToCheck)
                # update minieditor event type ComboBox
                self.aw.etypeComboBox.clear()
                self.aw.etypeComboBox.addItems(self.aw.qmc.etypes)
                #update mini editor
                self.aw.etypeComboBox.clear()
                self.aw.etypeComboBox.addItems(self.aw.qmc.etypes)
                #update autoCharge/Drop flag
                self.aw.qmc.autoChargeFlag = self.autoCharge.isChecked()
                self.aw.qmc.autoDropFlag = self.autoDrop.isChecked()
                self.aw.qmc.markTPflag = self.markTP.isChecked()
                #save quantifiers
                self.aw.updateSlidersProperties() # set visibility and event names on slider widgets
# we don't do that anymore!
#                # we save the current button and slider definitions to palette 0
#                self.transferbuttonsto(0)

                self.aw.qmc.redraw(recomputeAllDeltas=False)
                self.aw.sendmessage(QApplication.translate("Message","Event configuration saved"))
                self.close()
            else:
                self.aw.sendmessage(QApplication.translate("Message","Found empty event type box"))
                #save quantifiers
                self.aw.updateSlidersProperties() # set visibility and event names on slider widgets
            #save special event annotations
            self.saveAnnotationsSettings()
            self.aw.closeEventSettings()
        except Exception as e: # pylint: disable=broad-except
            #import traceback
            #traceback.print_exc(file=sys.stdout)
            _, _, exc_tb = sys.exc_info()
            self.aw.qmc.adderror((QApplication.translate("Error Message", "Exception:") + " updatetypes(): {0}").format(str(e)),getattr(exc_tb, 'tb_lineno', '?'))

    def closeEvent(self,_):
        self.closeHelp()
        settings = QSettings()
        #save window geometry
        settings.setValue("EventsGeometry",self.saveGeometry())
        self.aw.EventsDlg_activeTab = self.TabWidget.currentIndex()

    @pyqtSlot(bool)
    def showEventbuttonhelp(self,_=False):
        self.helpdialog = self.aw.showHelpDialog(
                self,            # this dialog as parent
                self.helpdialog, # the existing help dialog
                QApplication.translate("Form Caption","Event Custom Buttons Help"),
                eventbuttons_help.content())

    @pyqtSlot(bool)
    def showSliderHelp(self,_=False):
        self.helpdialog = self.aw.showHelpDialog(
                self,            # this dialog as parent
                self.helpdialog, # the existing help dialog
                QApplication.translate("Form Caption","Event Custom Sliders Help"),
                eventsliders_help.content())

    @pyqtSlot(bool)
    def showEventannotationhelp(self,_=False):
        self.helpdialog = self.aw.showHelpDialog(
                self,            # this dialog as parent
                self.helpdialog, # the existing help dialog
                QApplication.translate("Form Caption","Event Annotations Help"),
                eventannotations_help.content())

    def closeHelp(self):
        self.aw.closeHelpDialog(self.helpdialog)

#########################################################################
#############  CUSTOM EVENT DIALOG ######################################
#########################################################################

class customEventDlg(ArtisanDialog):
    def __init__(self, parent = None, aw = None, time_idx=0,description="",event_type=4,value=0):
        super().__init__(parent, aw)
        if time_idx != 0:
            event_time = self.aw.qmc.timex[time_idx]
            if self.aw.qmc.timeindex[0] > -1:
                event_time -= self.aw.qmc.timex[self.aw.qmc.timeindex[0]]
            event_time_str = " @ " + self.aw.eventtime2string(event_time)
        else:
            event_time_str = ""
        self.setWindowTitle(QApplication.translate("Form Caption","Event") + event_time_str)
        self.description = description
        self.type = event_type
        self.value = self.aw.qmc.eventsvalues(value)

        # connect the ArtisanDialog standard OK/Cancel buttons
        self.dialogbuttons.accepted.connect(self.accept)
        self.dialogbuttons.rejected.connect(self.reject)
        
        descriptionLabel = QLabel(QApplication.translate("Table", "Description"))
        self.descriptionEdit = QLineEdit(self.description)
        typeLabel = QLabel(QApplication.translate("Table", "Type"))
        etypes = self.aw.qmc.getetypes()
        self.typeCombo = MyQComboBox()
        self.typeCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.typeCombo.addItems(etypes)
        self.typeCombo.setCurrentIndex(self.type)
        valueLabel = QLabel(QApplication.translate("Table", "Value"))
        self.valueEdit = QLineEdit(str(self.value))
        
        grid = QGridLayout()
        grid.addWidget(descriptionLabel,0,0)
        grid.addWidget(self.descriptionEdit,0,1)
        grid.addWidget(typeLabel,1,0)
        grid.addWidget(self.typeCombo,1,1)
        grid.addWidget(valueLabel,2,0)
        grid.addWidget(self.valueEdit,2,1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.dialogbuttons)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addStretch()
        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)
        
    def accept(self):
        self.description = self.descriptionEdit.text()
        evalue = self.valueEdit.text()
        self.value = self.aw.qmc.str2eventsvalue(str(evalue))
        self.type = self.typeCombo.currentIndex()
        super().accept()