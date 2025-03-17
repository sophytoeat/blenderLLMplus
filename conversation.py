from scripts.infer import generate_response
from scripts.blender_runner import run_blender_script
import os

def handle_conversation():
    print("Welcome to BlenderLLM Conversation System!")
    print("Please describe what you want to create:")
    
    # First user input
    initial_prompt = input("> ")
    
    # First response asking for more details
    print("\nBlenderLLM: Please give me a more detailed script.")
    
    # Get detailed script from user
    detailed_script = input("> ")
    
    # Generate the Blender script using the model
    model_name = "FreedomIntelligence/BlenderLLM"  # Updated model path
    response = generate_response(model_name, detailed_script)
    
    print("\nGenerated Blender Script:")
    print(response)
    
    # Optionally, you can ask if they want to execute the script
    while True:
        execute = input("\nDo you want to execute this script? (yes/no): ").lower()
        if execute in ['yes', 'no']:
            break
        print("Please answer 'yes' or 'no'")
    
    if execute == 'yes':
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        
        try:
            run_blender_script(
                response,
                "generated_model",
                output_folder,
                [], [], (),
                "blender",  # You might want to make this configurable
                save_obj=True
            )
            print(f"\nScript executed successfully! Output saved in {output_folder}")
        except Exception as e:
            print(f"\nError executing script: {e}")

if __name__ == "__main__":
    handle_conversation() 