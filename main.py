import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def user(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    cred = credentials.Certificate('desafioribon-firebase-adminsdk-15ik6-059fcfb142.json')
    firebase_admin.initialize_app(cred, {'databaseURL':'https://desafioribon.firebaseio.com/'}, 'um-nome-novo')
    request_json = request.get_json()
    if request.method == 'POST':
    	call_type = request.args.get('call_type')
    	user = request.args.get('user_id')
    	if call_type is 'collected_coin':
    	    ref = db.reference('collected_coins')
    	    value = request.args.get('value')
    	    ref.push({
    	        'user_id':user,
    	        'value':value
    	    })
    	    ref_user = db.reference('users/'+user)
    	    user = ref_user.get()
    	    coins = 1
    	    if user.get('coins') is not None:
    	        coins += int(user.get('coins'))
    	    ref_user.update({'coins':str(coins)})
            if coins == 1 or coins == 100 or coins == 1000 or coins == 10000 or coins == 100000:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user, 'trophy':str(coins)+' coins'})
    	    
    	    
    	elif call_type is 'killed_monster':
    	    ref = db.reference('killed_monsters')
    	    monster = request.args.get('monster')
    	    ref.push({
    	        'user_id':user,
    	        'monster_id':monster
    	    })
    	    ref_user = db.reference('users/'+user)
    	    user = ref_user.get()
    	    monsters = 1
    	    if user.get(monster) is not None:
    	        monsters += int(user.get(monster))
    	    ref_user.update({monster:str(monsters)})
    	    ref_monster=db.reference('monsters/'+monster)
    	    monster_name = ref_monster.get().get('name')
            if monsters == 1 or monsters == 100 or monsters == 1000 or monsters == 10000 or monsters == 100000:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user, 'trophy':str(monsters)+" "+monster_name+" monsters killed"})
                
    	elif call_type is 'death':
    	    ref = db.reference('deaths')
    	    timestamp = request.args.get('timestamp')
    	    ref.push({
    	        'user_id':user,
    	        'timestamp':timestamp
    	    })
    	    ref_user = db.reference('users/'+user)
    	    user = ref_user.get()
    	    deaths = 1
    	    if user.get('deaths') is not None:
    	        deaths += int(user.get('deaths'))
    	    ref_user.update({'deaths':str(deaths)})
            if deaths == 1 or deaths == 10 or deaths == 25 or deaths == 50 or deaths == 100:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user, 'trophy':"You died "str(deaths)+" times"})   
        
        return f"OK" 	    
    	
    else:
        return f'Not supported operation'

