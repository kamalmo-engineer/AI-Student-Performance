import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLORS = {
    "bg": "#020617",
    "card": "#0f172a",
    "accent": "#38bdf8",
    "secondary": "#818cf8",
    "success": "#22c55e",
    "fail": "#ef4444",
    "warning": "#f59e0b",
    "border": "#1e293b",
    "text_main": "#f8fafc",
    "text_dim": "#94a3b8"
}

ctk.set_appearance_mode("dark")

class StudentAgent(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ AI STUDENT PERFORMANCE HUB")
        self.geometry("1200x850")
        self.configure(fg_color=COLORS["bg"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === LEFT PANEL ===
        self.left_panel = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=0, width=350)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_propagate(False)

        ctk.CTkLabel(self.left_panel, text="📊 DASHBOARD",
                     font=("Impact", 35), text_color=COLORS["accent"]).pack(pady=(40, 10))

        self.att_entry  = self.create_styled_input(self.left_panel, "ATTENDANCE (0-100%)")
        self.study_entry = self.create_styled_input(self.left_panel, "DAILY STUDY HOURS (0-12)")
        self.pass_entry  = self.create_styled_input(self.left_panel, "CLASSWORK MARKS (0-50)")

        self.btn_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.btn_container.pack(pady=30, padx=20, fill="x")

        self.predict_btn = ctk.CTkButton(
            self.btn_container, text="🚀 ANALYZE & PREDICT", command=self.predict,
            font=("Segoe UI", 16, "bold"), height=50, corner_radius=15,
            fg_color=COLORS["accent"], text_color=COLORS["bg"], hover_color=COLORS["secondary"]
        )
        self.predict_btn.pack(fill="x", pady=10)

        self.reset_btn = ctk.CTkButton(
            self.btn_container, text="RESET DATA", command=self.reset,
            font=("Segoe UI", 14), height=40, corner_radius=15,
            fg_color="transparent", border_width=2, border_color=COLORS["fail"],
            text_color=COLORS["fail"], hover_color="#450a0a"
        )
        self.reset_btn.pack(fill="x")

        # === RIGHT PANEL ===
        self.right_panel = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Result card
        self.res_card = ctk.CTkFrame(self.right_panel, fg_color=COLORS["card"],
                                     corner_radius=20, border_width=1, border_color=COLORS["border"])
        self.res_card.pack(fill="x", pady=(0, 20))
        self.result_label = ctk.CTkLabel(self.res_card, text="Waiting for Input Data...",
                                         font=("Segoe UI", 24, "bold"), text_color=COLORS["text_dim"])
        self.result_label.pack(pady=25)

        # Breakdown label (shows contribution of each factor)
        self.breakdown_label = ctk.CTkLabel(self.res_card, text="",
                                            font=("Segoe UI", 13), text_color=COLORS["text_dim"])
        self.breakdown_label.pack(pady=(0, 15))

        # Charts
        self.viz_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.viz_container.pack(fill="x", pady=10)

        self.chart_score = ctk.CTkFrame(self.viz_container, fg_color=COLORS["card"],
                                        corner_radius=20, border_width=1, border_color=COLORS["border"], height=350)
        self.chart_score.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.chart_inputs = ctk.CTkFrame(self.viz_container, fg_color=COLORS["card"],
                                         corner_radius=20, border_width=1, border_color=COLORS["border"], height=350)
        self.chart_inputs.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Problems card — shows detected issues sorted by severity
        self.problems_card = ctk.CTkFrame(self.right_panel, fg_color=COLORS["card"],
                                          corner_radius=20, border_width=1, border_color=COLORS["border"])
        self.problems_card.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(self.problems_card, text="🔍 PROBLEM DETECTION",
                     font=("Segoe UI", 14, "bold"), text_color=COLORS["fail"]).pack(pady=(15, 5))
        self.problems_text = ctk.CTkLabel(self.problems_card, text="",
                                          font=("Segoe UI", 13), text_color=COLORS["text_dim"],
                                          justify="left", wraplength=550)
        self.problems_text.pack(pady=(0, 20), padx=20)

        # Recommendations card
        self.recom_card = ctk.CTkFrame(self.right_panel, fg_color=COLORS["card"],
                                       corner_radius=20, border_width=1, border_color=COLORS["border"])
        self.recom_card.pack(fill="x", pady=20)
        ctk.CTkLabel(self.recom_card, text="💡 STRATEGIC RECOMMENDATIONS",
                     font=("Segoe UI", 14, "bold"), text_color=COLORS["secondary"]).pack(pady=(15, 5))
        self.recom_text = ctk.CTkLabel(self.recom_card, text="Enter your data to receive AI-driven advice.",
                                       font=("Segoe UI", 13), text_color=COLORS["text_dim"],
                                       justify="left", wraplength=550)
        self.recom_text.pack(pady=(0, 20), padx=20)

    def create_styled_input(self, master, label_text):
        container = ctk.CTkFrame(master, fg_color="transparent")
        container.pack(fill="x", padx=35, pady=12)
        ctk.CTkLabel(container, text=label_text,
                     font=("Segoe UI", 11, "bold"), text_color=COLORS["secondary"]).pack(anchor="w", padx=5)
        entry = ctk.CTkEntry(container, height=45, corner_radius=12,
                             fg_color=COLORS["bg"], border_color=COLORS["border"],
                             border_width=2, text_color=COLORS["accent"], font=("Consolas", 16))
        entry.pack(fill="x", pady=5)
        return entry

    # ── helpers ──────────────────────────────────────────────────────────────

    def _calc_score(self, att, std, cw):
        """Return (score, norm_std_pct, norm_cw_pct) and individual contributions."""
        norm_std = min((std / 12) * 100, 100)
        norm_cw  = (cw / 50) * 100
        score = min(max((att * 0.30) + (norm_std * 0.30) + (norm_cw * 0.40), 0), 100)
        c_att = att * 0.30
        c_std = norm_std * 0.30
        c_cw  = norm_cw  * 0.40
        return score, norm_std, norm_cw, c_att, c_std, c_cw

    def _severity_label(self, pct, low, mid):
        if pct < low:
            return "🔴 CRITICAL"
        if pct < mid:
            return "🟡 NEEDS WORK"
        return "🟢 GOOD"

    # ── main predict ─────────────────────────────────────────────────────────

    def predict(self):
        try:
            att = float(self.att_entry.get())
            std = float(self.study_entry.get())
            cw  = float(self.pass_entry.get())
        except ValueError:
            self.result_label.configure(text="⚠️ INVALID INPUT", text_color=COLORS["fail"])
            return

        if not (0 <= att <= 100) or not (0 <= std <= 12) or not (0 <= cw <= 50):
            self.result_label.configure(text="⚠️ DATA OUT OF RANGE", text_color=COLORS["warning"])
            return

        score, norm_std, norm_cw, c_att, c_std, c_cw = self._calc_score(att, std, cw)

        # Status
        status = "SUCCESS" if score >= 50 else "AT RISK"
        color  = COLORS["success"] if score >= 50 else COLORS["fail"]
        self.result_label.configure(text=f"{status}: {score:.1f}%", text_color=color)
        self.res_card.configure(border_color=color)

        # Contribution breakdown
        self.breakdown_label.configure(
            text=f"Attendance: +{c_att:.1f}pt  |  Study: +{c_std:.1f}pt  |  Classwork: +{c_cw:.1f}pt",
            text_color=COLORS["text_dim"]
        )

        self.update_visuals(score, att, norm_std, norm_cw)
        self.detect_problems(att, std, cw, norm_std, norm_cw, score)
        self.generate_recommendations(att, std, cw, norm_std, norm_cw, score)

    # ── visuals ───────────────────────────────────────────────────────────────

    def update_visuals(self, score, att, std_p, cw_p):
        for frame in [self.chart_score, self.chart_inputs]:
            for w in frame.winfo_children():
                w.destroy()

        plt.style.use('dark_background')

        # Donut
        fig1, ax1 = plt.subplots(figsize=(4, 4), facecolor=COLORS["card"])
        ax1.set_facecolor(COLORS["card"])
        color_main = COLORS["success"] if score >= 50 else COLORS["fail"]
        ax1.pie([score, 100 - score], colors=[color_main, COLORS["border"]],
                startangle=90, wedgeprops={'width': 0.3})
        ax1.text(0, 0, f"{int(score)}%", ha='center', va='center',
                 fontsize=30, fontweight='bold', color="white")
        ax1.set_title("OVERALL PROBABILITY", color=COLORS["text_dim"], pad=10)
        FigureCanvasTkAgg(fig1, master=self.chart_score).get_tk_widget().pack(fill="both", expand=True)
        FigureCanvasTkAgg(fig1, master=self.chart_score).draw()

        # Bar chart
        fig2, ax2 = plt.subplots(figsize=(4, 4), facecolor=COLORS["card"])
        ax2.set_facecolor(COLORS["card"])
        categories = ['Attendance', 'Study', 'Classwork']
        values     = [att, std_p, cw_p]
        bar_colors = []
        for v in values:
            if v >= 70:   bar_colors.append(COLORS["success"])
            elif v >= 40: bar_colors.append(COLORS["warning"])
            else:         bar_colors.append(COLORS["fail"])

        ax2.bar(categories, values, color=bar_colors)
        ax2.axhline(y=50, color=COLORS["warning"], linestyle='--', linewidth=1, label='50% threshold')
        ax2.axhline(y=75, color=COLORS["success"], linestyle='--', linewidth=1, label='75% target')
        ax2.set_ylim(0, 100)
        ax2.tick_params(axis='x', colors=COLORS["text_dim"])
        ax2.tick_params(axis='y', colors=COLORS["text_dim"])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.legend(fontsize=8, loc='upper right')
        ax2.set_title("METRICS ANALYSIS", color=COLORS["text_dim"], pad=10)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_inputs)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

    # ── problem detection (NEW) ───────────────────────────────────────────────

    def detect_problems(self, att, std, cw, norm_std, norm_cw, score):
        """
        Identifies which factor is dragging the score down the most,
        calculates the exact point gain if fixed, and sorts by severity.
        """
        problems = []

        # --- Attendance ---
        if att < 75:
            target_att  = 75
            gain        = (target_att - att) * 0.30
            sev         = self._severity_label(att, 50, 75)
            problems.append((gain, (
                f"{sev}  ATTENDANCE  ({att:.0f}%)\n"
                f"   → Raising to {target_att}% would add +{gain:.1f} pts to your score.\n"
                f"   → Missing sessions directly kills this metric (weight: 30%)."
            )))

        # --- Study hours ---
        if norm_std < 67:          # 67% ≈ 8h/12h
            target_std_h   = 4 if std < 4 else 8
            target_norm    = min((target_std_h / 12) * 100, 100)
            gain           = (target_norm - norm_std) * 0.30
            sev            = self._severity_label(norm_std, 33, 67)
            problems.append((gain, (
                f"{sev}  STUDY HOURS  ({std:.1f}h/day)\n"
                f"   → Increasing to {target_std_h}h/day would add +{gain:.1f} pts.\n"
                f"   → Even +1 hour daily makes a measurable difference (weight: 30%)."
            )))

        # --- Classwork ---
        if norm_cw < 70:
            target_cw  = 35          # out of 50
            target_nc  = (target_cw / 50) * 100
            gain       = (target_nc - norm_cw) * 0.40
            sev        = self._severity_label(norm_cw, 50, 70)
            problems.append((gain, (
                f"{sev}  CLASSWORK  ({cw:.0f}/50 = {norm_cw:.0f}%)\n"
                f"   → Reaching {target_cw}/50 would add +{gain:.1f} pts.\n"
                f"   → Classwork has the HIGHEST weight (40%) — fix this first!"
            )))

        if not problems:
            self.problems_text.configure(
                text="✅  No critical issues detected. All metrics are in a healthy range.",
                text_color=COLORS["success"]
            )
            return

        # Sort by gain descending → biggest impact first
        problems.sort(key=lambda x: x[0], reverse=True)

        lines = ["Problems ranked by score impact (highest first):\n"]
        for i, (gain, desc) in enumerate(problems, 1):
            lines.append(f"#{i}  Potential gain: +{gain:.1f} pts\n{desc}")

        self.problems_text.configure(
            text="\n\n".join(lines),
            text_color=COLORS["text_main"]
        )

    # ── recommendations (UPDATED) ─────────────────────────────────────────────

    def generate_recommendations(self, att, std, cw, norm_std, norm_cw, score):
        recoms = []

        # Classwork first — highest weight
        if norm_cw < 70:
            missing = 35 - cw
            recoms.append(
                f"📌 PRIORITY 1 — Classwork ({cw:.0f}/50, weight 40%):\n"
                f"   Submit all pending assignments. You need ~{missing:.0f} more marks to reach 35/50.\n"
                f"   Participate actively — every mark here is worth more than attendance or study."
            )

        # Attendance
        if att < 75:
            sessions_missed_est = int((75 - att) / 5)
            recoms.append(
                f"📌 PRIORITY {'2' if norm_cw < 70 else '1'} — Attendance ({att:.0f}%, weight 30%):\n"
                f"   You need roughly {sessions_missed_est} fewer absences to hit 75%.\n"
                f"   Even partial attendance helps — don't skip full weeks."
            )

        # Study hours
        if norm_std < 67:
            extra = max(1, 4 - std)
            recoms.append(
                f"📌 Study Hours ({std:.1f}h/day, weight 30%):\n"
                f"   Add {extra:.0f}h more per day. Use the Pomodoro method (25 min on / 5 min off).\n"
                f"   Focus on weak subjects first, not revision of already-known material."
            )

        if not recoms:
            self.recom_text.configure(
                text="🌟 Excellent balance! Keep this consistency and you're on track for top grades.",
                text_color=COLORS["success"]
            )
        else:
            self.recom_text.configure(
                text="\n\n".join(recoms),
                text_color=COLORS["text_main"]
            )

    # ── reset ─────────────────────────────────────────────────────────────────

    def reset(self):
        for e in [self.att_entry, self.study_entry, self.pass_entry]:
            e.delete(0, 'end')
        self.result_label.configure(text="Waiting for Input Data...", text_color=COLORS["text_dim"])
        self.breakdown_label.configure(text="")
        self.res_card.configure(border_color=COLORS["border"])
        self.problems_text.configure(text="")
        self.recom_text.configure(text="Enter your data to receive AI-driven advice.")
        for frame in [self.chart_score, self.chart_inputs]:
            for w in frame.winfo_children():
                w.destroy()


if __name__ == "__main__":
    app = StudentAgent()
    app.mainloop()
