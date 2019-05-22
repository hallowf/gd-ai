# AI for chrome://dino
### requires python 3.5 or above and git with bash and google chrome

#### Human
rec 3376

#### Bot
rec 700

# Installation
### Windows
1. Git Bash

```
py -3.5 refers to my python version this can be just replaced by python or other versions
python or py -3.6

git clone https://github.com/hallowf/gd-ai
cd gd-ai
py -3.5 -m pip install virtualenv==16.1
py -3.5 -m virtualenv venv
venv\Scripts\activate <- this creates a local python "install" and "defines" it as main Installation
pip install -r requirements.txt
cd src\
mkdir drivers images actions training trained_models Graph
```

2. Get chrome drivers http://chromedriver.chromium.org/downloads
 - Download multiple versions and place them in the drivers directory
 - Name them by version number ex: 74.exe 75.exe 73.exe

3. Create training data
 - inside src directory with your virtual environment activated
    - `python get_training_data.py`
    - Grab the browser window that appears and move it to the left of your screen until it auto resizes
      - why? because it is where the program captures screenshots
      - if your monitor is 4k resolution the screencapture is probably off you can check this by viewing the captured images in the images folder
    - the browser may close while trying to find the appropriate driver
    - Play the game (your performance dictates the AI's performance)
    - the letter t takes a screenshot it is used to map an image to nothing so press it
    when you have clearence
    - the arrow keys control the dino and screenshots get taken everytime they are pressed

4. Train the data
  - WARNING: This step may severely impact performance and may cause your pc to crash
  if you don't have the required hardware:
    - +8GB ram
    - +4 core fast cpu with AVX instruction set
    - ssd is helpfull not required
  - inside src directory with your virtual environment activated
     - `python train_data.py`
     - while still inside src you can watch the graphs and the structure with the command
      - `tensorboard --logdir=Graph\`

5. Check the results
  - `python play_game.py`


#### If you have captured bad/unwanted data just delete images and actions folder and restart from step 3

#### if you are a normal human ignore everything below


##### Notes:
1. All optimizers show up in the graphs
 - is this because of instantianting them as objects and storing them
 - or maybe just by importing them?
3. VGG and CIFAR10 seem to be the ones who performed best the others just didn't work or had a poor performance
4. there is still some "lag" due to the time it takes to capture a screenshot and save it
alongside a keypress could these actions be forwarded to individual threads?
 - the main problem with this would be synchronization of the keypresses and captured images
 - keyboard is multithreaded so it uses it's own thread afaik
5. There was a packaging problem involving distutils, donwgrading to virtualenv 16.1 seems to have fixed the issue
  - Either way packaging AI's doesn't seem like a good idea for now, unless you intent to distribute it across multiple users without resorting to cloud computing

##### Script to package with tensorflow and keras
`pyinstaller.exe --paths ..\venv\Lib\site-packages\ --add-data CIFAR10_RMSprop_set3.h5;. --hidden-import=h5py,h5py.def,h5py.utils,h5py.h5ac,h5py._proxy play_game.py`
##### or hidden import also works
hiddenimports=['h5py','h5py.defs','h5py.utils','h5py.h5ac','h5py._proxy']
