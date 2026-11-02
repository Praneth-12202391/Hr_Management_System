import sqlite3
from pathlib import Path

DB_PATH = Path(r"D:\H2\MAnaging Portal\backend\data\talentpulse.db")

def prune_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Identify Demo Logins & 3 Random Employees
    demo_emails = [
        "superadmin@talentpulse.local",
        "admin@talentpulse.local",
        "hr@talentpulse.local",
        "manager@talentpulse.local",
        "manager2@talentpulse.local",
        "employee@talentpulse.local"
    ]
    
    # 3 random employees (one of them is Praneeth Rao!)
    random_employee_emails = [
        "sai.prasad10@talentpulse.local",
        "praneeth.rao11@talentpulse.local",
        "ananya.sharma16@talentpulse.local"
    ]
    
    keep_emails = demo_emails + random_employee_emails
    
    placeholders = ",".join("?" for _ in keep_emails)
    cursor.execute(f"SELECT id, email, full_name, role FROM users WHERE email IN ({placeholders})", keep_emails)
    retained_users = cursor.fetchall()
    retained_user_ids = [u[0] for u in retained_users]
    
    print(f"Retained Users ({len(retained_users)}):")
    for u in retained_users:
        print(f"  - ID {u[0]}: {u[1]} ({u[2]}, Role: {u[3]})")

    # Find retained employee IDs
    u_placeholders = ",".join("?" for _ in retained_user_ids)
    cursor.execute(f"SELECT id, user_id, employee_code, job_title FROM employees WHERE user_id IN ({u_placeholders})", retained_user_ids)
    retained_employees = cursor.fetchall()
    retained_emp_ids = [e[0] for e in retained_employees]
    
    print(f"\nRetained Employees ({len(retained_employees)}):")
    for e in retained_employees:
        print(f"  - Emp ID {e[0]} (User ID {e[1]}): {e[2]} - {e[3]}")

    emp_placeholders = ",".join("?" for _ in retained_emp_ids)

    # Begin transaction
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    # 2. Prune child tables
    cursor.execute(f"DELETE FROM survey_responses WHERE employee_id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_survey = cursor.rowcount

    cursor.execute(f"DELETE FROM onboarding_tasks WHERE employee_id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_onboard = cursor.rowcount

    cursor.execute(f"DELETE FROM leave_requests WHERE employee_id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_leaves = cursor.rowcount

    cursor.execute(f"DELETE FROM performance_reviews WHERE employee_id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_reviews = cursor.rowcount

    cursor.execute(f"DELETE FROM attrition_scores WHERE employee_id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_attrition = cursor.rowcount

    cursor.execute(f"DELETE FROM chat_messages WHERE user_id NOT IN ({u_placeholders});", retained_user_ids)
    del_chat = cursor.rowcount

    cursor.execute(f"DELETE FROM notifications WHERE user_id NOT IN ({u_placeholders});", retained_user_ids)
    del_notif = cursor.rowcount

    # 3. Prune employees table
    cursor.execute(f"DELETE FROM employees WHERE id NOT IN ({emp_placeholders});", retained_emp_ids)
    del_employees = cursor.rowcount

    # 4. Prune users table
    cursor.execute(f"DELETE FROM users WHERE id NOT IN ({u_placeholders});", retained_user_ids)
    del_users = cursor.rowcount

    # Commit changes
    conn.commit()
    cursor.execute("VACUUM;")
    conn.close()

    print("\n[+] Pruning Completed Successfully:")
    print(f"  - Deleted {del_users} non-essential users (retained {len(retained_users)})")
    print(f"  - Deleted {del_employees} non-essential employees (retained {len(retained_employees)})")
    print(f"  - Deleted {del_leaves} leave records")
    print(f"  - Deleted {del_reviews} review records")
    print(f"  - Deleted {del_attrition} attrition score records")
    print(f"  - Deleted {del_survey} survey response records")
    print(f"  - Preserved all departments and policy documents for RAG Helpdesk")

if __name__ == "__main__":
    prune_db()
