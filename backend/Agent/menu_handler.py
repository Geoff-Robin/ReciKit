from langchain.schema import AIMessage

def handle_menu(user_input, messages):
    if user_input.strip() == "1":
        return AIMessage(content="Okay! Let's record your inventory. Please tell me what items you want to add.")
    elif user_input.strip() == "2":
        return AIMessage(content="Great! Please provide a recipe or ingredient list to analyze nutrition.")
    elif user_input.strip() == "3":
        return AIMessage(content="Sure! Please tell me your preferences (e.g., vegetarian, high protein, etc.)")
    elif user_input.strip() == "4":
        return AIMessage(content="Let's manage your profile. Do you want to update dietary preferences or allergies?")
    elif user_input.lower() in ["hi", "hello"]:
        return AIMessage(content="Hi! What do you want to do today?\n1. Record inventory\n2. Analyze nutrition\n3. Get recipe & meal plan\n4. Manage profile")
    return None 
