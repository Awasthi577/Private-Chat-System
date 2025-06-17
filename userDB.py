from models import User
from database import SessionLocal

def create_and_store_user(username: str, password: str):
    session = SessionLocal()
    try:
        user = User.create_user(username=username, password=password)
        session.add(user)
        session.commit()
        print(f"User {username} created with id {user.id}")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()


create_and_store_user("sneha", "sneha_june05")
create_and_store_user("sushant", "Sushant@123")

