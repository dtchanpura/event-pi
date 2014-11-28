# Event-Pi

A small and simple event management tool for everyone...
[Get EventPi](http://geteventpi.com)

## Start here
For most of the testing purposes we are created a virtual environment which might not be available. To do so we have provided a ```requirements.txt``` file following will create a new virtual python runtime environment and we will install those packages locally in this folder.
```sh
~/event-pi$ virtualenv venv
~/event-pi$ venv/bin/pip install -r requirements.txt
```
For running the server it needs this `venv` folder which has this binary files for Python. To run just type down
```sh
~/event-pi$ venv/bin/python run.py
```
This will start server according to the `config.py` file which is to be renamed right after the setup. To start the local SMTP server for logs on mail we need to use python's `smtpd` as follows.
```sh
python -m smtpd -n -c DebuggingServer localhost:25
```
> If this gives error try running it as administrator/sudo.

To be added..

### Webpage Tree

#### Home Page / Event Management Page

Details about all events that are been added in database which are going to be held or have completed.

It mainly contains all events and links to their details and also adding a new event

#### Event Details Page

Gives details about the selected event such as name, address, date, fees and attendees till date.

#### Add Event Page

Adding new event form page which takes all those details about an event to be organized like place, fees...

#### Add User Page

Adding a new user form page which takes those details about user for some event and generates QR Code and sends them on their email.

#### Show Attendees

This page shows details about which users are going to attend the event.

#### Admin Page (Realtime data of those who are present)

At the time of event this page shows details whether the user has attended or not.

### Backend Tree
The basic structure of our database is containing three table as follows

![Database Overview](https://dl.dropboxusercontent.com/u/93136802/eventpi/db_overview.png "Database Overview")

As it can be understood the user table has the data related to user and all details like name, contact informantion and qr_data (which will be stored in the QR code) in same way the other table event_details will have details about the event which are been organized.

The data may come from many places like registration from the official website and then could be added as a simple comma separated values (.CSV) file containing fields with semi-colon. e.g.
```
first_name;last_name;email;college_name;contact_no;
Hodor;Rodoh;hodor@hodor.hodor;hodor;;
```
