from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins)


model_name_or_path = "TheBloke/Llama-2-7b-Chat-GPTQ"
model_basename = "gptq_model-4bit-128g"

use_triton = False
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(
    model_name_or_path,
    model_basename=model_basename,
    use_safetensors=True,
    trust_remote_code=True,
    device="cuda:0",
    use_triton=use_triton,
    quantize_config=None)

logging.set_verbosity(logging.CRITICAL)

print("*** Pipeline:")
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.95,
    repetition_penalty=1.15
)

def inference(prompt):
    prompt_template=f'''[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    {prompt}[/INST]'''

    print("\n\n*** Generate:")
    # input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    # output = model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512)

    raw_result = pipe(prompt_template)[0]['generated_text']

    result = raw_result.replace(f'''[INST] <<SYS>>\n    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n    <</SYS>>\n    {prompt}[/INST]  ''', '')
    print(result)
    
    return result


@app.get('/')
def index():
    return "This is Llama 2 API"


@app.post('/chat')
async def getSentiment(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        if text == "":
            print("Empty data")
            return {"status": 0}
    except Exception as e:
        print(e)
        return {"status": 0}
    
    result = inference(text)

    return {"result": result}
