from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/speaker_verification", echo=True)

with open('unknown_speaker.wav', mode='br') as known:
    data_bytes = known.read()
    data_type = type(data_bytes)
    known.close()

with Session(engine) as session:
    result = session.execute(
        text("UPDATE public.old_person SET audio=:audio WHERE id_old_person=:id"),
        [{"id": 5, "audio": data_bytes}],
    )
    session.commit()
