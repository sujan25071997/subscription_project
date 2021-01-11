# subscription_project

=> Run - MySQL Command Line Client
=> Create a Database name "django_project"
$ CREATE DATABASE django_project

=> and make changes according to your MySQL configurations in settings>DATABASES

=> download Zip file of the project from GitHUb repository
 https://github.com/sujan25071997/subscription_project.git

=> extract on your local machine
=> open terminal and Change Directory to project location
=> create a virtual environment and activate it
$ virtualenv env
$ env/Scripts/activate

=> Now install the projects requirements
$ pip install -r requirements.txt   

=> Now we create a Database table for a project
$ python manage.py makemigrations
$ python manage.py migrate

=> now run the server
$ python manage.py runserver

=> Now open the browser and search http://127.0.0.1:8000/
=> now SignUp by filling the details
=> then click on login button & Login yourself by using 'username' which is your Email ID and 'password'  
=> after login you can choose the Subscription plan and make the payment
=> after successfully completing the payment it will direct you to 'Thanks' page
