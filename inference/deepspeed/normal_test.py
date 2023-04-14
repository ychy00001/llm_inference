import os
import deepspeed
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoConfig

local_rank = int(os.getenv('LOCAL_RANK', '0'))
world_size = int(os.getenv('WORLD_SIZE', '4'))

model_path = "/data/yckj3980/tmp_model/bloomz-7b1-mt"
# max_memory_mapping = {6: "1GB", 7: "2GB"}
# model_8bit = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", load_in_8bit=True, max_memory=max_memory_mapping)
model_8bit = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)

pipe = pipeline("text-generation", model=model_8bit, tokenizer=tokenizer)

json_config = str(config.to_json_string)
print(json_config, type(json_config))


pipe.model = deepspeed.init_inference(pipe.model,
                                 mp_size=4,
                                 dtype=torch.half,
                                 #checkpoint=model_path+"/config.json",
                                 replace_with_kernel_inject=True)


prompt = "你是一个对话机器人，请用对话的方式回答下面问题。问题：你是谁？"

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
generated_ids = model_8bit.generate(**inputs)
output_ids = model(**inputs)
#print(output_ids)
outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

outputs = pipe(prompt)
print(outputs)
