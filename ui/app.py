import gradio as gr
import requests
import json

def request_api(prompt, max_tokens=64, top_k=50, top_p=0.5, temperature=0.7):
    url="http://10.128.61.9:7070/generation"
    headers={
        'Content-Type': 'application/json',
        'accept': 'application/json'  
    }
    payload={
        "max_tokens": max_tokens,
        "prompt": prompt,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature
    }
    print(payload)
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    json_obj = json.loads(r.content)
    return json_obj['text']

def inference(model_name, prompt, temperature):
    #salutation = "Good morning" if is_morning else "Good evening"
    #greeting = f"{salutation} {model_name}. It is {temperature} degrees today"
    
    result = request_api(prompt=prompt, temperature=temperature)
    return result

with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown(
    """
    # LLM Inference
    Pick a model and trying inference!
    """)
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            dropdown_model = gr.Dropdown(["bloomz-7b-mt", "llama-7b-hf", "others"], label="Model")
            textbox_prompt = gr.Textbox(label="Prompt", lines=5)
            btn_generate = gr.Button(value="Generate", variant="primary").style(full_width=True, size='sm')
            slider_temperature = gr.Slider(label="Temperature", value=0.7, minimum=0, maximum=1, step=0.1)
        with gr.Column(scale=2, min_width=600):
            textbox_output = gr.TextArea(label="Output", lines=13, max_lines
=13)

        btn_generate.click(
            fn=inference, 
            inputs=[dropdown_model, textbox_prompt,  slider_temperature], 
            outputs=textbox_output
        )


if __name__ == "__main__":
   demo.launch(share=False, server_name='0.0.0.0', server_port=7860) 
