![Logo](/home/brian/code/Inter-Planetary-Flash-Cards/src/assets/ipfc_logo.png)

# Inter-Planetary-Flash-Cards

Universal flashcard converter, decentralized flashcard cloud storage, and flashcard app

## What is IPFC?

The goal is for IPFC to be:
 * A universal flashcard format converter, 
 * A decentralized flashcard cloud storage for flashcards, leveraging [IPFS](https://ipfs.io) and finally 
 * Flashcard and EdTech app ecosystem

## Currently IPFC is:

 * A minimal flashcard app for desktop computers.
 * A converter for [Quizlet](https://quizlet.com) flashcard decks exports, solving some of the inconsistencies in export format, especially dealing with images and line breaks.
 * A cloud storage solution for the cards using the [Inter Planetary File System](https://ipfs.io).

## Why IPFC?

Currently there are two main use cases:

### Syncing & Sharing

Users and developers of educational apps who would like to have their flashcard decks more easily shared between apps. 

The popular apps [Kahoot!](https://kahoot.com/) and [Gimkit](https://www.gimkit.com/) are cooperative/competitive flashcard games played live in a classroom.  Most users of those apps are starting with a flashcard deck (also referred to as a set) created in Quizlet. 

The export/import procedure takes some time, and often corrupts the data when the cards have not been formatted properly between apps. In an IPFC-style ecosystem, new app creators could have users instantly able to use their app/game bringing all of their previous cards with them and with no data loss.

Not only could the flashcards themselves be shared, but also user’s performance data. While Kahoot might give a report of the users performance in the game, those are results are not shared with Quizlet. If users’ performance across apps could travel with them, they could better use their study time across apps by only reviewing the cards that are often forgotten. If you keep getting an answer wrong, it will show up in all the apps you use, if you’ve proven an answer is easy to you it will show up less in any app you use.

### Data ownership

Developers and serious users of flashcard apps, especially those who use long term learning Spaced Repetition Software (SRS), who would like their data to be syncable across devices, but worry the current systems available lock them into using one company/organization’s set of apps and don’t give them control of their own data. 

Users might fear that the company goes bankrupt, suffers an attack, or changes the user agreement, holding the user’s data hostage. IPFC solves this issue by letting users host their own data on the IPFS. Although the current implementation of IPFC requires a private database for storing user information and passwords, even in its current state, if the IPFC database goes offline, users can immediately access all of their data as it has been constantly backed up on the IPFS. This allows users to feel comfortable using a new service they can get out of any time. 

If a developer wants to create an app, for example a flash card game, and they’d like to try connecting it to a flashcard review or creation app, they would have to ask that app for permission first or require users to go through an inconvenient import/export. In the IPFC ecosystem, they could add a new app that instantly works with all the others without asking for permission. They also don’t have to worry that one day IPFC will start charging them for access or suddenly disappear. Until a purely decentralized model is created, the IPFC centralized database will regularly upload the semi anonymous user IDs, and user collection data of the whole project to the IPFS at a publically shared location. This means another development team could instantly fork the project and run the centralized server with no interruptions to users as long as users recorded their ID.

Please stay tuned for more updates and detailed explanations for users and developers.

# Build & Install Instructions

As this is a very new project, if you want to run it now, you need to run it locally.  Hopefully it will be hosted in the very near future.

## Development Instructions

1. Clone the entire repo
2. Ensure you are running nodejs (version 10+) 
3. In the directory in which you cloned the project into run 
   ```script
   npm i install
   ```
   
4. Finally run the app in debug mode:
   ```script
   npm run serve
   ```
5. To get started with some flashcard decks, feel free to use the testing account:

```
Username: hello@world.ipfc
Password: Password123
```

Because there are many images in the test decks, the initial sync might take some time.


Found Bugs? Create an issue on the issue tracker, or post it in the [support group](https://t.me/joinchat/HFuUg0iRw-CrD5QbOByfSQ)

