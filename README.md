## Event-Pi

A small and simple event management tool for everyone...
[Get EventPi](http://geteventpi.com)

###Start here
For most of the testing purposes we are created a virtual environment which might not be available. To do so we have provided a ```requirements.txt``` file following will create a new virtual python runtime environment and we will install those packages locally in this folder.
```
event-pi/$ virtualenv venv
event-pi/$ venv/bin/pip install -r requirements.txt
```

####Webpage Tree



####Backend Tree
The basic structure of our database is containing three table as follows

![Database Overview](https://dl.dropboxusercontent.com/u/93136802/eventpi/db_overview.png "Database Overview")

As it can be understood the user table has the data related to user and all details like name, contact informantion and qr_data (which will be stored in the QR code) in same way the other table event_details will have details about the event which are been organized.

The data may come from many places like registration from the official website and then could be
