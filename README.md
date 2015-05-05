# WhatsApp Tracker

## Introduction
The aim of this project is to track WhatsApp users' behavioral patterns by analyzing the time they are online using WhatsApp.

## How does this work
Unlike other services, WhatsApp does not provide any API to access and play with users data. This makes it relatively hard to create bots, track users and automate WhatsApp. It is hard but that does not mean it is impossible.

I am just scraping the screen pointing to the WhatsApp web interface and using OCR to check if the user is online. If it can read the user is online, it stores it to the database and we can plot it using any plotting tool and analyze the users behaviour.

So, for this to work, you may have to adjust the screen capturing coordinates according to your screen resolution and the browser position. This is a tricky part as you need to tune it everytime you setup. But if you are using a dedicated machine (I am planning to use my RaspberryPI), this should not be a problem as it will be a one time setup.

## What is it useful for?
It depends upon how you use it but once you grab the data, you will start finding a way to use that.
Let me warn you not to use this to invade anyone's privacy and use it in your legal limits. I am not resposible for how you use it.

## Limitations
- Each instance can track only single user at a time
- Each instance needs a dedicated machine or virtual machine to run
- It uses screen capturing and so it needs to be configured separately for different resolutions.
- No good documentation... author is lazy/busy.