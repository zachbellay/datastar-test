import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory=".")

lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget blandit nisl. Ut luctus arcu sit amet tempus imperdiet. Nunc mi tellus, aliquam et pharetra a, tempor non mi. Mauris non odio consectetur, consequat magna in, semper tellus. Vivamus magna nisl, elementum sed velit sed, auctor rutrum tortor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce at neque sodales, euismod eros a, tincidunt lorem. Aenean vel dolor laoreet risus laoreet convallis a ut risus. Morbi tincidunt nisl nec lacus luctus maximus. Fusce feugiat felis a viverra bibendum. Nullam sit amet posuere ipsum, vulputate accumsan ante.

Pellentesque vehicula nisl sed ornare pulvinar. In tempor mauris ac purus pretium semper. Sed ante eros, facilisis eu porttitor at, pellentesque vitae risus. Aliquam ultrices euismod augue, at facilisis elit consectetur a. Duis et pellentesque massa, sed venenatis nisl. Sed laoreet velit eget enim pretium venenatis. Nulla et consequat risus, eget posuere ligula. Quisque pulvinar risus tellus. Integer dictum ipsum sapien, ut porttitor nibh luctus nec.

Sed ante augue, faucibus vitae maximus sit amet, consectetur id lectus. Donec facilisis ex eu libero volutpat fermentum. In vitae odio lacinia, interdum ante sed, imperdiet ligula. Nam viverra condimentum sem, nec ultrices ante facilisis tincidunt. Cras eu sapien vitae purus sollicitudin scelerisque id dignissim orci. Nullam venenatis maximus sapien, non iaculis enim vehicula sed. Praesent et sodales ipsum. Etiam eleifend augue massa, eu mollis orci dignissim at. Nullam viverra dapibus eleifend. Sed vestibulum quam non aliquam vulputate.

Aenean at euismod libero. Aliquam semper vestibulum eros vitae posuere. Donec porttitor purus nec tellus auctor varius et varius metus. Aenean semper congue nisl non sodales. Pellentesque metus nunc, semper in eros id, dignissim pharetra massa. Morbi at rhoncus turpis. Donec in libero in turpis lobortis ultricies. Aenean consequat justo ut nulla auctor, vitae blandit tellus mattis. Integer nec sapien pretium, consequat risus eget, gravida odio. Pellentesque laoreet semper nisl, id ullamcorper quam ullamcorper id. Quisque ornare quam vitae ipsum vestibulum congue. Sed eu risus lobortis, maximus ipsum eget, finibus felis.

Nam hendrerit diam sit amet sem feugiat, eget lobortis lacus feugiat. Sed aliquet sem vitae tellus fermentum tristique. Donec gravida pretium fringilla. Proin fermentum libero sit amet metus faucibus malesuada. Nullam imperdiet lectus ac finibus ultrices. In fermentum lobortis dolor in viverra. Suspendisse semper nisl eu sapien iaculis, sed convallis ipsum sodales. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam aliquam tristique feugiat. Praesent in eros consequat, sollicitudin tellus nec, dapibus lacus. Phasellus convallis nibh turpis, nec tincidunt elit volutpat sit amet. Proin porttitor varius ligula et finibus. Nulla ac auctor nunc, in ornare turpis. Fusce vel mollis orci. Ut quis lorem id dolor dictum luctus. """

def send_event(frag: str, merge: bool = False):
    event_data = 'event: datastar-fragment\n'   
    if merge:
        event_data += 'data: merge append_element\n'
        event_data += 'data: selector #feed\n'
    event_data += f'data: fragment {frag}\n\n'
    return event_data

def lorem_ipsum_generator():
    words = lorem.split()
    for word in words:
        yield word

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="base.html")

@app.get("/stream/")
async def stream():
    async def event_stream():
        generator = lorem_ipsum_generator()
        while True:
            try:
                frag = f'<span>{next(generator)} </span>'
                yield send_event(frag, merge=True)
                await asyncio.sleep(0.01)
            except StopIteration:
                break

    return StreamingResponse(event_stream(), media_type='text/event-stream')
