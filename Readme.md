## VoiceAssistance

This project represents a Voice assistant that talks about Freeways club, created with the help of the Neuralintents Library.



## setup - linux and raspi pi 

- Pyttsx3 
```bash 
sudo apt  update 
sudo apt install espeak ffmpeg libespeak1 
sudo apt-get install portaudio19-dev
``` 

- Install new voices
```bash 
sudo apt install mbrola mbrola-us3

espeak -v mb/mb-us3 -s 150 "Hello world, happy things "


```
> the -s specifies the speed 

- install requirements

```bash 
pip3 install -r requirements.txt
```

- we can test voices using 
```bash 
# To test the pyttsx3 run the script 

python3 ./test_programs/test_voices.py
```
### nltk setup 
- this is for training new intents or the intents database gets updated 
```python 
import nltk
nltk.download('punkt_tab')
```

