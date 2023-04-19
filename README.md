# AVL - A machine learning tool to detech phishing URLs

AVL has 2 main parts:
1. **server**: A flask webserver which provide a restful api to fetch an url's information
2. **extension**: A Chrome extension which interact with sharkcop-server to detech phishing URLs

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

```
Python 3 >
```

### Installing
Clone the repository
```
git clone https://github.com/Chisj1/AVL-team
```


**1. Install sharkcop-server on your local machine**

At the project root directory, run
```
cd AVL-team
```

Install the required packages
```
pip3 install –r requirements.txt
```

```
python3 app.py
```

![image](https://user-images.githubusercontent.com/63899044/232265426-ea208920-dfea-4492-a88e-9426a4be749d.png)

The server will be up at 127.0.0.1:8080. 
The RESTful API endpoint would be in this format:
```
http://127.0.0.1:8080/api/check?url=https://abc.xyz
```

You can test the api through a web interface at http://127.0.0.1:8080

There are 2 statuses that could be returned:
-  1 : The url is phishing
-  0 : The url is normal

**2. Setup extension (for Chrome)**

  - Open Chrome Extension Manager (chrome://extensions/)
  - Enable Developer Mode
  - Click 'Load unpacked' and select the directory **'extension'** inside our project root directory
  
![image](https://user-images.githubusercontent.com/63899044/232265450-b62708f5-529e-4807-a127-7a4fd507fc87.png)


## Built With

* Python
* Javascript

## Techniques
* Preprocessing: NLP, TF-IDF vectorizer
* Model: naive bayes

![image](https://user-images.githubusercontent.com/63899044/232265561-1afde0c4-836c-4aaa-b58b-9612ab6c2119.png)
