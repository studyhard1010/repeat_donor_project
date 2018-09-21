# Introduction

Author: Ding

# Problems and Research
For the concept of the n-th percentile, refer to here: https://en.wikipedia.org/wiki/Percentile

In this case, the aggreation distribution of the repeat donors should be discrete rather than continues, which explains why the 30th percentile of (333, 384) is 333 instead of 348.3


# Approaching Steps
the big picture:
    raw_data --> parsing --> filter & aggregation --> update repeat --> calculate n-th percentile --> write to output

1. read from the raw data and parse them line by line 
2. filter out the invalid information and process aggregation
3. update the repetitive donor contribution depends on the situation
4. calculate the n-th percentile
5. write to the output

# Libraraies and Dependencies 
Only includes built-in packages in this project:
sys: for reading file path
time: for timestring validation
math: for calculation

# Complexity 
Assume the length of the transcations is N. The time complexity is O(N^2) in total, mainly for reading the repetitive transcations, which takes O(N) and mainting an incresing array, which takes O(N) in each insertion. 

However, if the n-th percentile is based on a continues distribution, for example, percentile(333, 384) == 348.3, the approachment can even be optimized to O(NLogN). In that case, we can maintain a max heap and a min heap ( O(LogN) ) seperately storing the min/max value when reading each transcation (N)

# Key Points
1. use a dictionary to de-dupliciate/update the repetitive donor
2. use a list to memorize the output sequence
3. replace an unnecessary sort ( O(NLogN) ) with a list insertion function ( O(N) ) when accumulate the repeat donation amount for calculating the n-th percentile 


# Compile Instruction
To build and debug: 
repeat_donor_project~$ ./run.sh

To run test cases:
insight_donor_project~$ ./run_tests.sh

# Test Design
test_1 and test_2 are fetched directly from the prompt

test_invalid_amount: the TRANSACTION_AMT column from the input is not digit

test_invalid_cmte_id: the CMTE_ID column is empty

test_invalid_date: the datetime string is too long or too short

test_invalud_zipcode: the zipcode is less than 5 digits

test_more_repeated_donors: have more than 3 repeat donors, who are in a messy order

test_different_percentile: the percentile input is different from the given test cases
