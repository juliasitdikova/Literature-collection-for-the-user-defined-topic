# Homework-Mazars
the link for the video ( run of the code): https://www.loom.com/share/1590ee34787b4d19b41ef70dc8c38d47
The robot is used to automate the process of https://www.semanticscholar.org/ literature collection for the user-defined topic. Result of the process is an email with attached excel with info about each found article.

Used libraries
selenium - web-browser
automation pandas - work with datatables
smtplib \ email - email creating and sending
wcm - function for working with Windows credential manager 

Algorithm 
1. User defines a topic, number of pages, and receiver of the resulting email 
2. Robot creates links for each search results page 
3. Robot collects links to the articles from each page 
4. Robot scraps article's info and downloads source docs if available 
5. Robot writes all info to excel and sends email 
How to use
1. Clone git repository to your computer 
2. Create a virtual environment (optional) 
3. Install packages from requirements.txt 
4. Make setup correcting conf.py file 
5. Run script articles_search.py
