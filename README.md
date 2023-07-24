# llama-2-inference

<img src="https://github.com/rezkyws/llama-2-inference/assets/54891455/66563d2e-52e5-40fb-9862-2816df58ee11"  width="600" height="400">

This is quantized llama 2 7b model version.

You can running this model in two different ways with this repo : 
* Only API
* Using Web UI (streamlit)

first things first, please run the requirements :
> pip install -r requirements.txt

To run api only :
> uvicorn run api:app --host 0.0.0.0 --port 4342

If you want to use the UI, run the api first and the run this command :
> streamlit run streamlit.py --server.port=4343

**Note** : You need approximately 5 gb vram in order to run this model (7b ver) in your local machine.
