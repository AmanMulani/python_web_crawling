Webcrawling is the process of scanning through the webpages to get the desired information.
In this python project, we use webcrawling to get all the links present inside the website that we are crawling.
We do not go to the websites which are outside the domain.
Once we get the urls from the targetted website, then we find the page rank of all the pages which are linked to
that website.

The backend is written in Python3. I have used sqlite to as a database to store the url, and BeautifulSoup is used
to extract the links from the website.

The visualization part is done using html, css and javascript. The d3.js library is used for visualization.

How to run:
1. Open the terminal and run the spider.py file.
2. Run the sprank.py file
3. To see the data stored in the database on terminal you can run the spider_terminal_output.py file
4. Now we have to convert the data stored in our database to json format so that we can feed it to our javascript program,
   to do this, run the spider_json.py file
5. Now open the force.html file to see the visualization.
