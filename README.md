# Arduino AI Defence system
Arduino based defence system that tracks faces and uses a mini-potato launcher to "throw" food at intruders.

...

click on the different titles to show each section...

header 1 + link
header 2
header 3...

---

<details style="margin-bottom: 1px;" > 
  <summary><h1> 🔋 Parts & Robotics... </h2></summary>
  <p align="left">
     <img align="right" src="media/1.jpg" width="330" />

The 3d files are located in the `3d files` folder. \
Robotic parts:
- Your PC;
- 2 SG90 servo motors;
- 1 MG996R servo motor;
- 1 Stepper motor 28BYJ-48 + control module;
- Any Arduino Board (im using Uno);
- Arduino Breadboard (or solder the cables);
- 1 relay module + 3-9v battery;
- 1 High voltage generator (3-7v input : 50kv output);
- Small speaker (not required);
- Led light bulbs (not required);
- Laser pointer (not required)
- Jumpers, cables, screws, tape, hot glue and other stuff;

Non-robotic parts:  
- 1 needle;
- 1 lighter;
- Empty shampoo bottle;
- Long pvc pipe that fits in the bottle;
- Short metal pipe that fits on the outside of the pvc pipe;
- Grapes or any small (but soft) fruits that fit into the pipe;

Alternatively, if you want to run this project anywhere:
- Replace the PC and the Arduino Controller with a raspberry pi (at least raspberry 3 imo);
- Usb camera;
- 5v output Powerbank;
- Screen/LCD display OR Old phone (with hdmi to usb streaming cable); 

You can get most of these parts on Aliexpress for very cheap prices.

  </p>
  
</details>

---

<details style="margin-bottom: 1px;" > 
  <summary><h1> 💻 Code and Machine Learning... </h2></summary>
  <p align="left">

<img align="right" src="media/2.jpg" width="330" />

