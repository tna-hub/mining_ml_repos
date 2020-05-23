a) Downloaded the paper of code files (json)

b) Extracted, through github API, the repositories with python as main language

c) Removed duplicates. Duplicates are projects that have the same github link. These are usually different versions of the paper but still linked to the same github repository.

d) Get the number of commit of each project.

e) Remove the lower quartile to keep only projects with the sufficient amount of commits.
For confidenttiality, researchers somethimes develop thir code out of Github or in a private Repository, then once the paper is published, they then pull all the code into one or few commits to Github.
This removes all the medatadata associated to the project evolution and makes the project impossible to mine.
