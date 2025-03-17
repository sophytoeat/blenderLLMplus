import os
import argparse
from scripts.infer import generate_response
from scripts.blender_runner import run_blender_script
from scripts.geometry_utils import calculate_bounding_box
from scripts.config import CAMERA_ANGLES, BRIGHTNESS
from scripts.chat_system import BlenderChatSystem
from dotenv import load_dotenv

load_dotenv()  # Add this at the top of the file

def generate_blender_script(model_name, prompt):
    """Generate a Blender script based on the given model and prompt."""
    return generate_response(model_name, prompt)

def ensure_output_folder_exists(output_folder):
    """Check if the output folder exists, and create it if not."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def run_script_and_save_obj(script, obj_name, output_folder, blender_executable):
    """Run Blender script to save the generated .obj file."""
    ensure_output_folder_exists(output_folder)
    run_blender_script(
        script, obj_name, output_folder, [], [], (), blender_executable, save_obj=True
    )
    return os.path.join(output_folder, f"{obj_name}.obj")

def calculate_and_render_image(script, obj_name, output_folder, obj_path, blender_executable, brightness):
    """Calculate bounding box and render the image using Blender script."""
    ensure_output_folder_exists(output_folder)
    bounding_coords = calculate_bounding_box(obj_path)
    brightness_value = BRIGHTNESS.get(brightness, BRIGHTNESS["Very Dark"])
    run_blender_script(
        script,
        obj_name,
        output_folder,
        bounding_coords,
        CAMERA_ANGLES,
        brightness_value,
        blender_executable,
        save_image=True,
    )

def handle_interactive_mode(args):
    """Handle interactive conversation mode for modeling"""
    print("Welcome to BlenderLLM Interactive Modeling System!")
    print("Let's have a conversation about what you want to create.")
    print("You can chat with the system to refine your idea.")
    print("Type 'done' when you're ready to generate the model.")
    print("\nWhat would you like to create?")
    
    chat_system = BlenderChatSystem(
        model_name=args.model_name,
        openai_api_key="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"  # Or use os.getenv("OPENAI_API_KEY")
    )
    
    conversation_count = 0
    max_turns = 4  # Maximum number of conversation turns
    
    while conversation_count < max_turns:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'done':
            break
            
        # Get model response
        response = chat_system.get_response(user_input)
        print("\nBlenderLLM:", response)
        
        conversation_count += 1
        if conversation_count < max_turns:
            print(f"\n({max_turns - conversation_count} turns remaining. Type 'done' when ready.)")
    
    # Generate final script
    print("\nGenerating final Blender script based on our conversation...")
    final_script = chat_system.generate_final_script()
    print("\nGenerated Blender Script:")
    print(final_script)
    
    # Handle object naming and saving
    obj_name = input("\nEnter name for the output file (default: generated_model): ").strip()
    if not obj_name:
        obj_name = "generated_model"
    
    output_folder = input(f"\nEnter output folder path (default: output/{obj_name}): ").strip()
    if not output_folder:
        output_folder = f"output/{obj_name}"
    
    # Execute the script
    try:
        obj_path = run_script_and_save_obj(
            final_script, obj_name, output_folder, args.blender_executable
        )
        print(f"\nOBJ file saved at {obj_path}")
        
        render_images = input("\nDo you want to render images? (yes/no): ").lower()
        if render_images == 'yes':
            calculate_and_render_image(
                final_script, obj_name, output_folder, obj_path, 
                args.blender_executable, args.brightness
            )
            print(f"Images rendered and saved in {output_folder} folder.")
        
    except Exception as e:
        print(f"\nError executing script: {e}")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run Blender Script to Generate 3D Objects and Images.")
    parser.add_argument("--model_name", type=str, default="FreedomIntelligence/BlenderLLM", 
                       help="Model path to generate the script.")
    parser.add_argument("--prompt", type=str, help="Text prompt to describe the object.")
    parser.add_argument("--obj_name", type=str, default="cube", 
                       help="Name of the generated object file.")
    parser.add_argument("--output_folder", type=str, default="images/cube", 
                       help="Folder to save output files.")
    parser.add_argument("--blender_executable", type=str, default="blender", 
                       help="Path to Blender executable.")
    parser.add_argument("--brightness", type=str, default="Very Dark", 
                       choices=BRIGHTNESS.keys(), 
                       help="Brightness level for the rendered image.")
    parser.add_argument("--interactive", action="store_true", 
                       help="Start in interactive conversation mode")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.interactive:
        handle_interactive_mode(args)
    else:
        if not args.prompt:
            parser.error("--prompt is required when not in interactive mode")
            
        script = generate_blender_script(args.model_name, args.prompt)
        print(f"The bpy script of {args.obj_name} is:\n{script}")

        obj_path = run_script_and_save_obj(
            script, args.obj_name, args.output_folder, args.blender_executable
        )
        print(f"OBJ file saved at {obj_path}.")

        calculate_and_render_image(
            script, args.obj_name, args.output_folder, obj_path, 
            args.blender_executable, args.brightness
        )
        print(f"Image rendered and saved in {args.output_folder} folder.")

if __name__ == "__main__":
    main()
