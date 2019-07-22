# AI for chrome://dino

#### Human
rec 3376

#### Bot
rec 800

## Source Installation
### requires python 3.5 or above and git with bash and google chrome
### Windows
1. Git Bash


    py -3.5 refers to my python version this can be just replaced by python or other versions
    python or py -3.6

    git clone https://github.com/hallowf/gd-ai
    cd gd-ai
    py -3.5 -m pip install virtualenv==16.1
    py -3.5 -m virtualenv venv
    venv\Scripts\activate <- this creates a local python "install" and "defines" it as main Installation
    pip install -r requirements.txt
    cd src\
    mkdir drivers training trained_models Graph


2. Get chrome drivers http://chromedriver.chromium.org/downloads
 - Download multiple versions and place them in the drivers directory
 - Name them by version number ex: 74.exe 75.exe 73.exe

3. Create training data
 - inside src directory with your virtual environment activated
    * `python get_training_data.py identifier --optional-args`
    * Grab the browser window that appears and move it to the left of your screen until it auto resizes
      - why? because it is where the program captures screenshots
    * the browser may close while trying to find the appropriate driver
    * Play the game (your performance dictates the AI's performance - kind off)
    * the arrow keys (up/down) control the dino and screenshots get taken everytime they are pressed
     * you can also use space to jump but that won't trigger a screenshot
     * if you have captured "unwanted data" delete the last file recorded

4. Balance data
  - same as before:
    * `python balance_data.py identifier --optional-args`
    * This will make sure the data is balanced which means for EX:
     - instead of having lots of images "jumping" and the relative keypress it will discard some images and keypresses so that you have an equal lenght of all possible situations
     - this also means that you will "lose a lot of data captured", the files won't be deleted a new one is created but it will have a lot less data

5. Train the data
  - WARNING: This step may severely impact performance and may cause your pc to crash
  if you don't have the required hardware:
    - +6GB ram
    - +6 core fast cpu or +4 core fast single thread with AVX instruction set
    - ssd is helpfull not required
  - inside src directory with your virtual environment activated
     - `python train_data.py identifier model`
     - while still inside src you can watch the graphs and the structure with the command
      - `tensorboard --logdir=Graph\`

6. Check the results
  - `python play_game.py`



#### if you are a normal human ignore everything below


##### Notes:
1. All optimizers show up in the graphs
 - is this because of instantianting them as objects and storing them
 - or maybe just by importing them?
3. VGG and CIFAR10 seem to be the ones who performed best the others just didn't work or had a poor performance
5. There was a packaging problem involving distutils, donwgrading to virtualenv 16.1 seems to have fixed the issue
  - Either way packaging AI's doesn't seem like a good idea for now, unless you intent to distribute it across multiple users without resorting to cloud computing

##### Packaging

1. Script to package with tensorflow and keras:

       pyinstaller.exe --paths ..\venv\Lib\site-packages\ --add-data CIFAR10_RMSprop_set3.h5;. --hidden-import=h5py,h5py.def,h5py.utils,h5py.h5ac,h5py._proxy play_game.py

2. hidden import also works
  - hiddenimports=['h5py','h5py.defs','h5py.utils','h5py.h5ac','h5py._proxy']
