# Mining machine learning repositories


This project aims to mining github machine learning repositories in order to understand how they deal with datasets. It is part of of a bigger project having three reseach questions:

  - RQ1: What are the main libraries used in these projects?
  - RQ2: How  do developers deal  with  datasets  in  ML projects?
  - RQ3: How  do ML projects evolve?

For now, we focus only on the second research question, as the first one have already been assessed.

# Dataset
We analysed repositories from the Paper Of Code project which put together machine learning research papers with their corresponding github repository. We then filtered it to get only repos writen in python language.

# Method
Our hypothesis is that dataset are stored as files in the project to allow them to be tracked by Git.
We developed some heuristics to identify dataset:
  1) directory name: Any directory name matching the String ``` data*``` is considered as storing data files.
  2) File name is loaded in the code: Using python ast, we checked for any mention of a project's non-code filename in the code of the repo. To do this, we had to split repo files into code and non-code files using filenames and extensions.


We downloaded the latest version of each repository from github, then all