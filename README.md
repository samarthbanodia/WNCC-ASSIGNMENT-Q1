
#### My Approach ::: 
this assignment seemed straightforward so i planned out the different functions and variables i need so the code is easy to read. Also i made a GUI for this part as i wanted it to be interesting - i used tkinter for windows, tables and button - i knew tkinter existed from school so just had to brush up the methods and tables. I made a dictionary for each participant which contains every detail so its easy to implement to understand -  events participated , current-rating, consecutive misses(for decay), events completed and similar for events as well.


#### Libraries i used , 
![[Pasted image 20250410194104.png]]

ttk is treeView module of tkinter it helps in making tables ; pandas for reading csv files , math for writing formulas and webbrowser for opening the broswer when "ReadMe" or "Linkedin" Button is pressed.





![[Pasted image 20250410194802.png]]
defining variables



![[Pasted image 20250410195849.png]]
loading data from the csv files with pandas and initialising the participant and events dictionary.




![[Pasted image 20250410195949.png]]
expected_performance -  calculates the expected number of problems solved for a given rating and event difficulty using the given formula.

generate_problems_solved - randomly generated the actual problems solved with bias to rating of the participant . I used choices method of the random library to put on bias.




Rating Update Logic:
taking inspiration from machine learning , i remembered how optimizers techniques like Schhochtic gradient descent , SGD + momentum , Adam update the their position on the loss function based on the previous data. Similarly i applied a logic similar to SGD + momemtum to update the rating




![[Pasted image 20250410200922.png]]

![[Pasted image 20250410201005.png]]
define the error delta as the difference between actual and expected. We define a learning rate and a momentum coefficient which scales the velocity . 

Uncertainity_factor stays 1 for participants who have completed 3 or more events and stays 2.2 if less. this helps newer players to gain more rating significantly faster.


![[Pasted image 20250410201241.png]]

First we add a velocity parameter to the participants data , it keeps track of rate of change of rating of the participant.


![[Pasted image 20250410201344.png]]
https://www.youtube.com/watch?v=NE88eqLngkg

Here the for the change of rating i have taken a factor of learning_rate - to scale values

Velocity is calculated by the formula shown in the video , gradient is taken as the delta and uncertainity factor is also multiplied.

![[Pasted image 20250410202341.png]]


The Decay formula is fairly simple - if a partcipant misses >=2 events consecutively they get a decay of decay_amount for every consecutive missed event.


![[Pasted image 20250410202436.png]]
updating the leaderboard - sorting the enteries after each event and updating the entries in table . 

I have explained the code for tkinter window in the comments itself, take a look.
