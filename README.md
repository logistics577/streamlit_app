# streamlit_app
Build & Run (Commands)
```
# 1. Build the image
docker build -t chatbot .

# 2. Run the container
docker run -d \
  --name chatbot \
  --restart unless-stopped \
  -p 8501:8501 \
  chatbot

```