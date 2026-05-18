# AI-Student-Performance

An advanced desktop application built with **CustomTkinter** and **Matplotlib** designed to analyze, predict, and optimize student academic performance. The system evaluates attendance, study hours, and classwork marks to provide real-time predictive analytics and actionable feedback.

## 🚀 Features

*   **Predictive Analytics:** Calculates the overall success probability based on weighted academic metrics.
*   **Dynamic Visualizations:** Integrates Matplotlib charts (Donut charts for probability and Bar charts for metric analysis) directly into the dark-themed GUI.
*   **Intelligent Problem Detection:** Automatically scans student data, identifies critical bottlenecks, and ranks them by their potential score impact.
*   **Strategic Recommendations:** Generates targeted, actionable advice (e.g., specific assignment targets, attendance adjustments, and time-management strategies like Pomodoro).
*   **Modern UI/UX:** Styled using a sleek custom dark-mode theme matching modern developer dashboards.

## 📊 Core Algorithm Weights

The system computes the overall score using the following academic distribution:

$$\text{Final Score} = (\text{Attendance} \times 0.30) + (\text{Normalized Study Hours} \times 0.30) + (\text{Normalized Classwork} \times 0.40)$$

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/kamalmo-engineer/AI-Student-Performance.git](https://github.com/kamalmo-engineer/AI-Student-Performance.git)
   cd AI-Student-Performance
