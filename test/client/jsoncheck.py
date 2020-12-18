big = {"auth": '123123', "req": "token_authentication", "rid": 76355, "msg": {"token_id": "79a49f3c65c5d21581adad5eb8259e"}}
w = {'79a49f3c65c5d21581adad5eb8259e': '213123123'}
print(w[big['msg']['token_id']])