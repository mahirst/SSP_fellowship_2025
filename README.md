# Data for: Revenue, Region, and Racial Demographics: A study of college publishing programs and presses over time
Data, methods, scripts, and results from my 2025 SSP Early Career Fellowship project

Quantitative study: Molly A. Hirst, PhD

Qualitative study: Mikayla Lee (not posted here)

## Disclaimers
TLDR: don't come for me lol 

This GitHub repo was created for a simple project I did for the Society of Scholarly Publishing 2025 Early Career Fellowship. This project is not exclusive- I left out a lot of potentially important variables for the sake of simplicity and velocity. I also accidentally deleted my fuzzy matching script and did not feel like re-creating it, so there's that. Any results from this project should be thoroughly scrutinized for accuracy and should not be taken as fact.

The randomized list of college names was generated using AI. The scripts were written with the help of AI when I got stuck or for troubleshooting purposes.

## Abstract

Despite recent efforts to make publishing resources more financially accessible and racially inclusive, it remains unclear how university revenue correlates with the availability of publishing programs and presses over time. This research investigates the impact of recent political and economic trends on college presses at both Northern and Southern colleges, discussing how these trends have affected the representation of Black scholars and their work in scholarly publishing. We will collect revenue and other publicly available data from approximately 200 U.S. institutions from 2012 onward and perform a linear regression model to determine if there is a correlation between the presence/absence of publishing programs with institution revenue and other variables. We will then focus our attention on some case studies, including HBCUs, Tribal Colleges, and Hispanic-serving Institutions, to explore how having publishing programs in these types of institutions may affect the representation of BIPOC scholars in academic publishing.

## Description of the data and file structure

These files and folders are divided into whether they are input and output files, as well as scripts. Any empty cells indicate that the data could not be collected, usually because it does not exist.

1 file: 

* Publishing_programs_univs_data - Sheet1.csv - the unformatted data file used for analysis (after transformation; see below)

3 main folders:

* Revenue
* map_figure
* analysis

### 'Revenue' folder

#### 'Revenue' folder input

##### file: hd2022.csv 

The latest IPEDS directory dataset (as of March 2025). This is an unaltered public domain file, and you can find a data dictionary for the column names on their website (info at the end of the README). There are far too many for any sane human to list here.

##### folder: IPEDS_Finance

IPEDS financial data collected from the Data Center. There are 3-4 zipped folders per year. For each year, there is a zip file containing CSVs like the following:

F1A.csv — Finance data for public and private institutions

F1B.csv, F2.csv, etc. — Other finance forms (community colleges, etc.)

These are unaltered public domain files, and you can find a data dictionary for the column names on their website (info at the end of the README). There are far too many for any sane human to list here.

##### file: colleges_list.csv

A simple list of college names, with the single variable header "Institution_names"

##### colleges\_matched\_fresh\_with_fuzzy.csv

I accidentally deleted the script for this, but if you've gotten this far, you probably know how to write one, so you can do it. I believe in you! The script just helped match college names and unitids from IPEDS. All but 9 matched either exactly or via fuzzy matching.

##### missing\_colleges.csv 
This was created because 9 of the college names did not match those used by IPEDS, and fuzzy matching didn't work because there are multiple campuses, or the college names were just too different. I manually fixed these and then ran the "missing" scripts to get the unitids and other information. Anything with "missing" in the header is just for these unmatched unitids. 

##### missing\_colleges\_with\_verified\_metadata.csv
Generated all the info needed to run the missing.py script for the unmatched colleges.

##### ef2022a_rv.csv and ef2012a_rv.csv 

IPEDS input files for figuring out the top 3 reported demographics per institution, plus the reported student population size. 

#### 'Revenue' folder scripts

##### extract\_ipeds\_revenue.py

The first script to run to extract IPEDS total revenue data per named unitid

##### missing.py

Some college names did not match those in IPEDS, so this was just made for the small list of unmatched colleges

##### summarize\_revenue.py

This script summarizes all the total revenue data from the IPEDS financial datasets into a clear, concise format

##### pop_demogs.py

This script uses the files "ef2012a_rv.csv" and "ef2022a_rv.csv" to generate the files called "institution_top_demographics_2012.csv" and "institution_top_demographics_2022.csv". 

#### 'Revenue' folder output

##### college\_financial\_data\_out.csv
The first output file, generated from the script extract\_ipeds_revenue.py. Notice that it contains the unitids and then a bunch of stuff I don't need. I revised it to just get the total revenue using the script summarize\_revenue.py, which generated...

##### college\_total\_revenue\_summary.csv
This contains the college_name with each row being a college, and then columns B-L are years. Each value is the total revenue for that college per year. Note that the year is the fiscal year. Year 2024 will be released on IPEDS in January 2026.

##### missing\_colleges\_revenue_summary.csv
Contains all the total revenue info for the colleges that didn't match exactly or via fuzzy matching. 

##### Final csv file: Publishing\_programs\_univs_data.csv
This file is the final file that I compiled to run statistical analyses.

* **university:** college name generated with the help of ChatGPT
* **type\_1 and type\_2:** the type of college. Some colleges have multiple types that are not listed here. These can be public, private, liberal arts, HBCU (Historically Black Colleges and Universities), HSI (Hispanic-Serving Institution), Women's College, R1, R2, R3, TCU (Tribal Colleges and Universities).
* **region:** the region of the US where the institution is located
* **publishing\_program:** whether or not the institution has a publishing program. 1 = yes, 0 = no. These data were collected manually using Google searches
* **press:** whether or not the institution has a press. 1 = yes, 0 = no. These data were collected manually using Google searches
* **student\_pop\_size\_most\_recent\_average:** most recent average student population size
* **demogs\_1-3:** highest reported demographics for that institution
* **YYYY_revenue:** Reported total revenue for that fiscal year

