from Agent.models import Message

def handle_menu(user_input, messages):
    if user_input.strip() == "1":
        return Message(role="assistant", content="Okay! Let's record your inventory. Please tell me what items you want to add.")
    elif user_input.strip() == "2":
        return Message(role="assistant", content="Great! Please provide a recipe or ingredient list to analyze nutrition.")
    elif user_input.strip() == "4":
        return Message(role="assistant", content="Let's manage your profile. Do you want to update dietary preferences or allergies?")
    elif len(messages)==1:
        return Message(role="assistant", content="Hi! What do you want to do today?\n1. Record inventory\n2. Analyze nutrition\n3. Get recipe & meal plan\n4. Manage profile")
    return None 
