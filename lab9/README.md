# PR Lab No. 9

---

#### Author: *Corneliu Catlabuga*
#### Group: *FAF-213*
#### Task: Mail client using SMTP and FTP

---

# Instructions:

## Running the SMTP client

### Virtual environment setup
```bash
python3 -m venv venv
```

### Activate virtual environment

Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate.bat
```

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Run the app
```bash
python3 main.py
```

## Uploading files to FTP server:
```bash
python3 send_file.py <path_to_file>
```