* Note: The University of North Georgia did not exist in 2012, so that data is missing from this file.

##### institution_top_demographics_2012.csv

The top 3 demographics reported by institutions in 2012, as well as the total number of students reported.

##### institution_top_demographics_2022.csv 

The top 3 demographics reported by institutions in 2022, as well as the total number of students reported.

### 'map_figure' folder

#### 'map_figure' folder input

##### complete\_university\_coordinates.csv
coordinates for all institutions for statistical analysis

#####  institution_coordinates.csv
coordinates for the Michigan case study institutions- note that the scripts fail for these. I scrapped this part of the project, but maybe YOU have time to troubleshoot this part of the project!

Both have 3 columns: Institution_Name, Latitude, and Longitude. Lat/Long corresponds to each institution per row.

#### 'map_figure' folder scripts

##### SSP_maps.R
R script used to generate base maps for both CSV files above. 

##### Image_Resolution_editing.R
The R script that I have used for years to help increase the image resolution of JPG outputs from R 

#### 'map_figure' folder output

##### us.jpeg
map of North America showing locations of institutions (blue dots) 

##### mi.jpeg
Michigan map showing locations of institutions (blue dots)


### 'analysis' folder

#### 'analysis' folder input

**Publishing_programs_univs_data - Sheet1.csv**

A copy of the **Publishing_programs_univs_data - Sheet1.csv** file in the main folder.

**Reshaped_University_Revenue_Data.csv**

This is the CSV file that will be read into the following script. It contains all of the information from the original data file named **Publishing_programs_univs_data - Sheet1.csv** but is reshaped to long format to analyze revenue over time (allowing the linear mixed model to work properly).

#### 'analysis' folder script

**LMM_correlations_analysis.R**

R script to run linear mixed models and output figures (forest plots), which were then made pretty in PowerPoint

#### 'analysis' folder output

**sig_fixed_effects.jpeg**

Forest plot showing only the significant effects from the revenue over time model

**sig_revenue_predictors.jpeg**

Forest plot of significant predictors for cross-year (2012 vs 2022) revenue analysis

## Methods

##### Randomized college list generation
I asked ChatGPT 4o for a randomized list of 200 U.S. colleges because ain't nobody got time to generate that. Here's my exact prompt: provide a randomized list of ~198 US universities/colleges of all types (e.g., R1, HBCU, tribal, liberal arts, etc.) and make it so that when I copy and paste it into google sheets, it will list each university/college in it's own row. Do not include the University of Michigan or Howard University. UM and HU were excluded because we already chose those to include as an example when I was showing Mikayla how we would format the data file (Publishing\_programs\_univs\_data.csv). 

I had to fight with ChatGPT for a while to make it include things like the type of college, and to make sure it was actually generating 200 colleges. I also thoroughly questioned its confidence in its answers and made it generate a confidence interval for every single entry to ensure it was confident enough (>95%) about college type, and it was not happy with me. You do not have to replicate this, unless you also want to fight with ChatGPT.

##### Download IPEDS data
I downloaded public domain data from IPEDS Data Center, selecting years of interest and "Finance". I downloaded all of the files for each year, including F1A, F2, F3, and FLAGS datasets. 

1. Go to the IPEDS Data Center Download Page at https://nces.ed.gov/ipeds/datacenter/ 

2. In the “Survey Component” dropdown, choose: Finance

3. Then select the year (e.g., 2021–22). Click “Continue.”

4. Under "File Names and Descriptions": Look for the ZIP file that includes F1A (e.g., F2122_F1A.zip) and click to download

5. Repeat for all years from 2012–13 through 2022–23

##### Match institution name with unitid

I didn't want to manually locate the information from all these files, and there's so much information that I simply don't understand as a biologist short on time, so I wrote some simple Python scripts to scrape that info for me. First, you'll need to download the latest IPEDS directory dataset to match college names to their official IPEDS unitids. This is the file hd2022.csv. This can be downloaded from the Data Center. 

Once you have the IPEDS directory dataset, the other data files, and your list of colleges, you can run the scripts above to generate the output files and run analyses. 

##### Availability of a publishing program or press

These data are subjective (i.e., what defines a publishing program or press?) and were generated manually by my fellowship partner by doing simple Google searches for each institution. 1 means a program or press exists at that institution currently; 0 means they do not.

##### Running the scripts

In the **Revenue** folder, you can start by running extract_ipeds_revenue.py and then missing.py. Then, run the summarize_revenue.py to get the college_total_revenue_summary.csv file. 

Population demographics analysis for 2012 vs 2022 can be run using the pop_demogs.py file.

In the **analysis** folder, there is only one R script called "LMM_correlations_analysis.R". This will run the linear mixed models to look for correlations between the variables included, and it will generate the resulting forest plots that are in the **analysis** folder.

## Sharing/access information

Python version 3.13.2
R version 2024.12.1+563 (2024.12.1+563)

This project has an MIT license. Please read the license file. 

IPEDS data is public domain and can be downloaded from their Data Center.

The unaltered IPEDS data included here were downloaded on 27 March 2025. Please go to the IPEDS website for a more up-to-date version of these documents. https://nces.ed.gov/ipeds/use-the-data

Data source: U.S. Department of Education, National Center for Education Statistics, Integrated Postsecondary Education Data System (IPEDS), [2025].
