# Making Problems

Adding problems requires you to make a new `problem` object and then add it to the `problems` array. 

## Prompt String
Each problem object requires a string, which will contain the prompt for that problem. Make sure to specify limits and ranges of the input that the participant can enter inside this prompt. 

## The function
The next parameter for the problem object is a function that takes in a string as input and returns nothing. The input string is the raw line of input given by the player. Your function must parse it and then print the output to cout.

## Points to keep in mind
1. Make sure every string is a single line, because newlines will split the message into 2 parts and mess the server up. Same applies to the output, make sure that it is a single line. 
2. Validate the input given by the player to make sure its within limits. If the code throws an error (like divide by 0), then the program may crash. 
3. There are some helper functions in the `RC.cpp` like `get_ints()` which you may find helpful.
