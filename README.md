# pokeFetch: An interactive GUI pokedex app written in Python 

### Video Demo: <URL HERE>

### Description:

#### A cross-platform python application for viewing Pokédex information including such as base stats and abilities. Additionally, users can maintain a set of parties where they can create their own sets of pokemon to plan out teams for using in game. 

* To implement a GUI environment, I’ve used the tkinter Python library, which allows for the creation of a GUI window with widgets and labels to create a user interface.  

* I have implemented a login screen so the program can keep track of which user id they should be pulling parties from. New users can register their login, which will insert them into the SQL database in the users table. 

* Once the user logs in, they are presented with the information of the first Pokemon in the Pokedex – Bulbasaur – and they can then search for other Pokemon using the search box at the bottom of the screen or access a list of their parties by clicking the ‘Parties’ button below the search box. The user also has the option to scroll through the Pokedex in incrementing Pokedex ID order using next and previous buttons. For example, if you clicked the ‘next’ page from the Bulbasaur page, you would see Ivysaur’s page, and if you click ‘previous’ from Bulbasaur’s page, the list wraps around to the final Pokemon in the Pokedex at time of writing – Pecharunt. 

* To fetch the Pokemon sprites and information, I’ve used the pyPokedex library, which implements functions for fetching information from the pokeAPI web API. This saved a lot of work maintaining a large database of Pokemon and allowed for relatively quick acquisition of the sprite photos. However, I’ve probably look to use a more efficient method to fetch multiple requests from this API, because the party summary pages are quite slow to load due to the large number of simultaneous requests. 

* Users can create parties, which will be inserted into the parties table in the SQL database. These are then shown in a list on the ‘parties’ page. The user can then click on a party summary button, which will show them the Pokemon in the given party, as well as the sprites of the Pokemon in that party, their names and their type information in a list format.  

* TODO - At the bottom of the page is a visual that displays type coverage for the selected party, and displays weaknesses using red, grey, and green to indicate coverage. 

* Users can delete whole parties, or also delete individual Pokemon from a given party using buttons in the GUI. This will remove the specific party from the SQL database, and from the list of parties in the users’ party page.  

* TODO - On the parties page, users can check type coverage to see if their parties have weaknesses against certain types of pokemon in battle, and can use these stats to try and improve their teams. 
