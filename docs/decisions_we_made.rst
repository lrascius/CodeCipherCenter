Decisions We Made
=================

- Django over Flask: Django is a much more full and practical choice for our website.

- Heroku over Google App Engine: Heroku's database is PostGreSQL, relatively simple to
  use with Django. Google App Engine uses NoSQL, much more difficult to use.
  
- Extend built in User model with UserProfile model so that we can add more information
  to use later, such as a profile picture.
  
- Allow for multiple ciphers to be applied in a single challenge.

- Check if a proposed solution is correct on the server, less vulnerable to hacking.

- The difficulty of a challenge is the difficulty of its hardest cipher since in many
  cases the application of lesser ciphers do not increase the difficulty and if they do,
  they don't increase it by much.
  
- Push notifications over email: Use push notifications to alert users to invitations to
  join a challenge instead of emails.
