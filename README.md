# CourseProject  
# Automatic Crawler of Faculty Pages  

Tool is live on this URL: https://sxxgrc.github.io/faculty-scraper/  

Directory structure  

&nbsp;&nbsp;&nbsp;&nbsp;faculty_scraper_ui.py >> flask client for GUI  
&nbsp;&nbsp;&nbsp;&nbsp;cli.py >> command line utility to use the faculty scraper  
&nbsp;&nbsp;&nbsp;&nbsp;globals.py >> common python definitions  
&nbsp;&nbsp;&nbsp;&nbsp;README.md  
&nbsp;&nbsp;&nbsp;&nbsp;+---data  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;finalized_model.sav >> svm model data  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;output.zip >> output example  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TrainingDataSetTest.csv  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TrainingTestingDataSet.csv  
&nbsp;&nbsp;&nbsp;&nbsp;+---output >> csv files will be generated here, one for positive cases, another for all URLs tested  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.gitignore  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;README.md  
&nbsp;&nbsp;&nbsp;&nbsp;+---doc  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Automatic crawler of faculty pages - Project Proposal.pdf  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ProgressReport.pdf  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FinalReport.pdf  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;UsageDemo.mp4  
&nbsp;&nbsp;&nbsp;&nbsp;+---spiderbot  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scrapy_spider.py  
&nbsp;&nbsp;&nbsp;&nbsp;+---ui >> web content for GUI such as JS, html and css  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---public  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---src  
&nbsp;&nbsp;&nbsp;&nbsp;faculty_scraper.js >> Main search page for UI, handles accessing the flask client and polling  
&nbsp;&nbsp;&nbsp;&nbsp;results.js >> Main results page which displays the JSON result from the Flask client  
&nbsp;&nbsp;&nbsp;&nbsp;+---urlclassification  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;url_classification.py >> model training and classification  
