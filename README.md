# 🧠 Blink: Intelligent Safety Monitoring for Independent Living

**Blink** is designed to be an extra set of eyes for people who live alone or experience difficulties in mobility and cognition — such as elderly individuals with dementia.  
It provides **real-time monitoring**, **contextual understanding**, and **privacy-preserving emergency alerts** using computer vision and natural interaction.

---

## ⚙️ How It Works

Morpheus continuously monitors whether a person has been **motionless for an extended period** using a simple web camera.  
If a lack of movement is detected, it assumes a **potential alert state** and performs **cross-verification** using voice interaction.  

When the situation is confirmed to be dangerous, Morpheus:
- Sends **de-identified images** and **status information** to emergency services  
- Notifies the **caregiver** in real-time via secure alert message  
- Logs contextual information for post-event analysis  

---

## 🧩 Technologies Used

- **ETRI Human State Understanding API** — detects human posture and motion state  
- **ETRI Face De-identification API** — ensures privacy by blurring or anonymizing faces  
- **Python (Flask)** backend with API orchestration and state detection logic  
- **Twilio API** for caregiver SMS notifications  
- **OpenCV** for video frame analysis  

---

## 💡 Motivation

With the rapid growth of the aging population and the number of elderly people living alone,  
there is an urgent need for **non-intrusive and privacy-aware assistive technology**.  

Morpheus offers a **timely, compassionate, and accessible solution** — bridging AI safety monitoring and human-centered care for individuals who lack immediate supervision.

---

## 🏆 Impact

> **Impact:** Enabled autonomous fall detection and emergency notification for independent seniors,  
> providing peace of mind for families and caregivers.  
> **Recognized for innovation in human-centered AI safety design.**

---

> *“AI that watches over — not watches.”*
