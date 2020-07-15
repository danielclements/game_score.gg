# GameScore.GG

I got the idea for this project when I was looking for A new game to play, as A was scrolling through game review sites I noticed a glaring issue that all the reviews were written and published by said websites, very few websites had a focus on user reviews.   

I wanted to build this project as a place for people to read real opinions from gamers like them and make an informed purchase decision.

 
## UX
 
My design philosophy for this project was to keep everything simple for the user side of the site. I wanted people to visit the site and discover new games, I didn't want to force anyone to make an account in order to view things like games, developers, or publishers. A user would need to create an account to review a game. I would hope seeing other users' reviews would inspire other users to submit reviews too, once a user discovers a game on the site and decides that they will purchase it would be ideal if they to would return to the site to leave a review on said game. I  have added a featured games section to the home page, this way if people are only having a glance at the site hopefully they will click on one of the featured games and check some of the reviews out.


When the user wants to add an item they need to press the 'add' button on the navbar and select the item they want to add (game, review ...) then fill out the form, in order to access the form the user must be logged in, if not they will be redirected to the login page.

The form the user will have to fill out will change depending on what they decide to add, once the form is submitted the user will be redirected to the appropriate page and flashed a message to let them know the form was submitted and added to the DB successfully.

- As a game enthusiast, I want to write reviews of my favorite games to inspire others to experience and enjoy the games I enjoy.

- As a gamer I want to find a new game to play, I like to read reviews from other players and make my decision to purchase a game based on the reviews of others.


[Wireframes / Mockups!]()

## Features

### Existing Features
- Authentication
    - User registration allows a user to create an account and began posing reviews 
    - User login allows a user to login, when logged in a session is started and the Username will be printed on all documents the user adds to the DB, used later on when checking if a user has permission to edit a record
    - User logout will stop the current user's session, when logged out a user can no longer add/edit records to the DB 

- Add Developer
    - Adding a developer using the front end form, after adding a developer it will allow you to use this developer when adding a game.

- Add publishers
    - Adding a publisher using the front end form, after adding a publisher it will allow you to use these publishers when adding a game.

- Add Category
    - Adding a category using the front end form, after adding a category it will allow you to use this category when adding a game.    

- Add Game
    - Adding a game is the result of adding all the above, after filling out the form and adding the game you can now add a review for said game.
    ![Add game form](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/add_game_form.png)

- Add Review
    - Add a review for any of the games on the site, once added the review will appear with all the other reviews for the game you choose.

- Edit records
    - When a user wants to edit a game or a review the first thing the application does is check if the user has logged in and a session was started, if the username in the current session does not match the user name that added the game they will be denied access to the edit page, if the user name is a match then they will be redirected the edit page and allowed to submit the edits.

- filter
    - Allows the user to filter the view games page by game category, this allows a user to find games in a specific genre


### Features Left to Implement

- pagination to games page as having to many games on one page could casue issues down the line.

- A profile page that will display all the items that user added, this will maek it easier for a user to update/ delete added content.

## Technologies Used

- [HTML 5](https://en.wikipedia.org/wiki/HTML5)
    - The project uses **HTML 5** to write the front end of the website.

- [CSS 3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
    - This project uses **CSS 3** to style the front end of the website.

- [Javascript](https://www.javascript.com/)
    - Used within bootstrap elements.

- [Python](https://www.python.org/)
    - Python handles all backend code for this site

- [Bootstrap 4](https://getbootstrap.com)
    - This project uses **Bootstrap** to improve scaling to mobile and to add the contact form.

- [Sketch](https://www.sketch.com/)
    - This project uses **Sketch** to create mockups / wireframes, also used to create the background for the Contact page.

### Frameworks Used
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - Flask is a back-end micro framework and is used in this project.

- [jinja](https://jinja.palletsprojects.com/en/2.11.x/)
    - The project uses jinja for the templating language.
    
- [GSAP](https://greensock.com/gsap/)
    - The project uses Gsap to handle animations.

### CDNs Used
- [Google Font](https://fonts.google.com/)

- [Font Awesome](https://fontawesome.com/)
    


## Testing
[Testing](https://github.com/danielclements/game_score.gg/blob/master/readme/testing.md)

## Database Schema

[Database schema](https://github.com/danielclements/game_score.gg/blob/master/readme/Game_Score.png)

### Browsers used for testing:

- [Google Chrome](https://www.google.com/chrome/)
- [Firefox](https://www.mozilla.org/en-GB/firefox/new/)
- [Safari](https://www.apple.com/uk/safari/)
- [Microsoft Edge](https://www.microsoft.com/en-gb/windows/microsoft-edge)

### Devices used for testing:

- MacBook Pro 13"
- Office PC with 28" monitor 
- Office PC with 24" monitor 
- Iphone 11
- Google Chrome dev tools using multiple view ports

### Bugs:

- Feautred game slider on the home page, expands depending on the image selected

- When a user tries to access a feature that requires login they will be rerouted to the login page, when logged in they will then be returned to the home page instead of the page they originally tried to access.

## Deployment

This project is hosted on heroku [GameScore.GG](http://game-score-gg.herokuapp.com/home)

This python project is dependent on a few packages.

First these need to be installed, we can achieve this with the following command: pip install -r requirements.txt

This project is hosted on heroku, I achieved this by:

1. Going to the heroku dashboard and creating a new app.
2. Then the 'Deploy' section and down to 'deployment method' select github and link heroku to this repository.
3. Create a 'config vars' under the 'setttings' tab and add the variable 'Game_Score' with the link and password to the database.
4. Back to the 'Deploy' tab, continuing down to 'manual deploy' and pressing 'deploy branch'.


### Running Code locally:


1. Using Download:
    1. Navigate to `https://github.com/danielclements/game_score.gg`.
    2. Click the green button that says "Clone or Download".
    3. Click download zip.
    4. Extract zip file.
    5. Import in to preferred IDE.

2. Using Git Clone:
    1. Open terminal in preferred IDE.
    2. Type "git clone https://github.com/danielclements/game_score.gg"
    3. you will need to add a  'env.py' file containing 'os.environ["DBname"] = "withTheLinkToTheDataBase"'
    4. This command will install the dependencies for this project: pip install -r requirements.txt
    5. In the terminal write 'pyhton app.py' to run the application.
    



## Credits

### Content
- Wikipedia

### Media

- Main Background for the section was provided by [Pexels](https://www.pexels.com/)


### Acknowledgements

- I used code by [Chris Coyier](https://css-tricks.com/perfect-full-page-background-image/) to add full view height background images.

- Password requirements by [W3Schools](https://www.w3schools.com/howto/howto_js_password_validation.asp)

- Multiple select from [Stakc Overflow](https://stackoverflow.com/questions/50895806/bootstrap-4-multiselect-dropdown)

- Authentication and login provided by[Pretty Printed on Youtube](https://www.youtube.com/watch?v=vVx1737auSE)

- Message flashing tutorial by [Tech With Tim](https://www.youtube.com/watch?v=qbnqNWXf_tU)

- review score slider by [W3Schhols](https://www.w3schools.com/howto/howto_js_rangeslider.asp )

Live version of the site : http://game-score-gg.herokuapp.com/home
