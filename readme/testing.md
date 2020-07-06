# Testing

If you don't want to create the new account to test certain features use the credentials bellow:
- Username: test-account
- Password: Test123

## Register

Creating a new account:
- When on the login page if the user clicks 'register now!' they will be taken to the register page where the user can create a new account.
- When creating an account, all fields have been filled out and the user clicks register, the backend code will do a quick check on the username provided by    the user and check it against all the usernames in the datebase, if the username exists they will be redirected to the registration page and a message will be   flashed.
![User Alrady registered](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/user-already.png) 

-If registration is successful the user will be registered to the home page and flashed a successful message
![successful Message](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/successful-message.png) 

## Login
Loggin In:
- When logging in if the user forgets to enter one or both fields it will flash a message.
![Please fill in this field](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/please-fill-in.png)  
- When A user provides a Username and Password the backend code will check for a username matching the date from the input form if it finds a match it will then proceed to check the password provided against the one stores in the database, if one of these are not a match the following message will be flashed.
![Invalid Username/Password](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/invalid-username-pasasword.png) 
- If successful the following message will be flashed.
![Login successful](https://raw.githubusercontent.com/danielclements/game_score.gg/master/readme/login-successful.png)

