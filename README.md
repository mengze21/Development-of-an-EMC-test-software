# Further development of an EMC testing software
This project is for the Research paper from Institute for Power Transmission and High Voltage Technology (Institut für Energieübertragung und Hochspannungstechnik, [IEH](https://www.ieh.uni-stuttgart.de/)), [Universtity of Stuttgart](https://www.uni-stuttgart.de/), Germany.

Electromagnetic Compatibility (EMC) = Elektromagnetische Vertäglichkeit (EMV)

The tasks of this project include:

- Creation of drivers for the measurement devices for EMC testing in IEH laboratory.
- Solving the communication problems between devices and the developed software. 
- Creation of automatic program sequences based on standardized tests.
- Creation of a user-friendly graphical user interface (GUI) for the software.


## Screenshots of the software
**`Start window.`**
![Start Window](https://github.com/YunheWolke/Development-of-an-EMC-test-software/blob/main/gui/image_materials/1.png)

**`Main window under the "Feldgebundene Emissionsmessung" testing mode.`**
![Main Window (Under the "Feldgebundene Emissionsmessung" test mode)](https://github.com/YunheWolke/Development-of-an-EMC-test-software/blob/main/gui/image_materials/4.png)

**`Main window under the "Leitungsgebundene Emissionsmessung" testing mode.`**
![Main Window (Under the "Leitungsgebundene Emissionsmessung" test mode)](https://github.com/laura-bar/Weiterentwicklung-einer-EMV-Pruefsoftware/blob/main/Development%20of%20an%20EMC%20test%20software/gui/image_materials/Hauptfenster%20LE.png)

**`Main window under the "Leitungsgebundene Störfestigkeitsprüfung" testing mode.`**
![Main Window (Under the "Leitungsgebundene Störfestigkeitsprüfung" test mode)](https://github.com/laura-bar/Weiterentwicklung-einer-EMV-Pruefsoftware/blob/main/Development%20of%20an%20EMC%20test%20software/gui/image_materials/Hauptfenster%20LS.png)

**`Test window for visualizing the measurment results in real-time under the "Feldgebundene Emissionsmessung".`**
![Test window](https://github.com/YunheWolke/Development-of-an-EMC-test-software/blob/main/gui/image_materials/16.png)

**`Test window for visualizing the measurment results in real-time under the "Leitungsgebundene Emissionsmessung" .`**
![Test window](https://github.com/laura-bar/Weiterentwicklung-einer-EMV-Pruefsoftware/blob/main/Development%20of%20an%20EMC%20test%20software/gui/image_materials/Testfenster%20LE.png)

**`Test window for visualizing the measurment results in real-time under the "Leitungsgebundene Störfestigkeitsprüfung".`**
![Test window](https://github.com/laura-bar/Weiterentwicklung-einer-EMV-Pruefsoftware/blob/main/Development%20of%20an%20EMC%20test%20software/gui/image_materials/Testfenster%20LS.png)

More screenshots see **[here](https://github.com/laura-bar/Weiterentwicklung-einer-EMV-Pruefsoftware/tree/main/Development%20of%20an%20EMC%20test%20software/gui/image_materials)**.

## Requirements
Operating system:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Windows 10\
IDE:&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;PyCharm Community Edition 2019.2.4\
Python:&ensp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Anaconda Python 3.6.10

The **necessary python packages** are:


|                |        |                                      |
|----------------|--------|--------------------------------------|
| PyQt5          | 5.15.2 | Creation of GUI.                     |
| PyQtChart      | 5.15.2 | Creation of interactive diagramms.   |
| OpenCV         | 4.2    | Preprocessing of icons.              |
| qimage2ndarray | 1.8.3  | Transform QImage into Numpy Array.   |
| python-docx    | 0.8.10 | Used to generate report in MS Word.  |
| pypdf2         | 1.26.0 | Used to generate report in PDF file. |
| openpyxl       | 3.0.6  | Used to generate report in MS Excel. |
| pyvisa         | 1.11.3 | Used to control measurement devices. |

```
conda create -n emc_gui python=3.6.10
conda activate emc_gui
pip install PyQt5==5.15.2
pip install PyQtChart==5.15.2
pip install opencv-python
pip install qimage2ndarray==1.8.3
pip install python-docx==0.8.10
pip install PyPDF2==1.26.0
pip install openpyxl==3.0.6
pip install pyvisa==1.11.3
```
In addition, a software called **Qt Designer** is used. Detailed information and download link of this software can be found **[here](https://build-system.fman.io/qt-designer-download)**. 

## Design of GUI

The design of this GUI was inspired by **[emcware](https://www.arworld.us/html/IRC_software.asp)**, which is a testing software that automates Electromagnetic Compatibility (EMC) testing and report generation.

All the icons used in this GUI came from the open source icon library **[ICONS8](https://icons8.com/license)**.

## Structure of the repository
- `gui/`  - All files in this folder are for the GUI and connection programm between GUI and controlling programm.
    - `data/`  - Antenne factors and cabledampfungs are stored in this folder.
    - `icon_materials/`  - Icons are stored in this folder.
    - `image_materials/` - Screenshots of the GUI and a testing result.
    - `uifiles/`  - .ui files generated by Qt Designer.
    - `implement.py`  - Run this .py file to open the software.
    - `MainWindow.py`  - Code of the MainWindow for the GUI.
    - `ManagementderAusrustung_FE.py`  - This .py file is for generating a window for equipment settings for 'Feldgebundene Emissionsmessung'.
    - `ManagementderAusrustung_FE.py`  - This .py file is for generating a window for equipment settings for 'Leitungsgebundene Emissionsmessung'.
    - `ManagementderAusrustung_FE.py`  - This .py file is for generating a window for equipment settings for 'Leitungsgebundene Störfestigkeitsprüfung'.
    - `ReportWindow.py`  - This .py file works as setting window for generation of the final testing report.
    - `TestWindow_FE.py`  - The measurement results are visualized for 'Feldgebundene Emissionsmessung' in this window. Users can also interact with the visualized results. 
    - `TestWindow_LE.py`  - The measurement results are visualized for 'Leitungsgebundene Emissionsmessung' in this window. Users can also interact with the visualized results. 
    - `TestWindow_LS.py`  - The measurement results are visualized for 'Leitungsgebundene Störfestigkeitsprüfung' in this window. Users can also interact with the visualized results. 
    - `thread_FE.py`  - This .py file is the controlling programm for the measurment devices for 'FE'.
    - `thread_LE.py`  - This .py file is the controlling programm for the measurment devices for 'LE'.
    - `thread_LS.py`  - This .py file is the controlling programm for the measurment devices for 'LS'.
    - `Versuchsaufbau.py`  - This .py file is for the window of testing setup.
    - `WordReportGenerator.py`  -  This py. file includes the functional codes for generating the final measurement report in word. (Report template in MS Word.)
- `other control code and data read code/` - Here are the code for controlling the measurement devices and reading and drawing the measurements.


## How to use?

```
python3 -m gui.implement
```
