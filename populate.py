import json
from models import Participant
from app import db
import settings
import qrcode

count = 1

os.environ["DATABASE_URL"] = settings.DATABASE_URL


        # if (d['status']['confirmed']) and not d['profile']['school'] == "University of Virginia-Main Campus" and not d['profile']['school'] == "Thomas Jefferson High School for Science and Technology":
        #     # ct = Participant.query.get(email=d['email']).count()
        #     print(d['profile']['name'])
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
