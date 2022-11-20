# Capstone Final Project

For my final project I wanted to create something that solves a problem in the real world. So I created a web application that can be used to monitor health for people. The application helps people who want to lose or gain weight by giving them an easy way to set a goal and track their progress towards their goal. Unlike most other fitness apps, this one is user-friendly and very simple. It removes all the added complexity that most health and fitness services try to provide and focusses entirely on the core fundamentals of what a weight management app should be. The application is built using the Django framework for the back-end and Javascript for the front-end. 

## Distinctiveness and Complexity

The application is visually appealing. Using CSS linear-gradients and box-shadows, the visuals are the most complex part of this project. The progress charts clearly demostrate the complexity of the project with a meter that responds to the users progress towards their goals.

This application is nothing like any other project created during web50. Instead of functioning like a mail service or commerce store, it serves as a management tool to help people choose a fitness goal and track their progress in pursuit thereof.

It uses a wide variety of techniques to complete its functionality. Including an API call and a series of complex javascript functions. It uses a scalable vector graphic to depict progress towards a users goal which allows the visual impact to work as required.

### Contents of files

Since this application is run using django, this file structure follows the same pattern as all the previous web50 projects. We have an app called 'program' within a project called fitness. The program app consists of 5 different html templates and one layout page. Linked to this are 4 corresponding static stylesheets written in CSS. There is only one model, User, which inherits from AbsractUser but with many additional fields e.g. weight, goal, end_date etc. This model is then registered within admin.py so that an administrator can access all of the data. There are 7 different url paths contained within urls.py. Each path is carefully constructed to only be accessible at the right time based on whether a user is authenticated or not. Views.py contains all the code to making the back-end of the server run smoothly and efficiently, including authentication processes and template rendering.

### How to run application
The application can be run the same as all django projects. Download the distribution code and then execute "python manage.py runserver" into your command line to run the application. Then in your browser go to your local server.