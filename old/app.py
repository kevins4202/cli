from fastapi import FastAPI
import bing  # Import your Python script here (e.g., `import my_script`)

app = FastAPI()

@app.get("/run-script")
async def run_script():
    result = bing.run()  # Replace with the function or code to execute your script
    return {"status": "Script executed", "result": result}
