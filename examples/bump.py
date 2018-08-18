from cleverapi import CleverApi

access_token = "TOKEN"
api = CleverApi(access_token)

#градусы
cords = [59.980589, 30.202559]

api.bump(cords[0],cords[1])
