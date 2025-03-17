from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from scripts.infer import generate_response
import os

class BlenderChatSystem:
    def __init__(self, model_name="FreedomIntelligence/BlenderLLM", openai_api_key=None):
        self.model_name = model_name
        self.memory = ConversationBufferMemory()
        self.conversation_history = []
        
        # Initialize ChatGPT for conversation
        self.chat_model = ChatOpenAI(
            temperature=0.7,
            openai_api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        
        # Define the prompt template for ChatGPT
        template = """You are an expert in 3D modeling and Blender. Help the user refine their 3D model concept.
        Ask specific questions about details they haven't mentioned.
        Focus on gathering information about:
        - Dimensions and proportions
        - Materials and textures
        - Specific features and details
        - Style preferences
        
        Current conversation:
        {history}
        Human: {input}
        Assistant:"""
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
        
        self.conversation = ConversationChain(
            llm=self.chat_model,
            prompt=self.prompt,
            memory=self.memory
        )
    
    def get_response(self, user_input):
        """Get interactive response from ChatGPT"""
        self.conversation_history.append({"role": "user", "content": user_input})
        response = self.conversation.predict(input=user_input)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def generate_final_script(self):
        """Generate the final Blender script using BlenderLLM"""
        # Combine all user inputs into a detailed prompt
        user_inputs = [msg["content"] for msg in self.conversation_history 
                      if msg["role"] == "user"]
        combined_prompt = "\n".join([
            "Based on the following conversation, create a detailed Blender script:",
            "---",
            *user_inputs,
            "---",
            "Generate a complete bpy script that implements all the discussed features."
        ])
        
        # Generate the final script using BlenderLLM
        return generate_response(self.model_name, combined_prompt)