# SFOS_Calendar_Search
A basic Python script using sqlite to search text into SFOS Calendar

It will only match with events containing all search terms you entered, found either in Description, Summary or Location fields.

With the help of ```qcommand``` (or ```ShellEx```?), the idea is to easily search for text into the calendar.

At the moment alas, only useable as root.

Enjoy!

Remarks and suggestions are welcome as I am very noob.


## Some tips on how to use it
Copy this script to your favourite place on the phone.

Install python3-sqlite.

cd to the dir where you copied it and change the ownership so you can use/edit it: ```chown 100000:100000 ./calendar_search_[version number].py```
Make it executable with ```chmod +x ./calendar_search_[version number].py```.

Install qCommand and create an entry for it: enter the path where you stored the script and click "Interactive" so you can enter keywords to search for into the terminal window it will automatically open.


After the search, you will get a list of events where ALL your keywords were found.

This list displays:

-Starting Date/Time of the event

-The event description, summary and location

Unfortunately, at the moment, you'll have to tick "run as root" into qCommand. 

Always inspect the script before doing such a thing.

This script is shared without warranties. It works on my phone but might harm yours.
