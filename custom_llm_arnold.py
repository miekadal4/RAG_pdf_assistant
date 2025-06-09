import ollama
"""
This script demonstrates how to interact with the Ollama API.

Functionality:
- Defines a custom assistant model "arnold" based on the "gemma3:4b" model.
- Customizes the assistant's system prompt to be concise, focused, and informative.
- Sets a custom temperature parameter to control response creativity (though not passed in create here).
"""

model = "gemma3:4b"
custom_system = "You are a highly intelligent assistant. Always provide the most important and relevant information to answer my questions directly. Avoid unnecessary explanations, opinions, or details I didn’t ask for. Be concise and focused"
custom_parameter = "temperature 0.7"
ollama.create(model="arnold", from_=model, system=custom_system, )