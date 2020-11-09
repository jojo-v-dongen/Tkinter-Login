# Tkinter-Login
Working login system using Tkinter and MySQL with captcha

## Disclaimer
This is no well-coded project, tkinter should always be in a class for example and I am sure I messed some other things up!
This was one of my first projects as a beginner (which I still am) so please don't take this code seriously.  
<br/>
## Features
This is a simple tkinter program with 3 "pages", the Home, sign-up and sign-in page.  
The home page is just natural where you can go to the sign-up and sign-in page, when logged in it will show your username.  
The sign-up page will ask you to fill in your:
* Name
* Email
* Password
* Age
* CAPTCHA

The captcha is to prevent automatic bot sign-up and logins. The captcha creates a JPG image with random distorted letters that the human has to fill in.  
When the captcha is failed several times it will reload the page and the user needs to type everything in again.  
The same is for the sign-in page however the captcha will only show up when the user failed to login for several times.
<br/>
## How to use this code
You can either copy the .py file, clone the git or download the file.
For the credentials to save you need to edit the code at the bottom where the connection between the client and server is made.  

*  **Edit the:**
	*  **_host_**:		Use your own host such as localhost or an online host such as freesqldatabase.com  
	*  **_database_**: 	The name of your database  
	*  **_user_**:		Your username  
	*  **_password_**: 	Your password  
