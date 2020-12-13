# CourseProject
# Automatic Crawler of Faculty Pages

Tool is live on this URL: https://sxxgrc.github.io/faculty-scraper/ 

Directory structure
|   faculty_scraper_ui.py >> flask client for GUI 
|   cli.py >> command line utility to use the faculty scraper 
|   globals.py >> common python definitions 
|   README.md 
|    
+---data 
|   |   finalized_model.sav >> svm model data 
|   |   output.zip >> output example 
|   |   TrainingDataSetTest.csv 
|   |   TrainingTestingDataSet.csv 
|   |    
|   \---output >> csv files will be generated here, one for positive cases, another for all URLs tested 
|           .gitignore 
|           README.md 
|            
+---doc 
|       Automatic crawler of faculty pages - Project Proposal.pdf 
|       ProgressReport.pdf 
|       FinalReport.pdf 
|       UsageDemo.mp4 
+---spiderbot 
|   |   scrapy_spider.py 
|   |    
+---ui >> web content for GUI such as JS, html and css 
|   +---public 
|   \---src 
|           faculty_scraper.js >> Main search page for UI, handles accessing the flask client and polling 
|           results.js >> Main results page which displays the JSON result from the Flask client 
+---urlclassification 
|   |   url_classification.py >> model training and classification 
