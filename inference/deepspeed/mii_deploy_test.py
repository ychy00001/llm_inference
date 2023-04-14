import mii
mii_configs = {"tensor_parallel": 2, "dtype": "fp16"}
mii.deploy(task="text-generation",
           model="/data/yckj3980/tmp_model/bloomz-7b1-mt",
           deployment_name="bloom7b_deployment",
           mii_config=mii_configs)
