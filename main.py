import sys
from pandas import read_csv
import nfc
import winsound
import time


def main():
    print(r'''                                                                           
 _____     _   _                  _____       _                               
|  _  |___| |_| |_ ___ ___ _ _   |  |  |___ _| |___ ___                       
|     |   |  _|   | . |   | | |  |  |  | -_| . | -_|  _|                      
|__|__|_|_|_| |_|_|___|_|_|_  |   \___/|___|___|___|_|                        
                          |___|                                               
 _____ ___ ___ _                    _____         ___                         
|     |  _|  _|_|___ ___ ___ ___   |     |___ ___|  _|___ ___ ___ ___ ___ ___ 
|  |  |  _|  _| |  _| -_|  _|_ -|  |   --| . |   |  _| -_|  _| -_|   |  _| -_|
|_____|_| |_| |_|___|___|_| |___|  |_____|___|_|_|_| |___|_| |___|_|_|___|___|
                                                                              
==============================================================================
''')
    print("Ok. Starting registration application...")
    inlist = loadexcel()
    outlist = registerinput(inlist)
    saveexcel(outlist)
    raw_input('Press ENTER to exit.')


def loadexcel():
    state = raw_input(
        "Is this a new session or are you restarting during a registration session?\nNEW/RESTART: ").lower()
    if state == 'new':
        while True:
            cleanlist = raw_input(
                "Did you place the 'master.csv' list in the 'Lists' folder? And remove any previous list from that folder?\nY/N: ")
            if cleanlist.lower() != 'y':
                continue
            else:
                break
        try:
            inlist = read_csv("./Lists/master.csv", sep=";")
            print("Loaded master list")
            return inlist
        except IOError:
            print("Master file not found!")
            loadexcel()
    elif state == 'restart':
        try:
            inlist = read_csv("./Lists/master_temp.csv", sep=";")
            print("Loaded existing list")
            return inlist
        except IOError:
            print("Existing file not found!")
            loadexcel()
    else:
        print("Did not recognize input. Please select either new or restart...")
        time.sleep(2)
        loadexcel()


def saveexcel(outlist):
    print("Saving list...")
    outlist.to_csv("./Lists/master_out.csv", sep=";")
    print("Done.")
    winsound.Beep(800, 200)
    winsound.Beep(600, 200)
    winsound.Beep(400, 200)


def registerinput(inlist):
    taglist = []
    bluetaglist = ['CA39670C','10DF354F','8073804E','DA81850B','E0BD214F','E0B9214F','B06C434F']
    clf = scannerconnect()
    print("The system is now listening... To stop listening, scan a blue tag.")
    while True:
        try:
            tag = str(clf.connect(rdwr={
                'on-connect': lambda tag: False
                , 'beep-on-connect': True
            }))[-8:]
        except IOError:
            clf.close()
            return inlist
        if tag in bluetaglist:  # for dev purposes
            print
            clf.close()
            break
        elif tag not in taglist:
            taglist.append(tag)
            print('\r' + tag + ' '*20),  # Dev purpose
            winsound.Beep(1000, 350)
            try:
                inlist.Check[inlist.RegCode == tag] = "Yes" #This needs to be caught in an exception block.
            except:
                print('''
                There is something wrong with the formatting of the Excel file.
                Please ensure that the column containing the codes is labeled "RegCode".
                The column to the right of RegCode should be labeled "Check".
                ''')
            inlist.to_csv("./Lists/master_temp.csv", sep=";")
            time.sleep(1)  # keep sleep for scan delay
        elif tag in taglist:
            print('\r'+"Tag already registered."),
            winsound.Beep(800, 200)
            winsound.Beep(800, 200)
            winsound.Beep(800, 200)
            time.sleep(1)  # keep sleep for scan delay
        else:
            print('\r'+"Input error, please retry. If this error keeps appearing, please find human assistance."),
    print
    clf.close()
    return inlist


def scannerconnect():
    try:
        clf = nfc.ContactlessFrontend(
            'usb:072f:2200')  # LET OP: Gebruik de Zadig driver installer om de ACS driver te vervangen met de standaard WINDUSB driver
        return clf
    except IOError:
        print(
            '''Can't find NFC reader device. Is the reader connected?
If yes, then please stop this app, take out the scanner and plug it in again. Then restart this app.

If this also does not help, check if the correct driver is installed:
   1. Please find the 'Zadig' tool in the application folder
   2. Pick list all devices under the options menu
   3. Find the ACS device in the list
   4. Select the winusb entry in the selector to the right of the green error
   5. Press install WCID driver and click OK in any prompts
   6. The driver is now installed. Please restart the registration program.
   ''')
        raw_input('Press ENTER to exit.')
        sys.exit(0)


if __name__ == '__main__':
    main()
