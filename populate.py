import json
from models import Participant
from app import db
import qrcode

count = 1

os.environ["DATABASE_URL"] = settings.DATABASE_URL

with open("HooHacks_Users.json") as f:
    for line in f:
        d = json.loads(line)
        if (d['status']['confirmed']):
            ct = Participant.query.get(email=d['email']).count()
            print(ct)
            # if ct == 0:
            #     p = Participant(d['profile']['name'],
            #         count, d['email'], d['confirmation']['phoneNumber'],
            #         d['confirmation']['dietaryRestrictions'])
            #     img = qrcode.make('Some data here')
            #     file_name = "QR/" + d['profile']['name']
            #     file_name = "_".join(file_name.split())
            #     file_name +=  ".jpg"
            #     img.save(".jpg")
            #     db.session.add(p)
            #     db.session.commit()
            #     print(d['profile']['name'])
            #     count+=1
            #     print(count)
