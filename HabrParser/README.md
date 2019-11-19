Habr parses
=====================
Displays the most used nouns in articles located on n pages of Habr.

![Описание проекта](http://picua.org/img/2017-04/27/5i4u3amhjov9hkmcy0knrgfco.jpg)

Install
-----------------------------------
git clone https://github.com/komodikus/PythonParsers/tree/master/HabrParser

Как использовать
-----------------------------------
![чето_там](http://s8.favim.com/orig/141228/gif-puppy-Favim.com-2342718.gif)
1) Run parsing_habr.py 
2) Input count parsing pages
3) ???
4) Profit

Or

1) Run with param (python parsing_habr.py 20 - 20 num of pages.)
3) ???
4) Profit

How to put downloaded data into a database
-----------------------------------
If you need to put the downloaded data into the database, then:
1) Uncomment the class
2) Uncomment the create_db_item function
3) Uncomment the import of the peewee package
4) Uncomment all commented values ​​in the main function

Dependencies
-----------------------------------
* Python 3+
* pymorphy2
* isoweek
* peewee
* bs4

Usage example
-----------------------------------
```

python parsing_habr.py
```


Enter the number of parsing pages

> 2

Output:

```
Неделя с 2018-04-23 по 2018-04-29
1)('лифт', 228)
2)('система', 172)
3)('ключ', 123)
```


Thanks for reading!
-----------------------------------





