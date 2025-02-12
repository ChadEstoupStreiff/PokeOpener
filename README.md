# 🐉 PokeOpener
PokeOpener is an application/game to draw random cards among more than 18000 cards to create your own collection.

## 🚀 Start the app
**Edit [.env](.env) file with your needs.**  
You can start everything with this command:
```bash
docker-compose up -d
```

## 🌐 Front application
You'll find all the code (and Dockerfile) inside [front](front) folder.  
The application uses the library [streamlit](https://streamlit.io/) to create a complete application.  

## 🤖 Back API
You'll find all the code (and Dockerfile) inside [back](back) folder.  
The application uses the library [fastapi](https://fastapi.tiangolo.com/) to create a complete API.  

## 📝 Test
You'll find all the code (and Dockerfile) inside [back_test](back) folder.  
The application uses the library [pytest](https://docs.pytest.org/en/stable/) to create tests.  

## 🔁 CI/CD
We use github action to automatically build and start containers to be able to make e2e tests.  
Look at this [config](.github/workflows/ci.yml) file