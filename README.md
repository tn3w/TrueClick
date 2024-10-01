![https://github.com/tn3w/TrueClick/releases/download/img_v1/TrueClick.png](https://github.com/tn3w/TrueClick/releases/download/img_v1/TrueClick.png)

# 𝐓𝐫𝐮𝐞𝐂𝐥𝐢𝐜𝐤
An open source, GDPR-compliant protection against robots that uses a mixture of human confirmation and Prove of Work.

<br>

## 🚀 Installation
#### Clone the Repository
```bash
git clone https://github.com/tn3w/TrueClick
```

or download the zip [here](https://github.com/tn3w/TrueClick/archive/refs/heads/master.zip).

#### Create Venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Run app.py
```bash
python3 app.py
```

## Known Issues
### opencv-python
If you encounter the error `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`, you can resolve it by installing the OpenGL package. Below are the commands specific to your operating system:
#### Ubuntu/Debian-based Systems
```bash
sudo apt-get update
sudo apt-get install libgl1-mesa-glx
```

#### Fedora
```bash
sudo dnf install mesa-libGL
```

#### Arch Linux
```bash
sudo pacman -S mesa
```

#### CentOS/RHEL
```bash
sudo yum install mesa-libGL
```

#### macOS
OpenGL is included with macOS, but you can ensure your system is up to date. If you are using Homebrew, you can reinstall OpenCV:
```bash
brew install opencv
```

#### Windows
For Windows, ensure that you have the appropriate OpenGL drivers installed. You can usually download these from your graphics card manufacturer's website (NVIDIA, AMD, Intel).

#### Docker
If you are using a Docker container based on Ubuntu, you can add the following line to your Dockerfile:
```Dockerfile
RUN apt-get update && apt-get install -y libgl1-mesa-glx
```
