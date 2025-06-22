import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/bitnet-b1.58-2B-4T"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    force_download=True,
)

# Initial system message
messages = [
    {"role": "system", "content": "You are a Senior Programmer."},
]

print("Type your message. Type 'Thank you BITNET' to end the chat.")

while True:
    user_input = input("\nYou: ")
    if user_input.strip() == "Thank you BITNET":
        print("Chat ended. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)
    chat_outputs = model.generate(**chat_input, max_new_tokens=700)
    response = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True)

    print("\nAssistant Response:", response)
    # Add assistant's message to history for context in next turn
    messages.append({"role": "assistant", "content": response})