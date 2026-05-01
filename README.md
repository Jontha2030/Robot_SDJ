1) su - Jon  (Rpi terminal (búið að búa til user sem heitir Jon))
2) ssh-keygen -t ed25519 -C "youremail@example.com"  (RPi terminal. Ýta á ENTER við öllum spurningum sem poppa upp)
3) cat ~/.ssh/id_ed25519.pub   (RPi terminal. Copy'a allt í output'i á þessari skipun)
4) Búa til nýjan SSH lykil á Github Settings með því sem var copy'að í skrefi 3)
5) ssh -T git@github.com  (Setja þetta í RPi terminal, ætti að koma : "Hi username! You've successfully authenticated...")
6) git clone git@github.com:Jontha2030/Robot_SDJ.git (Í RPi terminal)
7) git config --global user.name "Name" <br>
   git config --global user.email "youremail@example.com"

8) git branch "Nafn" og síðan git switch "Nafn" (Búa til nýtt branch sem hægt er að fykta á)
