## Datastar Noob Question
### How can I get a ChatGPT like UI using datastar without sending the entire page in each fragment?


### Setup

Install FastAPI via pip:
```bash
pip install -r requirements.txt
```

Start fastapi server:
```bash
fastapi dev app.py --port 8000
```

Then navigate to localhost:8000

You should see this:

![Current UI](pics/pic.png)

Where lorem ipsum is generated using server sent events powered by datastar on the frontend. The issue I have is that I could not get this to work by only sending individual words via `data: merge append_element`


So then on the `append` branch (`git checkout append`) I try to avoid this by using the `data: merge append_element`. Which sort of works in that my data being sent is much lower, however, it ends up almost crashing my browser and being very choppy.
