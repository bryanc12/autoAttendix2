# autoAttendix2
The autoAttendix2 is a better version of [autoAttendix](https://github.com/bryanc12/autoAttendix). It use the api instead of the web interface, which boost the performance significantly by skipping the process of waiting the web interface to load which takes a long time.

You may use the included QR Code image files for testing and checking if everything is working as expected or correctly.

## Requirements
1. Python 3.10
2. Internet :smiley:
   
## How to use
1. Add your ApSpace login credentials and mode to settings.json file. <br> For Example:
```json
{
    "username":"tp012345",
    "password":"password",
    "discord-bot":false,
    "discord-webhook":"",
    "power-saving":true
}
```
 - Turning ```power-saving``` on(true) will capture that screen less frequently for resources saving purpose, by turning it off(false), the programm will take more resource and power consumption, but this increase the sensitivity of QR code recognition.
 - Turning ```discord-bot``` on(true), the program will send message to the discord server whenever it log to console. By turning this on(true), the ```discord-webhook``` have to be a valid webhook address, more information about discord webhook can be found [below](#discord-webhook).
  
2. Click on start.bat and it will do their works.

## Discord Webhook
By using the discord webhook, the program will send you a message when a attendance signing process is attempted. This feature can be implemented to any private/public server. The webhook can generated with the steps below.

1. Go to discord app homepage
2. On the side navigation bar, scroll to the bottom
3. Select the plus/add symbol button
4. Select ```Create My Own```
5. Select ```For me and my friends```
6. Fill in your desire server name and click create
7. Right click on the server created
8. Select ```Server Settings```
9. Select ```Integrations``` on the side navigation bar
10. Select ```View Webhooks```
11. Select ```New Webhook```
12. Fill in the Webhook ```Name``` and choose your desire ```Channel```(#general as default)
13. Select ```Copy Webhook URL```
14. Paste the URL into the ```settings.json``` as example below, and set the ```discord-bot``` to ```true```
```json
{
    "discord-bot":true,
    "discord-webhook":"https://discord.com/api/webhooks/963589414606789804/RtZ_PnmMV_Ywxu132uTvSQn_xCjKdddawawdjw-GxY47AaUNe2kdwDWfSENyplS",
}
```
15. Done

## To do:
 - Multi User :hourglass:
 - Telegram Integration :hourglass:
 - Instagram Integration :running_man:
 - Discord Integration :heavy_check_mark: