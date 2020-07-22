# src/Python

All of the following programs can run on Linux and Windows. Can totally run on MacOs by adding a few lines

## General Case
Use general_lowerbound.py to use Gurobi to generate points only for the case where there are k+1 points in the database where k is the number of points in the output subset.
There are 4 main functions in this program:
  1) lowerbound(k, d, sol_count):
    Parameter: 
       k: the size of the output subset
       d: the number of attributes of each item
       sol_count: the number of solution 
    
    This function receives the three above parameters to write a complete Gurobi program in another python file.
  
  2) graph2d():
    Parameter: None
    
    This function works only with the case of 2D. It reads the terminal log to extract lines that contain the result to rescale and put them in a better form and graph it.
    
  3) graph3d():
    Parameter: None
    
    This function works only with the case of 3D. It reads the terminal log to extract lines that contain the result to rescale and put them in a better form and graph it.
    
  4) verify(k, d, sol_count):
    Parameter: 
       k: the size of the output subset
       d: the number of attributes of each item
       sol_count: the number of solution 

    This functions can be applied to any case of d. It reads the terminal log and calculates each of the division p_{jl}/v_{jl} to verify our conjecture of the worst case.
    
The main function will prompt the user of the value of k, d and sol_count and offers whether the user want the result to be graphed or not. Notice that the graphing function only works with the case where k = 2 or k = 3. With higher dimension, the result can still be found, but graphing is unavailable.

## k+n Case
Use k+n_points_lowerbound.py to use Gurobi to generate points only for the case where there are k+n points in the database where k is the number of points in the output subset and n is an integer greater than 0.
The main function is the execute_gurobi function, while the other smaller functions only support its execution.
There are 6 smaller functions:
  1) ncr(n, r):
    Parameter:
      n: an integer greater than r.
      r: an integer.
    
    This function quickly calculates the value of n choose r.
  
  2) all_pos(k, n):
    Parameter:
      k: the size of the output subset.
      n: an integer (in k+n).
    
    This functions generateall possible configuration of the points in the output subset. Each configuration is the list of points that give the worst regret ratio. The function returns the list of configuration (a 2d list), the list (l1) of integers from 1 to k+n and the 2d list (l2) contains every combination choosing n items from the list l1.
  
  3) getX(p):
    Parameter:
      p: the terminal log in type string.
      
    This function reads the terminal log and get the first value of x from that log and returns it.
    
  4) count_max(l, x):
    Parameter:
      l: the input list.
      x: the value (integer).
    
    This function count the number of times each number appears in a configuration.
  
  5) configuration_count(l):
    Paramter:
      l: a configuration
    
    This function reads through the configuration and update the numbering for each items in that configurations.
    
  6) increment(l, n):
    ParameterL
      l: a list of integers.
      n: the value of in k+n.
    
    This function performs a base n increment by 1 (i.e. base 2: 00 -> 01, base 3: 02 -> 10).
    
the main function:
  execute_gurobi(d, k, n):
    Parameter:
      d: the number of attributes of each item.
      k: the size of output subset.
      n: the number of additional items in the database.
    
    This function considers every configuration and execute the gurobi optimizer for each of these configurations and get the largest value of x among these configurations.
    
The main() function only prompts the user to input the value of k, d and n to execute the execute_gurobi function and return the result.

## KKT Case
Use KKT_general.py to use Gurobi to solve the KKT conditions for the case where the size of the database is k+1 points and k is the size of the output subset.

the kkt(k, d) functions get the input of the integer k and d to write all the constraints in another Python file and execute it to solve the KKT conditions and returns the raw output.

