import boto3
import json
from app.config import AWS_REGION, MODEL_ID

class LLM:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    def generate(self, prompt):
        body = {
            "prompt": f"<s>[INST] {prompt} [/INST]",
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        }

        response = self.client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )

        result = json.loads(response["body"].read())
        print("DEBUG - Bedrock model:", MODEL_ID)
        print("DEBUG - Raw Bedrock response:", result)
        return result.get("generation", "")