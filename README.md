# VidyAI++ – Multilingual AI Tutoring

## **Selected Domain**: AIML

## **Problem Statement / Use Case**: 
VidyAI++ is an AI-powered, multilingual education platform designed to transform learning for underprivileged (BPL) students in government schools across India. It provides personalized tutoring and mentorship that adapts to the learner's language, skill level, emotional state, and learning style, ensuring engaging and accessible education.

---

## **Abstract / Problem Description**:

VidyAI++ is an innovative platform aimed at bridging the educational divide for underprivileged students in India. Leveraging cutting-edge technologies in artificial intelligence (AI), machine learning (ML), and computer vision, VidyAI++ provides a comprehensive, multilingual tutoring system that tailors learning to the individual needs of each student. 

The platform focuses on creating a learning environment that is not only educational but also emotionally engaging. It tracks student engagement through emotion recognition and fatigue detection, adjusting lessons and content delivery to maintain focus and improve the learning experience. The use of AI tutoring modules like Gemini or GPT enables the delivery of localized content in various Indian languages, ensuring that students receive lessons in their native language for better comprehension.

VidyAI++ also integrates a mentorship system, matching students with mentors who are regionally and emotionally compatible, further enhancing the learning experience. The inclusion of gamified learning elements like micro-certifications, digital badges, and skill heatmaps adds motivation and a sense of achievement to the educational journey.

Key features of the platform include:
- AI tutoring in Indian languages (Gemini/GPT).
- Real-time adaptive learning based on student performance.
- Emotion, eye movement, and fatigue detection using OpenCV and DeepFace.
- AI-driven mentor matchmaking for personalized mentorship.
- Gamified learning environment with badges and certifications.
- Intuitive, multilingual user interface with zero literacy barriers.

By using VidyAI++, underprivileged students will have the tools and support needed to succeed in their education, irrespective of their background.

---

## **Features**:

1. **AI Tutoring in Indian Languages**:
   - Using Gemini/GPT for localized content and quizzes (text + voice).
   - Students can interact in their native language, making learning more relatable and effective.
   
2. **Real-Time Adaptive Learning**:
   - Lessons adjust based on student performance and behavior.
   - AI adapts the difficulty of the lessons dynamically, ensuring the student is always challenged but not overwhelmed.
   
3. **Emotion-Based Engagement Tracking**:
   - Vision-based emotion tracking via OpenCV and DeepFace to monitor student engagement, eye movement, and fatigue levels.
   - Helps the system detect if a student is losing focus or getting tired, adjusting the lesson accordingly.
   
4. **AI Mentor Matchmaking**:
   - Matches students with regionally and emotionally compatible mentors, ensuring effective guidance and emotional connection.
   
5. **Gamified Learning**:
   - Rewards students with micro-certifications, digital badges, and skill heatmaps to track progress and keep them motivated.
   
6. **Zero Literacy Barrier UI**:
   - Designed for users with limited literacy skills, the platform features intuitive visuals, voice navigation, and multilingual support.
   
7. **Personalized Learning Styles**:
   - The system personalizes learning based on whether the student learns best visually, auditorily, or kinesthetically.
   
8. **Comprehensive Student Data Handling**:
   - Profiles and academic data are securely stored and processed using MySQL, ensuring privacy and ease of access.
   
9. **Mentorship Integration via Google Meet API**:
   - Students can schedule and participate in live mentorship sessions with their assigned mentors.

---

## **Technology Stack**:

### Front-End Development:
- **HTML, CSS, JavaScript**: 
   - Responsive and user-friendly interface, optimized for diverse student needs, ensuring that it is easy to navigate and interact with.

### Back-End & Server-Side:
- **Python**:
   - AI modules for content delivery, student performance tracking, and backend logic.
   
- **Firebase**:
   - Real-time database management, authentication, and cloud storage for student profiles, preferences, and educational data.
   
- **SMTP (Mail Server)**:
   - Sends notifications, alerts, and performance reports to students and mentors.

### AI & Personalization:
- **Gemini AI (or GPT)**:
   - Powers multilingual tutoring and localized content delivery (both text and voice) to cater to regional linguistic differences.
   
- **OpenCV + DeepFace**:
   - Emotion, eye movement, and fatigue detection using computer vision to adjust learning content in real-time based on student engagement.

### Integration & Collaboration:
- **Google Meet API**:
   - Facilitates the scheduling and conducting of live mentorship and tutoring sessions, creating an interactive and collaborative learning environment.

### Database & Data Handling:
- **MySQL**:
   - Secure storage for student data, including academic history, preferences, and personal details.

### Deployment Tools:
- **Render**: 
   - For hosting the backend and front-end components, ensuring seamless scalability and availability.
   
- **GitHub**: 
   - For version control and collaboration, allowing easy updates and maintenance of the codebase.
   
- **Median.io**: 
   - To create and manage the visual media components used for tutoring and mentorship sessions.

---


