def Send_Otp_Code(*, phone_number, message):
    print(message + "" + phone_number)
    # try:
    #     api = KavenegarAPI("61535137624C4B30383758576C77624C5774772F36315133764D4B6D57786C746F356F392F3967757145493D")
    #     params = {"sender": "", "receptor": phone_number, "message": message}
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)
