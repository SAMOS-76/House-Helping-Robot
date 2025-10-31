# 🤖 House Helping Robot (HHR)

<img width="496" height="815" alt="image" src="https://github.com/user-attachments/assets/049c0b8a-0aba-4e15-b816-8a07cdb4b5fc" />


A personal robotics project designed to assist with everyday tasks in the home or care environments.  
The **House Helping Robot (HHR)** combines mechanical design, computer vision, and voice control to create an accessible, affordable, and collaborative robotic assistant.

---

## 📘 Background

### Personal Robotics  
Personal robots enable automation of repetitive or labor-intensive tasks in both domestic and professional settings.  
The goal of HHR is to make such automation **accessible, affordable, and practical** — inspired by systems like the Toyota HSR.

---

## 🎯 Aims

- **Easy to Use** – Operable by anyone without complex training.  
- **Cheap & Reliable** – Designed with affordability in mind, enabling scalability (e.g., multiple robots in a care home).  
- **Manoeuvrable** – Compact enough to navigate typical household spaces and avoid obstacles.  
- **Collaborative** – Built to **assist**, not replace, caregivers or nurses.

---

## ⚙️ How It Works

1. User gives a simple command — e.g. `"Grab the vase"`.
2. The robot:
   - Uses **object recognition** to identify the target.  
   - Calculates **distance** with a **depth camera**.  
   - Applies **inverse kinematics** to position its arm precisely.
3. The robotic arm then retrieves the object.

📹 *Demo:*  
https://github.com/user-attachments/assets/4dac9671-ce60-41e7-9f48-af2dfbe0eda8


---

## 💰 Cost & Materials

- **Frame:** Aluminium extrusion for modularity and strength.  
- **Custom Parts:** 3D printed (PLA and TPU) for cost-effective and quick manufacturing.  
- **Design Priority:** Maintain structural integrity while minimizing cost and weight.

---

## 🚗 Manoeuvrability

- Base width under **45 cm**, allowing smooth passage through standard doorways.  
- **Low center of mass** for exceptional stability.  
- Thin and strong aluminium frame ensures both rigidity and compactness.

---

## 🗣️ Control System

Initially tested various control methods such as remote controls, but these proved unsuitable for users with limited dexterity.  
Final design uses **voice activation** with **Natural Language Processing (NLP)** for intuitive control.

---

## 🧩 Mechanical Design

### ⭕ Wheel System
- **Material:** PLA (wheels) + TPU (tyres)  
- **Drive:** Gear system connects directly to motor shaft via 8 mm threaded rod  

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f56afff-fb4a-4cf4-8f83-0d01a1986fa5" width="45%" />
  <img src="https://github.com/user-attachments/assets/2c517d7a-700d-44dc-8dfa-5934cfdbdc11" width="45%" />
</p>


### 🧱 Frame
- **20 × 20 mm aluminium extrusions** form the main base structure  
- **20 × 80 mm center extrusion** supports the robotic arm and electronics  

<img width="898" height="546" alt="image" src="https://github.com/user-attachments/assets/f9137579-44ef-4b88-b4fd-36d9d7807e75" />


### 🤖 Robotic Arm
- Fully **3D-printed PLA** arm mounted to the aluminium frame  
- Custom-designed except for the open-source gripper [**James Bruton**](https://www.youtube.com/watch?v=5RxZzuLiMdA&list=PLpwJoq86vov-vjlb1OEefk8BDxUmujIxM&index=10)

<img width="695" height="878" alt="image" src="https://github.com/user-attachments/assets/876b0a42-6941-4b0b-b606-80622819e8b7" />


---

## 🧮 Inverse Kinematics

Used **Jacobian Inverse Kinematics** to determine servo angles that position the arm and gripper.  
Ensures coordinated movement between **shoulder** and **elbow** joints to keep the wrist properly aligned.

📹 *Inverse Kinematics Test:*  
<img width="517" height="920" alt="image" src="https://github.com/user-attachments/assets/c9803d78-0510-47ed-ba7f-b9c9a605d6a2" />
<img width="420" height="748" alt="image" src="https://github.com/user-attachments/assets/b3591c05-f3f9-41f2-b96e-7d98a31d76fa" />


---

## 🔌 Electrical Design

### Communication Architecture
- **Serial connection** between Raspberry Pi 4 and Arduino Nano for fast, interference-free data transfer.

### Arm Electronics
- Multiple servos controlled via **servo driver** board for simplified wiring and expandability.

### Base Electronics
- **Motor Driver:** BTS7990  
- **Motors:** High-torque DC motors  
- **Power Distribution:** Centralized via custom protoboard and controllers

🖼️ *Electronics Diagram:*  
![Electronics Diagram](media/images/electronics-diagram.jpg)

---

## 💻 Software Overview

### Object Recognition
- Utilizes **YOLO** algorithm with **Intel RealSense SDK** for real-time object detection and depth measurement.  
- Provides accurate distance data crucial for arm precision.

📹 *Object Detection Test:*  
[![YOLO + RealSense Test](media/images/object-detection-thumb.jpg)](media/videos/object-detection.mp4)

### Motion Control
- Early **speed testing** helped tune servo and motor response to prevent vibration and mechanical stress.  
- **Motor test** verified stability and smooth operation even at higher speeds.

📹 *Motor Test:*  
[![Motor Test Video](media/images/motor-test-thumb.jpg)](media/videos/motor-test.mp4)

---

## 🧠 Dataflow Diagram

The system processes:
- Speech recognition  
- Object detection  
- Robotic arm & base control  
- Depth perception  
- Servo feedback loops  

![Dataflow Diagram](media/images/dataflow-diagram.jpg)

---

## 🧪 Testing

- **Arm Speed Test:** Tuned for smooth, vibration-free motion  
- **Inverse Kinematics Test:** Verified accuracy of arm articulation  
- **Motor & Control Tests:** Confirmed stability and reliability  

📹 *Robot in Action:*  
[![Full System Test](media/images/system-test-thumb.jpg)](media/videos/full-system-test.mp4)

---

## 🏁 Results

✅ Stable navigation  
✅ Reliable object handling  
✅ Responsive voice control  

![Completed HHR](media/images/completed-hhr.jpg)

---

## 🚀 Future Improvements

- Enhance **aesthetics** and enclosure design  
- Optimize **software performance** and add **autonomous navigation**  
- Expand **gripper functionality** for a wider range of tasks  

---

## 🧩 Conclusion

> I truly believe this project has the potential to **improve quality of life** for people at home and in care facilities — not by replacing human care, but by supporting it.

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Brain** | Raspberry Pi 4 + Arduino Nano |
| **Vision** | Intel RealSense Camera + YOLO Object Detection |
| **Structure** | Aluminium Extrusion + 3D-Printed PLA & TPU |
| **Control** | Python, Serial Communication, NLP Voice Commands |
| **Motion** | High-Torque DC Motors, BTS7990 Driver, Servo Actuators |

---

## 📸 Media

📂 Project file structure suggestion:
