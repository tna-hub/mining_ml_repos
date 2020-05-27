# Mining machine learning repositories


This project aims to mining github machine learning repositories in order to understand how they deal with datasets. It is part of of a bigger project having three reseach questions:

  - RQ1: What are the main libraries used in these projects?
  - RQ2: How  do developers deal  with  datasets  in  ML projects?
  - RQ3: How  do ML projects evolve?

For now, we focus only on the second and third research question, as the first one have already been assessed.

# Dataset
We analysed repositories from the Paper Of Code project which put together machine learning research papers with their corresponding github repository. We then filtered it to get only repos writen in python language.

a) Downloaded the paper of code files (json)

b) Extracted, through github API, the repositories with python as main language

c) Removed duplicates. Duplicates are projects that have the same github link. These are usually different versions of the paper but still linked to the same github repository.

d) Get the number of commit of each project.

e) Remove projects with less than 30 commits to keep only projects with the sufficient amount of commits.
For confidenttiality, researchers somethimes develop their code out of Github or in a private Repository, then once the paper is published, they then pull all the code into one or few commits to Github.
This removes all the medatadata associated to the project evolution and makes the project impossible to mine.


# Method
Given the fact that there are several ways to store data and that GitHub keeps tracks of changes in the project through files, we study how datafiles  are stored as and how they can impact the evolution of the repository.

## RQ2
We developed some heuristics to identify dataset:
  1) directory name: Any directory name containing the String ``` *data*``` and whose name is mentioned in the code is considered as storing data files.
  2) Using a simple text find tool, like ``` grep ``` find all mentions of data or non-code files in code files. Ignore starndard files like README.md, setyp.py, requirements.txt.
  3) Non code file name is loaded in the code: Using python ast, we checked how non-code files are used in the identified code files from the previous step. 
  
  It may be interesting to find out if the data is mentioned as input or output dataset by using the function calling it. But due to the disparity and the huge number of possibilities to use data (custom function, function open(), library function), this is a hard task that will need time to identify at an interesting number of possibilities that won't bias the results.
  
  ## RQ3
  the third rq is to assess how the datafiles and the code evolve together.
For that, for each identified datafile (a file from the repo is identified as datafile according to the heuristics of the rq2), we checked all the commits modifying that file (C). We then looked at how many time a file appears in the commits. Let's say the file "data.csv" has been modified n=10 times (there are ten commits where that file appears). for each commit C[i] in C, we checked all the files modified by that commit. Let's call C[n][j] the jth file of the commit commit C[i]. then we check the presence of C[i][j] in all the commits (from 0 to 10) and count how many times we found that file.

(Not yet done) Need to use a mathematical method combining the number of commits and the occurence of the file in the commits to asses what is the treshold from wich a file is correlated to another file in its evolution. Also may be interesting to check if  the reverse is true (if a correlated to b implies b is correlated to a)

