# Inter-Planetary-Flash-Cards
Universal flashcard converter, decentralized flashcard cloud storage, and flashcard app


What is IPFC?

The goal is for IPFC to be:

•	A universal flashcard format converter, 

•	A decentralized flashcard cloud storage for flashcards, and finally 

•	Flashcard and EdTech app ecosystem

Currently IPFS is:

•	A very minimal flashcard app for desktop computers.

•	A converter for Quizlet flashcard decks exports, solving some of the inconsistencies in export format, especially dealing with images and line breaks.

•	A cloud storage solution for the cards using the Inter Planetary File System.


Why IPFC?

Currently there are two main use cases:

• SYNCING AND SHARING:

Users and developers of educational apps that would like to have their flashcard decks more easily shared between apps. 
>	The popular apps Kahoot and Gimkit are cooperative/competitive flashcard games played live in a classroom.  Most users are starting with a flashcard deck (also referred to as a set) created in Quizlet. The export/import procedure takes some time, and often corrupts the data when the cards have not been formatted properly between apps. In an IPFC-style ecosystem, new app creators could have users instantly able to use their app/game bringing all of their previous cards with them and with no data loss.

>	Not only could the flashcards themselves be shared, but also user’s performance data. While Kahoot might give a report of the users performance in the game, those are results are not shared with Quizlet. If users’ performance across apps could travel with them, they could better use their study time across apps by only reviewing the cards that are often forgotten. If you keep getting an answer wrong, it will show up in all the apps you use, if you’ve proven an answer is easy to you it will show up less in any app you use.

• USER CONTROL OF DATA:

Developers and serious users of flashcard apps, especially those who use long term learning Spaced Repetition Software (SRS), who would like their data to be syncable across devices, but worry the current systems available lock them into using one company/organization’s set of apps and don’t give them control of their own data. 

>	Users might fear that the company goes bankrupt, suffers an attack, or changes the user agreement, holding the user’s data hostage. IPFC solves this issue by letting users host their own data on the IPFS. Although the current implementation of IPFC requires a private database for storing user information and passwords, even in its current state, if the IPFC database goes offline, users can immediately access all of their data as it has been constantly backed up on the IPFS. This allows users to feel comfortable using a new service they can get out of any time. 

>	If a developer wants to create an app, for example a flash card game, and they’d like to try connecting it to a flashcard review or creation app, they would have to ask that app for permission first or require users to go through an inconvenient import/export. In the IPFC ecosystem, they could add a new app that instantly works with all the others without asking for permission. They also don’t have to worry that one day IPFC will start charging them for access or suddenly disappear. Until a purely decentralized model is created, the IPFC centralized database will regularly upload the semi anonymous user IDs, and user collection data of the whole project to the IPFS at a publically shared location. This means another development team could instantly fork the project and run the centralized server with no interruptions to users as long as users recorded their ID.


How IPFC?

Please stay tuned for more updates and detailed explanations for users and developers.

For now, to use the app:
1)	Download the whole github repository 

2)	Install the python libraries: pip install -r your/path/to/requirements.txt

3)	Run the IPFC_main.py file

To get started with some flashcard decks, feel free to use the testing account:

Username: 123@123.123

Password: Password123

Because there are many images in the test decks, the initial sync might take some time.
