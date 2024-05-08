from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import database
import function

app = FastAPI()

progress_order={}


@app.post("/")
async def handle_request(request:Request):
    req=await request.json()
    
    #extrac the information from json file :
    inten=req['queryResult']['intent']['displayName']
    parametres=req['queryResult']['parameters']
    output=req['queryResult']['outputContexts']
    session_id=function.get_session_id(output[0]['name'])
    
    #resent the respon
    if inten=="track.order:ongoing-track":
        return track_order(parametres)
    elif inten=="order.add:ongoing-order":
        return add_order(parametres,session_id)
    else:
        inten=="order.complete:ongoing -order"
        return complete_order(parametres,session_id)
        
     
def track_order(parametres:dict):
    order_id=int(parametres['order_id'])
    status=database.get_order(order_id)
        
    if status:
        fulfillmenttext = f'your order status for order id: {order_id}  is {status}'   
    else:
        fulfillmenttext=f" your  ordre id: {order_id} not found"
            
    return JSONResponse (content={'fulfillmentText':fulfillmenttext })


def add_order(parameters:dict,session_id:str):
    pharmacy_item=parameters['Pharmacy-items']   
    quan=parameters['number'] 
    
    if len(pharmacy_item)!=len(quan):
        fulfillmenttext="sorry I did't understant,pls specify  pharmacy item and quantities clearly"
        
    else:
        old_order_items=dict(zip(pharmacy_item,quan))
        if session_id in progress_order:
            new_item=progress_order[session_id]
            new_item.update(old_order_items)
            progress_order[session_id]=new_item
        else:
            progress_order[session_id]=old_order_items
        
        
            
          
    order_str=function.get_string_from_dict(progress_order[session_id]) 
    fulfillmenttext=f"So far you have: {order_str}. Do you need anything else?"
    
    
    
    return JSONResponse (content={'fulfillmentText':fulfillmenttext})


def complete_order(parameters:dict,session_id:str):
    if session_id not in progress_order:
        fulfillmenttext="I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        
    else:
        actual_order=progress_order[session_id]
        next_order_id=save_in_database(actual_order)
        #next_order_id=database.next_order_id()
    
        
        if next_order_id == -1:
            fulfillmenttext = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total=database.total_order_price(next_order_id)
            fulfillmenttext = f"Awesome. We have placed your order. " \
                           f"Here is your order id :{next_order_id}. " \
                           f"Your order total is {order_total} which you can pay at the time of delivery!"
        #del progress_order[session_id]
    
                           
    return JSONResponse (content={'fulfillmentText':fulfillmenttext})

        
def save_in_database(order:dict):
    next_order_id=database.next_order_id()
    for pharmacy_item, quantity in order.items():
         for pharmacy_item, quantity in order.items():
            rcode = database.insert_order_item(
            pharmacy_item,
            quantity,
            next_order_id )

            if rcode == -1:
                return -1
    
    database.order_tracking(next_order_id,"in progress")
   
    return next_order_id
        
        
    

        
    
    


