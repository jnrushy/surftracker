# This program asks about your surf session and responds to your feedback

# Function to get user input about their surf session
def get_surf_feedback():
    # Start an infinite loop that only breaks when valid input is received
    while True:
        # Ask for user input and convert it to lowercase to make it case-insensitive
        response = input("How was your surf session today? (good/bad): ").lower()
        
        # Check if the response is either 'good' or 'bad'
        if response in ['good', 'bad']:
            return response  # If valid input, return it and exit the function
        
        # If input was invalid, show error message and loop continues
        print("Please enter either 'good' or 'bad'.")

# Main function that controls the program flow
def main():
    # Get the surf session feedback from user
    feedback = get_surf_feedback()
    
    # Respond differently based on whether the session was good or bad
    if feedback == 'good':
        print("Awesome! Glad you had a great session! 🏄")
    else:
        print("Bummer! Hope your next session is better! 🌊")

# This is the entry point of the program
# It only runs the main() function if this file is run directly (not imported)
if __name__ == "__main__":
    main() 