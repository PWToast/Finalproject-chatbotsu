# from sqlalchemy.orm import Session
# from sqlalchemy import func, select

# engine = create_engine('mysql+pymysql://user:pass@localhost/dbname')

# def is_new_line_user(line_user_id):
#         statement = select(User).where(User.line_user_id == line_id)
#         result = session.scalar(statement)
#         if(result):
#             return False
#         else:
#             new_user = User(line_user_id=line_id_from_webhook, platform="line", timestamp=....)
#             session.add(new_user)
#             session.commit()

#         return True
