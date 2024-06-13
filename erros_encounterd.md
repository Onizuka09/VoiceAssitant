## installing pyaudio 
https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error
## tts steup 

install either espeak or espeak-ng 

install mbrola mbrola-fr1 mbrola-fr2 mbrola-fr4 (other voices the mbrola-fr4 is the best)

to test it in the commandline just run

`espeak-ng -v mb-en -s 150 "hello my name is mr black and i like choclate"`

the -s specifies the speed 

## neuralintents on pi 
you need to install this deps first 

sudo apt install libhdf5-dev 

to insatll it in a venv ( recommended) 

python3 -m venv venv 
pip3 install neuralintents 

globally 
pip3 install neuralintents --break-system-packages 

if this didn't work 
clone the repo of neural intents 
cd neuralintents
pip3 install . 




