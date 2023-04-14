# 初始化环境
```
conda activate /data/xxx/llm_inference/venv
```

# Deepspeed官方示例
```
deepspeed normal_test.py
```

# DeepspeedExample示例
```
deepspeed --num_gpus 2 inference_test.py --name /data/xxxx/tmp_model/bloomz-7b1-mt --use_kernel --dtype float16 --ds_inference --max_tokens 1024 --max_new_tokens 1024 --batch_size 1
```
