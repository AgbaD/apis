# APIs
Here, the abode of a collection of APIs and web apps 
(without template files) which were written using flask 
and Django web frameworks

The apis are divided into two groups based on
the framework used and are listed below.

### Flask APIs
- [Memo API](flask/memo_api)
  
  This is an api used for creating, editing and viewing notes
created by the user
  
  
- [Ecom](flask/ecom%20(web%20app))

  This is a single vendor ecommerce web app. The template files
for this are not present
 
 
- [Contact Validator](flask/con_val)

  #### Technologies: flask, numverify(API), faunadb
  
  A simple email  to check if an email is valid, and to give more
  information about a mobile number.
  
  ### Endpoints
 - ####/register  [POST]
    

    -d {"username":username, "password":"password"}
  
    returns: details

  - ####/login  [POST]
  
  
    -d {"username":username, "password":"password"}
  
    returns: token

  - ####/validat/:email
    Authentication Required


    Replace ':email' with email


    Find out if an email address is valid or not.
    

    -h {"x-access-token": token}

  - ####/info/:number [GET]
    Authentication Required
    

    Replace ':number' with the phone number


    Get information about number. Phone number should be complete 
    number without the plus sign. Eg '234812345678' instead of 
    '+2348123456789'


    -h {"x-access-token": token}

  - ####/user/contacts  [GET]
    Authentication Required


    Get all user api calls and their results
  
  

### Django APIs
- [Notes](django/notes)

  This is a django api used for keeping notes directed either
to a larger body of people (a workspace) or to specific individuals
 
 
- [Movie Ticket API](django/ml)

  This is an api which can be used to get single and multiple movies
and also to purchase movie tickets. The movies are to be added to the database
  by the admin
  

- [Flasher](django/flasher)

  Honestly can't say anything bout this. Its sha an api or web
app built with django.
