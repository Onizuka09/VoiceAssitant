## VoiceAssistance

This project represents a Voice assistant that talks about tunisia, created with the help of the Neuralintents Library.



## setup - linux and raspi pi 

### Pyttsx3 

```bash 

sudo apt  update 
sudo apt install espeak ffmpeg libespeak1

pip3 install pyttsx3
``` 



Install new voices

``` bash 

sudo pat install mbrola mbrola-fr1 mbrola-fr2 mbrola-fr4

espeak -v mb/mb-fr1 -s 150 "Bonjours, j'aime le chocolat"


To test the pyttsx3 run the script 

python3 ./test_programs/test_voices.py
```
the -s specifies the speed 


