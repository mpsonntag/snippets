Graphic card crashes on Linux (Ubuntu) with Nvidia graphics cards.

Open source Nvidia driver "nouveau" can lead to crashes. To replace them with the original ones from Nvidia check:

http://www.linuxandubuntu.com/home/how-to-install-latest-nvidia-drivers-in-linux
https://askubuntu.com/questions/61396/how-do-i-install-the-nvidia-drivers
https://www.nvidia.com/object/unix.html
https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa

    sudo apt-get purge nvidia*
    sudo add-apt-repository ppa:graphics-drivers
    sudo apt-get update
    # get the latest version here from the page linked above
    sudo apt-get install nvidia-390
    # reboot and check install
    lsmod | grep nvidia
    # if this is empty, check nouveau drivers
    lsmod | grep nouveau
    # if everything worked, avoid automatic updates
    sudo apt-mark hold nvidia-390
