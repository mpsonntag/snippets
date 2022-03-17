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

## Fedora notes

You can always access TTY w/o fancy graphics by pressing Alt+Ctrl+F3 and return by Alt+Ctrl+F2

Same issue occurs on Fedora

official driver download:
https://www.nvidia.com/Download/Find.aspx?lang=en-us

https://tecadmin.net/how-to-install-nvidia-drivers-on-fedora/
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html
https://www.if-not-true-then-false.com/2015/fedora-nvidia-guide/
https://phoenixnap.com/kb/fedora-nvidia-drivers

## Install Nvidia Drivers with RPM Fusion

    sudo dnf update
    sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
    https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
    lspci | grep VGA
    lspci | grep 3d
    sudo dnf install akmod-nvidia
    # or 
    sudo dnf install xorg-x11-drv-nvidia-390xx akmod-nvidia-390xx
    sudo dnf install xorg-x11-drv-nvidia-340xx akmod-nvidia-340xx

https://rpmfusion.org/Howto/NVIDIA

Something to consider in case of further issues: "... many similar issues ... with fedora 35 ... disable secure boot ... kernel now is actively blocking unsigned kernel modules from loading when secure boot is enabled."