This system is based on the Haarscade model, which has to be trained first, i explained the way this model works on [my previous repo](https://github.com/Hue-Jhan/AI-Face-Recognition-n-Tracking), it's divided in 2 codes, what it does is simply detecting and training on faces using a locally stored "binary pattern histogram" model called Haarscade, made by a German professor. This algorithm recognizes patterns in grey-scale images (taken previously) to detect faces, and the rest of the code starts tracking them. It also detects hostile faces if they are not associated with a pre-made user. Here are the all the codes explained:

#### - Data Collect.py
The first code takes 500 pics and inserts them into the datasets folder, they are associated to a specific user. It detects the faces using the haarscade model after putting the pics in a grey-scale format.

#### - Training Demo.py
The second code trains on the previously taken images, more precisely it opens all the previously taken pictures, and for every id (user) it tries to fetch the face unique patterns and stores them into a ```Trainer.yml``` file.

#### - Defense System.py (tracking system)
The actual tracking implemented in the ```defense-system.py``` is more complex, the camera constantly takes pictures and tries to detect faces in them, if a face is associated to a user, it keeps getting tracked until it disappears for 1 second, if a face remains unknown for over 2.5 seconds it's recognized as a hostile face, and its coorinates will then be sent to the motors, here is a more detailed explanation:

- Every second the camera takes various pictures (CV2 library, camera displayed on a custom image), if a face is found, the system will then check if the patterns of the face match the ones of any of the known users (located in Trainer.yml file), this "predictment" has a confidence level which tells us how likely a face is an actual known user's face.

- If the confidence level is above a certain level (it is reccomended to raise this level only after training lots of images, default is set to 55 but raise it if the faces are far away from the camera, as the model is not precise at longer distances) then a timer will start, if the confidence remains high for 2.5 seconds straight (without a single failure) then the system will add that face to a ```permanent faces``` list and won't try to recognize it anymore as it highly likely that the person matches the associated user. 

- The face will then be tracked until it disappears for over 1 second (and gets removed from the list), this is done because the algorithm isnt perfect and sometimes for a split second it wont recognize the face, this is due to a slight change in lighting, position, or whatever, therefore if a face isnt recognized for a short moment, for example if the user turns around, the tracking wont be lost and wont have to restart again.

- If the confidence is below a certain level, the face will simply be named "Unknown", if a face is unknown for over 2.5 seconds it's most likely that the person is an intruder, therefore the face is added to a ```permanent hostile``` list and will receive a heavy punishment. The system will start a sniper-like precise tracking and will fetch the exact coordinates of the face, the coorinates are based on the frame width of the camera, therefore if you use a different camera than me, then you will have to set some stuff on your own.

- The hostile face is lost after 1 second of no detection, meaning the intruder is probably gone, which means it's then removed from the hostile list and the face recognizer algorithm will start again. The code ends if u press "q".

#### - Defense System.py (Arduino Board)

First of all i'm gonna use PyMata library as PyFirmata is difficult to use with a Stepper motor, also there might be an error when sending signals to the Stepper motor but that can be easily resolved looking it up on google. 

Before the actual code several things need to be setup: the board, the Stepper motor pins, steps and variables, the Servo motors pins, the relay, the camera, the face-recognizer related modules, and of course all the paths and other variables. If you are using a different camera setup than me (for example an external usb camera) you might have to change some things like the cv2 library commands, ex: ```video = cv2.VideoCapture(0)```. 

You might also have issues establishing the com port but that's also easily solvable by googling the problem. 

If you are using a raspberry pi you will need to change lots of stuff like the way the camera sends signal or the PyMata library, in the future i will probably upload a code for the raspberry pi version of the entire system but because i only have a raspberry pi 3b+, training the model might be slow and overall difficult.

#### - Defense System.py (Motors and modules control)

- The first Servo motor controls the top to bottom movement of the system, its controlled by the ```ServoPoint function```, this function uses numpy library to calculate the right angle given the coordinates of the face, the width of the camera frame, and the a given "angle range", which i set to 45/125 as default.
- The Stepper motor controls the movements from left to right (x axis) of the defense system, its movement is controlled by the ```StepperPoint function```, because stepper motors work differently from servo motors, i had to use a different approach: first of all the starting point is calculated as the middle point between the furthest point to the left and the furthest from the right that the stepper can reach (technically stepper motor can rotate 360° as many times as they want, that's why i had to set these boundaries and start rotating the motor from them), second of all we calculate the angle we must reach based on the x coordinates, the width of the frame and the overall angle range (must be 180°). Then using this angle we calculate the amount of steps needed to reach that spot (considering also a thresold to avoid small changes every time) and we move the stepper to match those steps. Finally we update the current steps in order to update the starting position for the next cycle.
- The second SG90 servo and MG996R servo are used respectively to reload the food and to recharge the gas, they are both controlled by the ```ShootChargeLoad``` funtion (which also controls the relay), the reload servo is normally set to its furthest point to the left (180°), when its time to reload the payload it will be moved slighlty to the right to allow the next piece of food to fall in the chamber, and then will go back to its original position to the left in order to cover the chamber. The gas recharge motor does pretty much the same movements, it holds for a second the button that pushes out the gas out of the lighter, and goes back to its starting position.
- The relay is controlled by the same function as the 2 servos, and it simply turns on a high voltage generator.

  </p>
  
</details>

---

<details style="margin-bottom: 1px;" > 
  <summary><h1> ⚙ Engeneering and Robotics... </h1></summary>
  <p align="left">


warnign!! danger..<>


The system is basically just an automated potato launcher but for smaller and softer fruits like grapes, you can find the 3d files in the ```3d files``` folder, i used Pla+ on my Anycubik kobra 2 3d printer

#### - Launcher
The launcher works by incjecting gas from the lighter (remove the zapping system first tho) in the combustion chamber (empty shampoo bottle) through a small hole at the bottom of the bottle (on the opposite side of the opening cap), you will have to insert the cables of the high voltage generator there too, when the gas is lit by the high voltage generator, it quickly expands and whatever is at the other end of the bottle (where the cap was in the first place) gets quickly pushed away, if you add a pvc pipe at the end, the range and the precision of the projectile will greatly increase.

This angle range must be modified based on real life conditions, for example if the system and the camera are far away from the face, the angle will have to be smaller (like 70/100) because a light change in the angle will result in a huge difference in the overall path of the projectile (if the distance is long enough).

#### - Reloader
mag + reloader + payload...

<img align="right" src="media/2.jpg" width="330" />
  
Code....

! caution sign ! 

  </p>
  
</details>

