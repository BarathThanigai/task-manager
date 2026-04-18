from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg://postgres:barathbarath_2006@localhost:5432/task_manager')

print("Users:")
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row._asdict())

print("\nTasks:")
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM tasks"))
    for row in result:
        print(row._asdict())