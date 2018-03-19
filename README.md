# Secret Base

Secret Base is a socialnetwork which implement all basic functions.

## Getting Started

Download and extract the file. This programm is meant to be run on your PC.
To implement on cloud, some parts will be modified.

### Prerequisites

1.Install Python 3.5.4(or above)
2.Install Django
3.Refer to the Django documentation and setup the virtual enviroment.
4.Change path to the folder,then:

```
workon <your virtual enviroment name>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Functions

1. Register, login, logout;
2. Edit your Bio and Picture;
3. Post streams and view others stream;
4. Comment on stream;
5. Follow a user and view other users profiles.

## Authors

* **Zihao Wang**

## Citings

1. The login, register, logout, add comment parts cite the code from CMU 17637 notes.

2. Part of CSS are cited from w3schools:
ul.nav_class_list, li a.nav_class_bullet, li a.nav_class_bullet:hover   from https://www.w3schools.com/css/css_navbar.asp
input[value=Login], input[value=Register]                               from https://www.w3schools.com/css/css3_buttons.asp

3. Pictures are cited from:(not displayed in hw4 yet)
alt="knot"          from                           https://www.iconfinder.com/icons/284399/bow_decoration_knot_icon#size=64
alt='snowflake'     from
https://www.google.com/search?sa=G&hl=en&q=black+and+white+snowflake&tbm=isch&tbs=simg:CAQSlwEJOetDtvi1JVoaiwELEKjU2AQaBAgUCAAMCxCwjKcIGmIKYAgDEiicBpsGmxKgBpoGtgeeBuMBtwf6CaI07CGSKZUpoTSuNIk4yTfFN8o3GjBTkegdrkCRpsJKXjRLuZHzb7LHPX82zV6Og4G8EUFZVpe_1J8lex3YONDdPN6evvkwgBAwLEI6u_1ggaCgoICAESBLLcL0wM&ved=0ahUKEwijmY_u5aHZAhWirVkKHeCRAS0Qwg4IJigA&biw=1280&bih=566

4. Models functions: 
create_user_profile(sender, instance, created, **kwargs)
save_user_profile(sender, instance, **kwargs)
are both cited from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
