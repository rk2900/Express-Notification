# Express Notification
* This is the notification module of the express plan and the express status against bong.cn

## Function
* The script will check the status of your order in `Bong.cn`.
* If the status changes, it will get the express information within `shop.bong.cn/order`. Then it will send an email to your mailbox which you set up in `settings.config` file.
* You can set the username and password at Bong.cn in `settings.config` as well as your email configurations.

## Notion
* The mail-send client has been tested only on `126.com`. So you need an email account at `126.com`. Otherwise you should edit the `smtp` server address within the code in `.py` file.
* After you have edited `settings.config_template`, you should #save the file as# new one with the filename of `settings.config`