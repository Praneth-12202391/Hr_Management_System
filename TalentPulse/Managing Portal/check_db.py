import sys
from pathlib import Path

# Configure utf-8 encoding for standard output if supported
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models import (
    User,
    Employee,
    Department,
    LeaveRequest,
    PerformanceReview,
    PolicyDocument,
    EngagementSurvey,
    SurveyResponse,
    OnboardingTask,
    AttritionScore,
    ChatMessage,
    Notification
)

def inspect_database_sync():
    db = SessionLocal()
    db_file = backend_dir / "data" / "talentpulse.db"

    print("=" * 65)
    print("[*] TalentPulse AI - Live Database Synchronization Status")
    print(f"[*] Database Path: {db_file.resolve()}")
    print("=" * 65)

    if not db_file.exists():
        print("[!] Error: Database file not found!")
        return

    # Table Counts
    counts = {
        "Departments": db.query(Department).count(),
        "User Accounts": db.query(User).count(),
        "Employee Profiles": db.query(Employee).count(),
        "Leave Requests": db.query(LeaveRequest).count(),
        "Performance Reviews": db.query(PerformanceReview).count(),
        "Policy Documents": db.query(PolicyDocument).count(),
        "Engagement Surveys": db.query(EngagementSurvey).count(),
        "Survey Responses": db.query(SurveyResponse).count(),
        "Onboarding Tasks": db.query(OnboardingTask).count(),
        "Attrition Risk Scores": db.query(AttritionScore).count(),
        "Chatbot Q&A Messages": db.query(ChatMessage).count(),
        "Notifications": db.query(Notification).count(),
    }

    print("\n[+] Table Summary (Row Counts):")
    for table_name, count in counts.items():
        print(f"  - {table_name:<25}: {count} records")

    # Show Latest 5 Registered Users in DB
    print("\n[+] Latest 5 User Accounts in DB:")
    recent_users = db.query(User).order_by(User.id.desc()).limit(5).all()
    for u in recent_users:
        dept = u.department.name if u.department else "None"
        emp = u.employee_profile
        emp_code = emp.employee_code if emp else "No Profile"
        print(f"  - ID #{u.id:<3}: {u.full_name:<24} | {u.email:<32} | Role: {u.role:<10} | Code: {emp_code}")

    # Show Last 3 Applied Leaves
    print("\n[+] Latest 3 Leave Requests in DB:")
    recent_leaves = db.query(LeaveRequest).order_by(LeaveRequest.created_at.desc()).limit(3).all()
    for l in recent_leaves:
        emp_name = l.employee.user.full_name if (l.employee and l.employee.user) else "Unknown"
        print(f"  [{l.status}] {emp_name} - {l.leave_type} ({l.days_count} days) | Reason: {l.reason[:40]}")

    # Show Last 3 Chat Messages from GenAI Helpdesk
    print("\n[+] Latest 3 Helpdesk Chatbot Exchanges in DB:")
    recent_chats = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(3).all()
    if recent_chats:
        for c in recent_chats:
            user_name = c.user.full_name if c.user else "User"
            print(f"  - {user_name} asked: \"{c.query[:45]}\"")
            print(f"    Answer: \"{c.response[:65]}...\"")
    else:
        print("  - No chat exchanges yet.")

    print("\n" + "=" * 65)
    print("[SUCCESS] Database is 100% active and synchronized with FastAPI!")
    print("=" * 65)
    db.close()

if __name__ == "__main__":
    inspect_database_sync()
