import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import math
import webbrowser





min_rating = 1000
init_rating = 1000
participants_data = {}
event_weights = {}

def load_data():    

    participants_file = pd.read_csv('Participant_details.csv')
    for index, row in participants_file.iterrows():
        participant_number = row['Participant Number']
        events_participated = eval(row['Events Participated']) #"[1,2,3]" to [1,2,3]
        participants_data[participant_number] = {
             'events_participated': events_participated,
             'current_rating': init_rating,
             'consecutive_misses': 0,
             'events_completed': 0
         }
        
    events_file = pd.read_csv('event_weights.csv')
    for index, row in events_file.iterrows():
         event_number = row['Event Number']
         event_weights[event_number] = {
            'weight': row['Event Weightage'],
              'difficulty': row['Event Difficulty']
         }

def open_documentation():
    webbrowser.open("https://github.com/samarthbanodia/WNCC-ASSIGNMENT-Q1/tree/main")

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/in/sm4th/")
    

def expected_performance(rating, difficulty):

    if difficulty == 1  : Rmid = 1400
    elif difficulty == 2 : Rmid = 1500
    else: Rmid = 1600
    
    expected = 6 * (1 / (1 + math.pow(10,((Rmid - rating)/400))))
    return round(expected, 5) #5 decimals

def generate_problems_solved(rating):


    rating = min(min_rating, rating) #keeps the lower bound
    
    possible_problems = range(1, 7) # 6 problems
    
    if rating <= 1300:  
        weights = [0.42, 0.28, 0.12, 0.10, 0.03, 0.05]
    elif rating <= 1500:  
        weights = [0.10, 0.22, 0.36, 0.22, 0.05, 0.05]
    elif rating <= 1800:  
        weights = [0.02, 0.10, 0.15, 0.30, 0.30, 0.13]
    else:  
        weights = [0.01, 0.04, 0.10, 0.10, 0.30, 0.45]
    
    return random.choices(possible_problems, weights=weights, k=1)[0] 


def update_rating(participant_number, event_number):

    if event_number not in participants_data[participant_number]['events_participated']:
        return {"participated": False} #skip participant who havent taken part in this event
    
    old_rating = participants_data[participant_number]['current_rating']
    event_weight = event_weights[event_number]['weight']
    event_difficulty = event_weights[event_number]['difficulty']
    
    expected = expected_performance(old_rating, event_difficulty)
    actual = generate_problems_solved(old_rating)
    
    K = 40  #learning rate
    beta = 0.9  #momentum coeff 
   
    delta = actual - expected #differnec in actual vs expected
    
    events_completed = participants_data[participant_number]['events_completed']
    uncertainty_factor = 2.2 if events_completed < 3 else 1.0 #uncertainty factor so that players who have played less games their rating change *unc factor times
    
    if 'velocity' not in participants_data[participant_number]: #velocity parameter for each participant - measure of rate of change of rating
        participants_data[participant_number]['velocity'] = 0
    
    
    velocity = beta * participants_data[participant_number]['velocity'] + delta * event_weight * uncertainty_factor #update vel factor
    participants_data[participant_number]['velocity'] = velocity
    
    rating_change = K * velocity #calc rating change
    new_rating = max(min_rating, old_rating + rating_change)
    
    #update data
    participants_data[participant_number]['current_rating'] = new_rating
    participants_data[participant_number]['events_completed'] += 1
    participants_data[participant_number]['consecutive_misses'] = 0
    
    


def apply_decay(participant_number, event_number):

    if event_number not in participants_data[participant_number]['events_participated']:
        return {"decay_applied": False}
    
    participants_data[participant_number]['consecutive_misses'] += 1
    consecutive_misses = participants_data[participant_number]['consecutive_misses']
    
    if consecutive_misses >= 2:
        old_rating = participants_data[participant_number]['current_rating']
        
        decay_rate = 0.05 * (consecutive_misses - 1)
        
        decay_amount = old_rating * decay_rate
        new_rating = max(min_rating, old_rating - decay_amount)
        
        participants_data[participant_number]['current_rating'] = new_rating
        


def update_leaderboard():

    for i in leaderboard.get_children(): #delete previous entreies in table
        leaderboard.delete(i)


    
    all_participants = []
    for participant_id in participants_data:
        rating = participants_data[participant_id]['current_rating']
        events = participants_data[participant_id]['events_completed']
        all_participants.append([participant_id, rating, events])
    
    all_participants.sort(key=lambda x: x[1], reverse=True) #sort the table entries in decreasing order
    
    for rank, participant in enumerate(all_participants, 1):
        p_id = participant[0]
        rating = round(participant[1], 1)
        events = participant[2]
        
        leaderboard.insert("", "end", values=(rank, f"P{p_id}",rating,events ))

def run_event():
    if int(event_var.get()) > 10 :
        return 0
    
    else :
         event_number = int(event_var.get())
    
         for participant_number in participants_data:
             if event_number in participants_data[participant_number]['events_participated']:
                 update_rating(participant_number, event_number)
             else:
                 apply_decay(participant_number, event_number)
    
         update_leaderboard() 
    event_var.set(str(min(event_number + 1, 10))) #variable for displaying event on GUI

def main():

    global event_var, leaderboard
    
    root = tk.Tk() #main window
    root.title("Coding Circuit Rating System")
    root.geometry("600x500")
    
    load_data()
    
    main_frame = tk.Frame(root, padx=10, pady=10) #main frame
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    control_frame = tk.Frame(main_frame) #create controll frame inside the main_frame
    control_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(control_frame, text="Event Number:").pack(side=tk.LEFT, padx=5)
    event_var = tk.StringVar(value="1") #showing the evenet number on GUI
    event_label = tk.Label(control_frame, textvariable=event_var, width=3,bd=1)
    event_label.pack(side=tk.LEFT, padx=5)
    
    run_button = tk.Button(control_frame, text="Run Event", command=run_event)
    run_button.pack(side=tk.LEFT, padx=10) #run button
    
    doc_button = tk.Button(control_frame, text="ReadME", command=open_documentation)
    doc_button.pack(side=tk.LEFT, padx=10) #readme button
    
    linkedin_button = tk.Button(control_frame, text="LinkedIn", command=open_linkedin)
    linkedin_button.pack(side=tk.LEFT, padx=10) #linkedin button
    
    lb_frame = tk.Frame(main_frame) #now making the leaderboard frame
    lb_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    tk.Label(lb_frame, text="Leaderboard", font=("Arial", 14)).pack(pady=5)
    
    tree_frame = tk.Frame(lb_frame) #making treeview instance for making tables
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    columns = ("Rank", "Participant", "Rating", "Events Done") #setup colums
    leaderboard = ttk.Treeview(tree_frame, columns=columns, show="headings")
    
    for col in columns:
        leaderboard.heading(col, text=col)
    
    leaderboard.column("Rank", width=50, anchor='center') #setup colums widhts and center them
    leaderboard.column("Participant", width=100, anchor='center')
    leaderboard.column("Rating", width=100, anchor='center')
    leaderboard.column("Events Done", width=100, anchor='center')
    
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=leaderboard.yview)
    leaderboard.configure(yscroll=scrollbar.set) #all the participants werent fitting so i had to a scroll bar
    
    leaderboard.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #pack the scrollbar with the GUI
    
    update_leaderboard()
    
    root.mainloop()



if __name__ == "__main__":
    main()
