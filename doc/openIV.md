# OpenIV command line documentation

To customize OpenIV running you can use next prams’:

-core.game.select:false   - Don't show game select dialog

-core.game.select:true    - Always show game select dialog

-config.installed:false   - Show welcome screen

-core:[Filename]          - Load OpenIV core from [Filename] (by default it load Core.xml)

-core.game:[GAME_ID]      - Start OpenIV without game select dialog and load [GAME_ID] game.


Examples:

OpenIV.exe -core.game:IV  - To run OpenIV work with GTA IV and without game select dialog

OpenIV.exe -core:CustomCore.xml   - Run OpenIV with custom core.xml

OpenIV.exe -core.game.select:false Run OpeniV without game select dialog and load default game

OpenIV.exe "archive.img" /search:test - Open archive with search