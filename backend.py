import json
data_base = []

def append_obj(event, orderOf):
    obj = {
        'sender_id':event['sender_id'],
        'time' : event['time'],
        'bank_id' : event['bank_id'],
        'status' : 0,
        'left' : orderOf
    }
    data_base.append(obj)

def order(event):
    if not user_exits(event):
        orderOf = len(data_base)
        append_obj(event, orderOf)
        # print (data_base)
        return list(filter(lambda x: x['sender_id'] == event['sender_id'], data_base))[0]
    else:
        return ("error")

def user_exits(event):
    exists = False
    for i in range(len(data_base)):
            if event['sender_id'] == data_base[i]['sender_id']:
                exists = True
    return exists

def delete(event):
    for i in range(len(data_base)):
        if event['sender_id'] == data_base[i]['sender_id']:
            index = data_base[i]['left']
    i = 0
    del(data_base[i])
    print ('delete2')
    for i in range(len(data_base)):
        data_base[i]['left'] = i
    return('success')

def know_order(event):
    if len(data_base) != 0:
        if user_exits(event):
            return list(filter(lambda x: x['sender_id'] == event['sender_id'], data_base))[0]
        else:
            return ("error")
        # return data_base
    else:
        return ("error")

    # for i in range(len(data_base)):
    #     if data_base[i]['status'] == 1:
    #         data_base[i]['left'] =  left
    #         del(data_base[i])
    #         print (left)
    # append_obj(event)
    # print (data_base)
    return data_base


def lambda_handler(event, context):
    if event['procedure'] == 'take_order':
        print ('take_order')
        ret = order(event)
        ret = json.loads(json.dumps(ret))
        return ret
    elif event['procedure'] == 'know_order':
        print ('know_order')
        ret = know_order(event)
        ret = json.loads(json.dumps(ret))
        return ret
    elif event['procedure'] == 'delete':
        print ('delete1')
        ret = delete(event)
        ret = json.loads(json.dumps(ret))
        return ret
    elif event['procedure'] == 'changeStatus':
        del(data_base[0])
		for i in range(len(data_base)):
			data_base[i]['left'] = i
        # ret = delete(event)
        # ret = json.loads(json.dumps(ret))
        return ("y")
    else:
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        ret = son.loads(json.dumps('ne pravilnaya procedurka'))
        return ret
