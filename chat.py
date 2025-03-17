import argparse
from scripts.infer import generate_response
from conversation import handle_conversation

def parse_arguments():
    """
    Parse command line arguments for model name and prompt.
    """
    parser = argparse.ArgumentParser(description="Generate a response using a specified model.")
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model to use for response generation.")
    parser.add_argument("--prompt", type=str, help="Input prompt to generate a response.")
    parser.add_argument("--interactive", action="store_true", help="Start in interactive conversation mode")
    return parser.parse_args()

def main():
    """
    Main function to generate a response using input arguments.
    """
    args = parse_arguments()
    
    if args.interactive:
        handle_conversation()
    else:
        if not args.prompt:
            parser.error("--prompt is required when not in interactive mode")
            
        # Generate response
        response = generate_response(args.model_name, args.prompt)
        
        # Print the result
        print("Generated Response:\n", response)

if __name__ == "__main__":
    main()