#!/bin/bash

wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
chmod a+x Anaconda3-2022.05-Linux-x86_64.sh 
./Anaconda3-2022.05-Linux-x86_64.sh 

mkdir testwiththingy
sudo apt install  rtl-433
sudo apt install  git

cd testwiththingy
git clone https://github.com/gvieri/AQUACO.git 

