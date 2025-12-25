#!/usr/bin/env python
import os 
import warnings

from crewai import Crew, Process
from engineering_team2.crew import EngineeringTeam2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple account management system for a trading simulation platform.
The system should allow users to create an account, deposit funds, and withdraw funds.
The system should allow users to record that they have bought or sold shares, providing a quantity.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
The system should be able to report the holdings of the user at any point in time.
The system should be able to report the profit or loss of the user at any point in time.
The system should be able to list the transactions that the user has made over time.
The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
 from buying more shares than they can afford, or selling shares that they don't have.
 The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
"""
module_name = "accounts.py"
class_name = "Account"

def run():
    """
    Run the crew with interactive feedback loop.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name, 
        'class_name': class_name,
    }

    try:
        # Initialize crew to get agents and tasks
        crew_base = EngineeringTeam2()
        
        # Get the agents and tasks by name (more reliable than indices)
        secretary_agent = crew_base.secretary_note_taker()
        frontend_agent = crew_base.frontend_engineer()
        note_task = crew_base.note_taking_task()
        refined_note_task = crew_base.refined_note_taking_task()
        executer_task_obj = crew_base.executer_task()
        
        # Stage 1: Run note-taking task
        print("\n" + "="*60)
        print("=== STAGE 1: Note Taking ===")
        print("="*60 + "\n")
        
        note_taking_crew = Crew(
            agents=[secretary_agent],
            tasks=[note_task],
            process=Process.sequential,
            verbose=True,
        )
        
        note_result = note_taking_crew.kickoff(inputs=inputs)
        
        # Interactive feedback loop
        max_iterations = 5
        iteration = 0
        user_feedback = ""
        notes_file = 'output/note.md'
        refined_notes_file = 'output/refined_note.md'
        
        while iteration < max_iterations:
            # Read the current notes file
            current_notes_file = refined_notes_file if iteration > 0 and os.path.exists(refined_notes_file) else notes_file
            
            if os.path.exists(current_notes_file):
                with open(current_notes_file, 'r', encoding='utf-8') as f:
                    notes_content = f.read()
                
                print("\n" + "="*60)
                print("EXTRACTED NOTES:")
                print("="*60)
                print(notes_content)
                print("="*60)
            
            # Get user feedback
            print("\n" + "="*60)
            if iteration == 0:
                user_feedback = input("\nReview the notes above. Provide feedback or changes (press Enter if good enough): ").strip()
            else:
                user_feedback = input("\nReview the refined notes above. Provide more feedback or changes (press Enter if good enough): ").strip()
            print("="*60 + "\n")
            
            # If no feedback, break the loop
            if not user_feedback:
                print("Notes approved! Proceeding to frontend creation...\n")
                break
            
            # Stage 2: Refine notes with feedback
            iteration += 1
            inputs['user_feedback'] = user_feedback
            
            print(f"\n=== STAGE 2.{iteration}: Refining Notes Based on Your Feedback ===\n")
            
            refined_crew = Crew(
                agents=[secretary_agent],
                tasks=[refined_note_task],
                process=Process.sequential,
                verbose=True,
            )
            
            refined_result = refined_crew.kickoff(inputs=inputs)
        
        if iteration >= max_iterations:
            print(f"\nReached maximum iterations ({max_iterations}). Using latest notes.\n")
        
        # Stage 3: Run the execution task with frontend engineer
        # Read the final notes and pass them to the executer task
        final_notes_file = refined_notes_file if os.path.exists(refined_notes_file) else notes_file
        
        if os.path.exists(final_notes_file):
            with open(final_notes_file, 'r', encoding='utf-8') as f:
                final_notes_content = f.read()
            inputs['refined_notes'] = final_notes_content
        else:
            # Fallback: use requirements if notes file doesn't exist
            inputs['refined_notes'] = inputs.get('requirements', 'No notes available')
        
        print("\n" + "="*60)
        print("=== STAGE 3: Creating Frontend UI ===")
        print("="*60 + "\n")
        
        # Create crew with just the executer task - it will receive notes via inputs
        executer_crew = Crew(
            agents=[frontend_agent],
            tasks=[executer_task_obj],
            process=Process.sequential,
            verbose=True,
        )
        
        final_result = executer_crew.kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("=== FINAL RESULT ===")
        print("="*60 + "\n")
        print(final_result.raw)
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

