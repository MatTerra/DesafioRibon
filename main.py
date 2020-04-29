import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def trophyAPI   (request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # Initialize DB connection
    cred = credentials.Certificate('desafioribon-firebase-adminsdk-15ik6-059fcfb142.json')
    try:
        firebase_admin.initialize_app(cred, {'databaseURL':'https://desafioribon.firebaseio.com/'})
    except:
         firebase_admin.get_app()
    # Get request payload as JSON     
    request_json = request.get_json()
    #Check if POST was made
    if request.method == 'POST':
        # Get call type and user ID and validate values
        call_type = request_json.get('call_type')
        user = request_json.get('user_id')
        if call_type is None:
            return f"Call type not defined"
        if user is None:
            return f"User ID not defined"
        # Get user DB reference and validate ID
        ref_users = db.reference('users')
        user_ref = ref_users.order_by_child('id').equal_to(user).get()
        if len(user_ref) == 0 and not (call_type == 'new_user' or call_type == 'new_monster') :
            return f'Invalid User ID'
        
        if call_type == 'new_user':
            # Verify if ID is taken
            if not len(user_ref) == 0:
                return f'ID Unavailable'
            # Get DB reference
            ref = db.reference('users')
            # Register new user
            new_user = ref.push({"id" : user})
            return (f'Ok - '+new_user.key+f' registered with id '+user)
        if call_type == 'new_monster':
            return f"Not implemented yet, monster not registered"  
              
        # Get DB ID for user
        user_obj = user_ref.popitem()
        user_id = user_obj[0]
        ref_user = db.reference('users/'+user_id)
            
        if call_type == 'collected_coin':
            # Get DB reference
            ref = db.reference('collected_coins')
            # Get coin value and validate value
            value = request_json.get('value')
            if value is None:
                return f"Missing coin value"
            # Register collected coin
            ref.push({
                'user_id':user_id,
                'value':value
            })
            # Get user coins
            user_coins = user_obj[1].get('coins')
            coins = 1
            # Check if user already has coins
            if user_coins is not None:
                coins += int(user_coins)
            # Updates user coins
            ref_user.update({'coins':str(coins)})
            # Check for trophy amount
            if coins == 1 or coins == 100 or coins == 1000 or coins == 10000 or coins == 100000:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user_id, 'trophy':str(coins)+' coins'})
            return f'OK - Coin Added'
            
        elif call_type == 'killed_monster':
            # Get DB reference
            ref = db.reference('killed_monsters')
            # Get monster name
            monster = request_json.get('monster')
            # Get monster DB reference and validade name
            ref_monsters = db.reference("monsters")
            monster_ref = ref_monsters.order_by_child('name').equal_to(monster).get()
            if len(monster_ref) == 0:
                return f'Invalid Monster Name'
            # Get DB ID for monster
            monster_obj = monster_ref.popitem()
            monster_id = monster_obj[0]
            # Register killed monster
            ref.push({
                'user_id':user_id,
                'monster_id':monster_id
            })
            # Get user killed monsters
            user_monsters = user_obj[1].get(monster)
            monsters = 1
            # Check if user already killed monsters
            if user_monsters is not None:
                monsters += int(user_monsters)
            # Update user kills
            ref_user.update({monster:str(monsters)})
            # Check for trophy amount
            if monsters == 1 or monsters == 100 or monsters == 1000 or monsters == 10000 or monsters == 100000:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user_id, 'trophy':str(monsters)+" "+monster+" monsters killed"})
            return f'OK - Monster Kill added'
                
        elif call_type == 'death':
            # Get DB reference
            ref = db.reference('deaths')
            timestamp = request_json.get('timestamp')
            # Register death
            ref.push({
                'user_id':user_id,
                'timestamp':timestamp
            })
            # Get user deaths
            user_deaths = user_obj[1].get('deaths')
            deaths = 1
            # Check if user already died
            if user_deaths is not None:
                deaths += int(user_deaths)
            # Update user deaths
            ref_user.update({'deaths':str(deaths)})
            # Check for trophy amount
            if deaths == 1 or deaths == 10 or deaths == 25 or deaths == 50 or deaths == 100:
                ref_trophy = db.reference('received_trophies')
                ref_trophy.push({'user_id':user_id, 'trophy':"Died "+str(deaths)+" times"})
            return f"OK - Death added"
        return f"Invalid Call Type - "+call_type
        
    else:
        return f'Not supported operation'

