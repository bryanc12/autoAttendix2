import gc
import json
import time
from datetime import datetime

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
from PIL import ImageGrab
from pyzbar.pyzbar import ZBarSymbol


def main():
    global DiscordWebhook, DiscordEnabled
    username, password, powerSaving, DiscordEnabled, DiscordWebhook = getSettings()
    print('Start Tracking Attendance...\n')

    # Define variables for checking use
    lastOtpCode = None
    lastSignTime = time.time()

    # Loop for OTP Code and Sign after settings readed from settings file
    while True:
        while True:
            otpCode = getOtpCode(powerSaving)

            # If OTP Code is None type(Never attempt to sign otp before) or the OTP Code is 
            # different from from the last signed code then attempt to sign the OTP Code 
            if (otpCode == None) or (otpCode != lastOtpCode):
                break

            # When the OTP Code is same as the last signed OTP Code, check if it is 5mins ago
            # If yes, attempt to sign the OTP Code again, else sleep for 5 seconds
            lastSignGap = time.time() - lastSignTime
            if (lastSignGap > 300.0):
                break
            else:
                time.sleep(5)

        log('OTP Code Found -> ' + otpCode)
        signAttendance(otpCode, username, password)
        lastOtpCode = otpCode
        lastSignTime = time.time()

        gc.collect()


def getSettings():
    # read credentials from settings.json
    data = json.loads(open('.\settings.json', 'r').read())
    # Check if credentials are not empty
    if not (bool(data['username']) or bool(data['password'])):
        print('Please fill in your username & password!')
        exit()
    # Check if mode are valid(if mode are not True or False)
    if (type(data['power-saving']) != bool):
        print('Please fill in the power mode(true/false)!')
        exit()
    # Check if discord-bot is enabled
    if ((data['discord-bot'] == True) and not bool(data['discord-webhook'])):
        print('Please fill in the discord webhook, check documentation for more info!') 
        exit()
    
    return (data['username'], data['password'], data['power-saving'], data['discord-bot'], data['discord-webhook'])


def getOtpCode(powerSaving):
    # Loop until an OTP Code QR code is found
    while True:
        # Try to capture the screen
        try:
            img = ImageGrab.grab()
        except OSError:
            # If OS deny capture of screen, handle the exeption and screen capture again 
            print('Screen capture permission denied by Operating System, error handled and solved.\n')
        # Turn pixels data into array form
        imgNp = np.array(img)
        # Invert image (black to white, white to black)
        imgNp = cv2.bitwise_not(imgNp)
        # Turn pixels array from color to greyscale
        frame = cv2.cvtColor(imgNp, cv2.COLOR_BGR2GRAY)
        # Scan picture for capturing QR code
        decodedData = pyzbar.decode(frame, symbols=[ZBarSymbol.QRCODE])
        sorted(ZBarSymbol.__members__.keys())
        # Convert scanned object object into string, and check it is a valid QR code in 3 digit form
        for obj in decodedData:
            otpCode = obj.data.decode('utf-8')
            if otpCode.isdecimal():
                if (len(otpCode) > 0) and (len(otpCode) < 4):
                    return otpCode
        gc.collect()

        if powerSaving:
            time.sleep(1)
        else:
            time.sleep(0.1)


def signAttendance(otpCode, username, password):

    refreshTokenRequestUrl = 'https://cas.apiit.edu.my/cas/v1/tickets'
    signApiUrl = 'https://attendix.apu.edu.my/graphql'

    # Common header for questing refresh token and api request ticket
    commonHeader = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain',
    }

    refreshTokenRequestParameter = {
        'username': username,
        'password': password
    }

    refreshTokenResponse = requests.post(url=refreshTokenRequestUrl, headers=commonHeader, params=refreshTokenRequestParameter)
    refreshToken = refreshTokenResponse.text

    ticketRequestUrl = 'https://cas.apiit.edu.my/cas/v1/tickets/' + refreshToken + '?service=https://api.apiit.edu.my/attendix'
    ticketRequestParameter = {
        'service':'https://api.appit.edu.my/attendix'
    }

    ticketRequestResponse = requests.post(url=ticketRequestUrl, headers=commonHeader, params=ticketRequestParameter)
    ticket = ticketRequestResponse.text

    signHeader = {
        'accept':'application/json',
        'content-type':'application/json',
        'ticket':ticket,
        'x-amz-user-agent':'aws-amplify/2.0.7',
        'x-api-key':'da2-dv5bqitepbd2pmbmwt7keykfg4'
    }

    signVariables = {
        'otp':otpCode
    }

    signQuery = 'mutation updateAttendance($otp: String!) {\n  updateAttendance(otp: $otp) {\n    id\n    attendance\n    classcode\n    date\n    startTime\n    endTime\n    classType\n    __typename\n  }\n}\n'

    signJson = {
        'operationName':'updateAttendance',
        'variables':signVariables,
        'query':signQuery
    }

    signResponse = requests.post(url=signApiUrl, headers=signHeader, json=signJson)
    signResponseJson = signResponse.json()

    if signResponseJson['data'] is not None:
        log('Attendance successfully taken for `' + signResponseJson['data']['updateAttendance']['classcode'] + '`\n')
    else:
        log(signResponse.json()['errors'][0]['message'] + '\n')


def log(rawMsg):
    # Get current date time in defined style
    dateTime = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    msg = (dateTime + ' ' + rawMsg)
    print(msg)

    # Send message to discord server if webhook provided
    if DiscordEnabled:
        discordJson = {'content':msg}
        requests.post(url=DiscordWebhook, json=discordJson)

    # Append msg to latest.log
    with open('latest.log', 'a') as logFile:
        logFile.write(msg +'\n')

if __name__ == '__main__':
    main()