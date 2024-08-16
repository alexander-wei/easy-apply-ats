from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from . import models

DEBUG = False

try:
    engine = create_engine(
        "mysql+pymysql://root:1234@127.0.0.1:3306/jobapps?charset=utf8mb4", echo=False
    )

    if DEBUG:
        with engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            print(result.all())

    models.metadata_obj.create_all(engine)
except:
    pass
