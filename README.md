# 🚀 GPT-2 Text Generation Fine-Tuning & Web Deployment

This project demonstrates how to fine-tune GPT-2, integrate it inside a Flask web application, and deploy the entire solution using Docker, making it easy for anyone to access the model through a web interface.

## 📌 Features
🔬 Model Fine-Tuning

Fine-tuned GPT-2 using HuggingFace transformers

Supports multiple decoding strategies:

* Greedy Search

* Beam Search

* Top-K Sampling

* Top-P Sampling

* Temperature-based sampling

Customizable generation parameters using a simple UI

### 🌐 Flask Web App

### Attractive UI with:

* Prompt input box

* Method selection dropdown

* Adjustable parameters

### Clean backend structure using:

* Blueprints

* templates/ and static/ organization

* Real-time text generation output

## 🐳 Docker Deployment

Ready-to-use Dockerfile

#### Build your image:

* docker build -t yourname/gpt2-generator .


#### Run the container:

* docker run -p 5000:5000 yourname/gpt2-generator


Fully compatible with Railway / Render deployments

## 📁 Project Structure
project\
│
├── app\
│   ├── static\
│   │   └── css/style.css\
│   ├── templates\
│   │   ├── index.html\
│   │   ├── layout.html\
│   │   └── result.html\
│   ├── routes.py\
│   └── config.py\
│
├── models\
│   ├── generator.py\
│   └── __init__.py\
│
├── scripts\
│   └── train_gpt2.py  (optional – fine-tuning script)\
│
├── run.py\
├── Dockerfile\
├── requirements.txt\
└── README.md\

## ⚙️ How It Works
1️⃣ User enters a prompt\
2️⃣ Chooses a generation strategy\
3️⃣ Flask backend sends the prompt to the GPT-2 model\
4️⃣ The model generates text based on selected parameters\
5️⃣ Output displayed on the web page

## 🏗 Installation
### Clone the repository:
* git clone https://github.com/ruhul-cse-duet/gpt-2-text-generator-fine-tune.git \
cd gpt2-text-generator

### Install dependencies:
* pip install -r requirements.txt

### Run locally:
* python run.py

## 🧠 Technologies Used

* Python

* PyTorch

* HuggingFace Transformers

* Flask

* HTML / CSS

* Docker

## 🙌 Acknowledgements

Thanks to:

* HuggingFace for GPT-2 model

* Flask community

* Docker for containerized deployment

## Author
[Md Ruhul Amin](https://www.linkedin.com/in/ruhul-duet-cse/);  
Email: ruhul.cse.duet@gmail.com
