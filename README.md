Python: 3.5.4

Cloud server: EC2

Application Deployment IP: 18.222.81.146

#############################################################################################

Bugs are fixed from HW5

1.@transaction.atomic is implemented when adding posts and comments.

2.user bio can be updated correctly.

3.Commit multiple times with definite goal.

4.Test with string form usernames. It will not cause crash now.

5.Add a link so that when a user you are going to follow doesn't exist, you will be guide to that page.

6.Valid the bio input content. This time if a post is forged without typing actual bio, error message will be displayed.

#############################################################################################

CITINGS:

1.The login, register, logout, add comment parts cite the code from lecture notes.

2.Part of CSS are cited from w3schools:
ul.nav_class_list, li a.nav_class_bullet, li a.nav_class_bullet:hover   from https://www.w3schools.com/css/css_navbar.asp
input[value=Login], input[value=Register]                               from https://www.w3schools.com/css/css3_buttons.asp

3.Pictures are cited from:(not displayed in hw4 yet)
alt="knot"          from                           https://www.iconfinder.com/icons/284399/bow_decoration_knot_icon#size=64
alt='snowflake'     from
https://www.google.com/search?sa=G&hl=en&q=black+and+white+snowflake&tbm=isch&tbs=simg:CAQSlwEJOetDtvi1JVoaiwELEKjU2AQaBAgUCAAMCxCwjKcIGmIKYAgDEiicBpsGmxKgBpoGtgeeBuMBtwf6CaI07CGSKZUpoTSuNIk4yTfFN8o3GjBTkegdrkCRpsJKXjRLuZHzb7LHPX82zV6Og4G8EUFZVpe_1J8lex3YONDdPN6evvkwgBAwLEI6u_1ggaCgoICAESBLLcL0wM&ved=0ahUKEwijmY_u5aHZAhWirVkKHeCRAS0Qwg4IJigA&biw=1280&bih=566

4.Models functions: 
create_user_profile(sender, instance, created, **kwargs)
save_user_profile(sender, instance, **kwargs)
are both cited from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

#############################################################################################

Thank you!