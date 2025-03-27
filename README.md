# Arduino AI Defence system
Arduino based defence system that tracks faces and uses a mini-potato launcher to "throw" food at intruders.

...

click on the different titles to show each section...

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

This system is based on the Haarscade model, which has to be trained first, i explained the way this model works on [my previous repo](https://github.com/Hue-Jhan/AI-Face-Recognition-n-Tracking), it's divided in 2 codes, what it does is simply detecting and training on faces using a locally stored "binary pattern histogram" model called Haarscade, made by a German professor. This algorithm recognizes patterns in grey-scale images (taken previously) to detect faces, and the rest of the code starts tracking them. It also detects hostile faces if they are not associated with a pre-made user, and starts pointing at them in an ominous way :O 

##### - Data Collect
The first code takes 500 pics and inserts them into the datasets folder, they are associated to a specific user. It detects the faces using the haarscade model after putting the pics in a grey-scale format.

##### - Training Demo
The second code trains on the previously taken images, more precisely it opens all the previously taken pictures, and for every id (user) it tries to fetch the face unique patterns and stores them into a ```Trainer.yml``` file.

##### - Actual tracking ()
The actual tracking (implemented in the ```defense-system.py``` is more complex: \
Every second the camera will take various pictures and send them to the system, which will try to detect faces from them using the patterns saved in the Trainer.yml file. If a face is associated to a user, it keeps getting tracked until it disappears for 1 second (will explain later why), if a face remains unknown for over 2.5 seconds, then it's recognized as a hostile face, and a slighly different kind of tracking will begin, this one takes the face coordinates and will send them to the motors. The face is detected through cv2 library and displayed on a custom image.

##### - aaa

aaa
The AI works like this: 

- Every second the camera takes various pictures, if a face is found, the system will then check if the patterns of the face match the ones of any of the known users (located in Trainer.yml file), this "predictment" has a confidence level which tells us how likely a face is an actual known user's face.

- If the confidence level is above a certain level (it is reccomended to raise this level only after training lots of images, default is set to 55 but raise it if the faces are far away from the camera, as the model is not precise at longer distances) then a timer will start, if the confidence remains high for 2.5 seconds straight (without a single failure) then the system will add that face to a ```permanent faces``` list and won't try to recognize it anymore as it highly likely that the person matches the associated user. 

- The face will then be tracked until it disappears for over 1 second (and gets removed from the list), this is done because the algorithm isnt perfect and sometimes for a split second it wont recognize the face, this is due to a slight change in lighting, position, or whatever, therefore if a face isnt recognized for a short moment, for example if the user turns around, the tracking wont be lost and wont have to restart again.

- If the confidence is below a certain level, the face will simply be named "Unknown", if a face is unknown for over 2.5 seconds it's most likely that the person is an intruder, therefore the face is added to a ```permanent hostile``` list and will receive a heavy punishment. The system will start a sniper-like precise tracking and will fetch the exact coordinates of the face, the coorinates are based on the frame width of the camera, therefore if you use a different camera than me, then you will have to set some stuff on your own.  You can do whatever you want with those coordinates, such as a defense system which will """send""" flying """objects""" towards that intruder.

- The hostile face is lost after 1 second of no detection, meaning the blac- ehm i mean the intruder is probably gone, which means it's then removed from the hostile list and the face recognizer algorithm will start again.

The code ends if u press "q". You can implement more functions such as security checks, for example if a face is recognized as user X, and you press a certain letter, you can send a command to Arduino (using PyFirmata or other libs) which will open a door or something, this can be used as a sort of Face activated door or sum like that, i will use it to create a defense system later in the future which will be focused on the intruder "management".

aaaa

  </p>
  
</details>

---

<details style="margin-bottom: 1px;" > 
  <summary><h1> ⚙ Physics and Robotic implementation... </h1></summary>
  <p align="left">


<img align="right" src="media/2.jpg" width="330" />
  
Code....


  </p>
  
</details>

