#!/usr/bin/env python3
"""
Ham Radio Flashcard Viewer
Displays questions and answers from general.csv and extra.csv
Press Space or → to advance, ← to go back, Esc to quit
"""

import tkinter as tk
import csv
import sys
import os

class FlashcardViewer:
    def __init__(self, root, general_file, extra_file):
        self.root = root
        self.root.title("Ham Radio Flashcard Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        
        # Load question pools
        print("Loading question pools...")
        self.load_questions(general_file, extra_file)
        
        # Current question index
        self.current_index = 0
        
        # Create UI
        self.create_widgets()
        
        # Display first question
        self.display_question()
        
        # Keyboard bindings
        self.root.bind('<space>', lambda e: self.next_question())
        self.root.bind('<Right>', lambda e: self.next_question())
        self.root.bind('<Left>', lambda e: self.previous_question())
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    def load_questions(self, general_file, extra_file):
        """Load questions from CSV files"""
        try:
            self.questions = []
            
            # Load General questions  # Comment out when working with only Amateur Extra questions
            print(f"Reading {general_file}...")  # Comment out when working with only Amateur Extra questions
            with open(general_file, 'r', encoding='utf-8-sig') as f:  # Comment out when working with only Amateur Extra questions
                reader = csv.DictReader(f)  # Comment out when working with only Amateur Extra questions
                
                # Debug: Show what columns we found  # Comment out when working with only Amateur Extra questions
                if reader.fieldnames:  # Comment out when working with only Amateur Extra questions
                    print(f"  Columns found: {reader.fieldnames}")  # Comment out when working with only Amateur Extra questions
                
                for row in reader:  # Comment out when working with only Amateur Extra questions
                    # Handle different possible column names  # Comment out when working with only Amateur Extra questions
                    question_id = row.get('id') or row.get('ID') or row.get('Id') or ''  # Comment out when working with only Amateur Extra questions
                    question_text = row.get('question') or row.get('Question') or ''  # Comment out when working with only Amateur Extra questions
                    correct_answer = (row.get('Correct Answer') or   # Comment out when working with only Amateur Extra questions
                                    row.get('correct') or   # Comment out when working with only Amateur Extra questions
                                    row.get('answer') or   # Comment out when working with only Amateur Extra questions
                                    row.get('Answer') or '')  # Comment out when working with only Amateur Extra questions
                    
                    if question_id and question_text and correct_answer:  # Comment out when working with only Amateur Extra questions
                        self.questions.append({  # Comment out when working with only Amateur Extra questions
                            'id': question_id.strip(),  # Comment out when working with only Amateur Extra questions
                            'question': question_text.strip(),  # Comment out when working with only Amateur Extra questions
                            'answer': correct_answer.strip(),  # Comment out when working with only Amateur Extra questions
                            'pool': 'General'  # Comment out when working with only Amateur Extra questions
                        })  # Comment out when working with only Amateur Extra questions
            
            general_count = len(self.questions)  # Comment out when working with only Amateur Extra questions
            print(f"✓ Loaded {general_count} General questions")  # Comment out when working with only Amateur Extra questions
            
            # # Load Extra questions  # Comment out when working with only General questions
            # print(f"Reading {extra_file}...")  # Comment out when working with only General questions
            # with open(extra_file, 'r', encoding='utf-8-sig') as f:  # Comment out when working with only General questions
            #     reader = csv.DictReader(f)  # Comment out when working with only General questions
                
            #     # Debug: Show what columns we found  # Comment out when working with only General questions
            #     if reader.fieldnames:  # Comment out when working with only General questions
            #         print(f"  Columns found: {reader.fieldnames}")  # Comment out when working with only General questions
                
            #     for row in reader:  # Comment out when working with only General questions
            #         # Handle different possible column names  # Comment out when working with only General questions
            #         question_id = row.get('id') or row.get('ID') or row.get('Id') or ''  # Comment out when working with only General questions
            #         question_text = row.get('question') or row.get('Question') or ''  # Comment out when working with only General questions
            #         correct_answer = (row.get('Correct Answer') or   # Comment out when working with only General questions
            #                         row.get('correct') or   # Comment out when working with only General questions
            #                         row.get('answer') or   # Comment out when working with only General questions
            #                         row.get('Answer') or '')  # Comment out when working with only General questions
                    
            #         if question_id and question_text and correct_answer:  # Comment out when working with only General questions
            #             self.questions.append({  # Comment out when working with only General questions
            #                 'id': question_id.strip(),  # Comment out when working with only General questions
            #                 'question': question_text.strip(),  # Comment out when working with only General questions
            #                 'answer': correct_answer.strip(),  # Comment out when working with only General questions
            #                 'pool': 'Extra'  # Comment out when working with only General questions
            #             })  # Comment out when working with only General questions
            
            # extra_count = len(self.questions) - general_count  # comment this out when working with single dataset (i.e. only General or only Amateur Extra)
            # print(f"✓ Loaded {extra_count} Extra questions")  # comment this out when working with single dataset (i.e. only General or only Amateur Extra)
            # print(f"✓ Total questions: {len(self.questions)}")  # comment this out when working with single dataset (i.e. only General or only Amateur Extra)
            
            if len(self.questions) == 0:
                print("\nERROR: No questions were loaded!")
                print("Please check that your CSV files have the correct format.")
                sys.exit(1)
            
        except FileNotFoundError as e:
            print(f"Error: Could not find file: {e.filename}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading files: {e}")
            print("\nPlease check your CSV file format.")
            print("Expected columns: id, question, Correct Answer")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Title bar with question ID and pool
        self.title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        self.title_frame.pack(fill='x', side='top')
        self.title_frame.pack_propagate(False)
        
        self.title_label = tk.Label(
            self.title_frame,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        self.title_label.pack(expand=True)
        
        # Question section (top half)
        self.question_frame = tk.Frame(self.root, bg='white')
        self.question_frame.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        
        tk.Label(
            self.question_frame,
            text="QUESTION",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 10))
        
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=('Arial', 16),
            bg='white',
            fg='#2c3e50',
            wraplength=750,
            justify='left'
        )
        self.question_label.pack(expand=True)
        
        # Divider
        tk.Frame(self.root, bg='#bdc3c7', height=2).pack(fill='x', padx=20)
        
        # Answer section (bottom half)
        self.answer_frame = tk.Frame(self.root, bg='white')
        self.answer_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        tk.Label(
            self.answer_frame,
            text="CORRECT ANSWER",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 10))
        
        self.answer_label = tk.Label(
            self.answer_frame,
            text="",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#27ae60',
            wraplength=750,
            justify='left'
        )
        self.answer_label.pack(expand=True)
        
        # Bottom control bar
        self.control_frame = tk.Frame(self.root, bg='#ecf0f1', height=80)
        self.control_frame.pack(fill='x', side='bottom')
        self.control_frame.pack_propagate(False)
        
        # Progress label
        self.progress_label = tk.Label(
            self.control_frame,
            text="",
            font=('Arial', 10),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.progress_label.pack(side='left', padx=20)
        
        # Buttons
        button_frame = tk.Frame(self.control_frame, bg='#ecf0f1')
        button_frame.pack(side='right', padx=20)
        
        self.prev_button = tk.Button(
            button_frame,
            text="◄ Previous",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            border=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.previous_question
        )
        self.prev_button.pack(side='left', padx=5)
        
        self.next_button = tk.Button(
            button_frame,
            text="Next ►",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            border=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.next_question
        )
        self.next_button.pack(side='left', padx=5)
        
        # Instructions label
        tk.Label(
            self.control_frame,
            text="Space/→ = Next  |  ← = Previous  |  Esc = Quit",
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#95a5a6'
        ).pack(side='bottom', pady=5)
    
    def display_question(self):
        """Display the current question and answer"""
        q = self.questions[self.current_index]
        
        # Update title with ID and pool
        self.title_label.config(
            text=f"{q['id']} - {q['pool']} Class"
        )
        
        # Update question
        self.question_label.config(text=q['question'])
        
        # Update answer
        self.answer_label.config(text=q['answer'])
        
        # Update progress
        total = len(self.questions)
        progress_text = f"Question {self.current_index + 1} of {total}"
        
        # Add pool transition indicator
        if self.current_index == 0:
            progress_text += " (Start of General)"
        elif q['pool'] == 'Extra' and self.questions[self.current_index - 1]['pool'] == 'General':
            progress_text += " (Start of Extra)"
        
        self.progress_label.config(text=progress_text)
    
    def next_question(self):
        """Go to next question, loop at end"""
        self.current_index = (self.current_index + 1) % len(self.questions)
        self.display_question()
        
        # Visual feedback for loop
        if self.current_index == 0:
            self.root.bell()  # System beep when looping
    
    def previous_question(self):
        """Go to previous question, loop at beginning"""
        self.current_index = (self.current_index - 1) % len(self.questions)
        self.display_question()

def main():
    """Main entry point"""
    print("Ham Radio Flashcard Viewer")
    print("=" * 60)
    
    # Check for files
    general_file = "general.csv"
    extra_file = "extra.csv"
    
    if not os.path.exists(general_file):
        print(f"Error: {general_file} not found!")
        print("Make sure the file is in the same folder as this script")
        sys.exit(1)
    
    if not os.path.exists(extra_file):
        print(f"Error: {extra_file} not found!")
        print("Make sure the file is in the same folder as this script")
        sys.exit(1)
    
    # Create GUI
    root = tk.Tk()
    app = FlashcardViewer(root, general_file, extra_file)
    
    print("\n✓ Flashcard viewer ready!")
    print("✓ Use Space or → to advance")
    print("✓ Use ← to go back")
    print("✓ Press Esc to quit\n")
    
    root.mainloop()

if __name__ == "__main__":
    main()
