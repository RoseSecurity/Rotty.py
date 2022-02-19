# Rotty.py

![4752-gal-kingofcocaine-4](https://user-images.githubusercontent.com/72598486/154787169-11ed5a39-3eb5-4a43-b394-87861d3968c0.png)

Rotty.py delivers a cross-platform solution for performing simple home network monitoring. Utilizing network mapping and port scanning capabilities, Rotty will monitor your home network and report any significant changes that occur via email. This simple script will give you visibility and insight into the dynamic and ever-changing environment of your network. 

# Installation:

To install on Linux:

```
Rotty@BigDog $ sudo git clone https://github.com/RoseSecurity/Rotty.py.git
Cloning into 'Rotty.py'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 12 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (12/12), 5.01 KiB | 5.01 MiB/s, done.
Resolving deltas: 100% (2/2), done.

Rotty@BigDog $ cd Rotty.py/
Rotty@BigDog $ pip3 install -r requirements.txt
Rotty@BigDog $ sudo python3 Rotty.py
```

To run the script daily, as it is intended:

```Rotty@BigDog $ sudo crontab -e```

Within the file, add the following line:

```00 10 * * * <path to file>/Rotty.py```

# Interface

<img width="1440" alt="Interface" src="https://user-images.githubusercontent.com/72598486/154787952-bc163bf2-16c5-4afa-b711-a7fba4ec8ac6.png">





