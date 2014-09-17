============
Price Search
============

Overview
========

Price Search is a program to automate the process of identifying items at
a reduced price at the supermarket. It uses Scrapy to crawl the 
`mySupermarket`_ "Savvy Buys" pages, then does a bulk search for items that 
match the list provided.

Why?
====

With the rise of internet shopping, and in particular the supermarket 
comparison site `mySupermarket`_, it should be trivial to figure out the 
cheapest place to shop. `mySupermarket`_ automatically keeps track of the
total cost of a trolley of goods in each of the main UK supermarkets, and 
allows you to choose the cheapest at the end. 

The problem is that starting with a fixed shopping list and then working out 
the cheapest way to get it is a poor approximation of the way I actually shop.

My process is almost exactly the reverse of that promoted by `mySupermarket`_. 
I identify what's cheap/in season **first**, and only then plan meals and write
a shopping list. Also, the vast majority of my shopping is made up of things 
that I can easily store for a while (such as tinned tomatoes, teabags, pasta, 
rice, oils, spices, nappies, meat for the freezer, laundry detergent and 
bathroom products). That means that there are very few things I need to buy in 
any particular week; the things I choose to buy based on their current price 
and/or seasonality make up the majority of my shopping. 

`mySupermarket`_ does provide the necessary data for this (in the form of 
"Savvy Buys" pages) but not the interface to go with it. The only way to 
identify good value items is to sift through them manually. This is 
time-consuming and tedious, so I decided to automate it.

Requirements
============
* `Python`_ version 2.7
* The `Scrapy`_ library
* All `Scrapy`_'s dependencies. These are OS-specific and are listed `here`_. 

Running
=======
The program can be run from the command prompt/ shell with 
    python main.py <filename>

where <filename> is the name of the input file containing items to search.

For example
    python main.py search.txt

Input file format
=================
Items are separated by line. Multiple words on a line should be separated by
spaces. All words on the line must appear in the item title for a match to be
found. There is a sample input file provided, search_example.txt.

.. _mySupermarket: http://www.mysupermarket.co.uk/
.. _Python: http://www.python.org/
.. _Scrapy: http://scrapy.org/
.. _here: http://doc.scrapy.org/en/latest/intro/install.html#platform-specific-installation-notes


