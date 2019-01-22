Scripts:
--------

- This scripts were used to find results about experts evolution in StackOverflow using the mean expert contribution (M.E.C),
two sets of scripts where prepared, the first one using Golang to read XML dumps from StackOverflow post and divide them into smaller XML with the Post of interest for this study (Those with Angular, Ember, React and VUE questions and answers). The other set of scripts are for M.E.C
algorithm and retention rate calculation.  

Extraction of Information:
--------------------------
1) Download an XML Dump from StackOverflow
2) Extract the Questions/Answers of Interest (See folders: post_answer_extraction, post_extraction)  
3) This will create XML Files that could be read by the MEC calculator (See Running MEC)

Running MEC
------------
1) Under the folder Analysis running the script user_mec.py calculates the MEC
2) POLI_OWLS calculate the number of experts obtained from (1) using more than 1 technology.
3) Trendings.py a general script to generate trendings using python.
4) trendings_retention_owls.py am a script to find the retention rate. 





