# Testing

If you don't want to create the new account to test certain features use the credentials bellow:
- Username: test-account
- Password: Test123

## Register

1. Try register leaving all fields empty
2. Try register with a username that is already registered


Creating a new account:
- When on the login page if the user clicks 'register now!' they will be taken to the register page where the user can create a new account.
- When creating an account, all fields have been filled out and the user clicks register, the backend code will do a quick check on the username provided by    the user and check it against all the usernames in the datebase, if the username exists they will be redirected to the registration page and a message will be   flashed.
![User Alrady registered](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/user-already.png) 

- If registration is successful the user will be redirected to the home page and flashed a successful message
![successful Message](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/successful-message.png) 


- Below is the layout for the username data in MONGODB
![Username MONGODB](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/user-db.png) 

## Login

Loggin In:
1. Try logging in with both fields empty
2. Try logging in with a registered username but no password
3. Try logging in with a registered username and the incorrect password
4. Try logging in with a non registered username but a registered password

- When A user provides a Username and Password the backend code will check for a username matching the username from the input form if it finds a match it will then proceed to check the password provided against the one stores in the database, if one of these are not a match the following message will be flashed.
![Invalid Username/Password](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/invalid-username-pasasword.png) 
- If successful the following message will be flashed.
![Login successful](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/login-successful.png)

## Admin panel

- To access the admin panel a user must have admin permission, if the user does not have admin permission they will be redirected to the login page:
![Please login as admin](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/login-as-admin.png)


## Add game

This page can be found under "ADD" on the navbar then click "Game":

- All important input fields have the required tag, this stops empty filds being pushed to the DB

- When a user successfully adds a game they will be redirected to the "view_games" page and flashed the following message:
![Game added success](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/game_added_succ.png)

- If the user leaves the game image input box empty a default image will be applied to games page:
![Default game image](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/place-holder-game-img.png)

- If the user adds a image url it will use the image provided:
![User added game image](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/example-game-img.png)


## Add review
This page can be found under "ADD" on the navbar then click "Review":

- All the input boxes contain the required tag.

- When a user successfully adds a review they will be redirected to the "home_page" page and flashed the following message:
![Review added success](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/login-as-admin.png)

## Add developer/publisher
These pages can be found under "ADD"  then "publisher" or "developer" both pages use the same layout :

- All the input boxes contain the required tag.

- The user will be redirected to the "view_developer" or the "view_publisher" and flashed a success message

## Add category
The add category page only has one input box, this input has the important tag attached too
- When a user tries to submit an empty string to the DB it will flash requesting that the user fills out the field.

