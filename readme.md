# NFC Registrator
By: Luuk Leeuwenstein

## Goal
This small Python command prompt application for Windows will allow you to use ACR122U USB NFC Scanners to set-up a registration or clock-in system, based on a premade object or entrant csv list. Ensure that the NFC tags used are compatible with this scanner. 

Made for Anthony Veder Rederijzaken B.V.

## Requirements
### Package
* Python 2.7 (Required for NFCpy)
* [NFCpy 0.13.2](https://nfcpy.readthedocs.io/en/latest/)

### Running
To run the app, you will need to replace the built in driver for the USB NFC reader with a more generic winUSB driver. You could use a tool like [Zadig](http://zadig.akeo.ie/) for this step. 

Additionally, for generating an executable [libusb-win32](https://sourceforge.net/projects/libusb-win32/) is required. Place the `libusb1.0.dll` file in the root folder of the application. 

#### How to use
Before you can use the tool, ensure that you have created a list of registration objects (such as persons) and scanned their NFC tags in advance to gain a unique 8 character identifier. 

Ensure that a folder named `Lists/` is present in the root folder. In this folder, place a `master.csv` file that containts at least a `RegCode` column (for the identifiers) and a `check` column.   

Running the tool will guide you through a number of options untill the system is set to a `listening` state. When a tag is scanned, the input is compared to the `RegCode` column in `master.csv` and 'Yes' is entered into the `check` column of the newly created `master_temp.csv`. 

Currently, stopping the listening process require scanning certain specific hard coded tag identifiers. Doing so will generate a final `master_out.csv` file. Starting the applicaiton and picking `restart` to restart the registration will use `master_temp.csv` as input. 

## Creating an executable
Pyinstaller 3.3 can be used to generate an executable from the Python file. Please note that there are two hidden requirements:

* 'nfc.clf.acr122'
* 'pandas._libs.tslibs.timedeltas'

Running pyinstaller with the provided spec file as argument should include these requirements.

## Other remarks
The original idea was for the application to use a database for registration management. Due to time contraints the scope had to be scaled back and the choice was made to use a csv file based system.

## Contributing
The application is not being actively maintained, but feel free to create pull requests if so desired.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details