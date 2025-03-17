# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app=FastAPI(
#     title = "Just Rise FastAPI",
#     description = "Just Rise Youtube Recorded test FastAPI project",
#     version = "5.6.0"
    
# )

# @app.get("/")
# def produts():
#     return {"data": "products"}

# @app.get("/product")
# def  product():
#     return {"data": "currently you are in product data"}

# @app.get("/services/data")
# def  product():
#     return {"data": "currently you are in services data"}

# # Dyanmic Parameter in FastAPI
# @app.get("/services/{id}")
# def  product(id:int):
#     # return {"data": "currently you are in services " + id}
#     return{"data":f"currently you are in services {id}"}

# @app.get("/bonus/{basesalary}/{bonus}")
# def  product(basesalary:int, bonus :int):
#     return {"data": basesalary+ bonus}
#     # return{"data":f"currently you are in services {id}"}
    
# item =[
#     {"name":"laptop", "price":50000, "desc":"This is a laptop"},
#     {"name":"mobile", "price":20000, "desc":"This is a mobile"},
#     {"name":"watch", "price":5000, "desc":"This is a watch"},
#     {"name":"shoe", "price":1000, "desc":"This is a shoe"},
#     {"name":"shirt", "price":500, "desc":"This is a shirt"}
  
# ]

# # Post Method in FastAPI
# class Product(BaseModel):
#     name:str
#     price:int
#     desc:str
    
# @app.post("/product")
# def new_product(pro:Product):
#     return pro.name

# @app.post("/create_product",status_code=201)
# def create_product(pro:Product):
#     item_des= {"name":pro.name, "price":pro.price, "desc":pro.desc}
#     item.append(item_des)
#     return {"message":"Data has been created successfully"}


# @app.get("/view_all_product")
# def view_product():
#     return item

# @app.get("/view_product/{price_val}")
# def view_single_product(price_val:int):
#     for i in item:
#         if i["price"]==price_val:
#             return i
#     return {"data":"Product Not Found"}

# # PUT Method in FastAPI
# @app.put("/update_product/{price_val}")
# def update_product(price_val:int, pro:Product):
#     for i in item:
#         if i["price"]==price_val:
#             i["name"]=pro.name
#             i["price"]=pro.price
#             i["desc"]=pro.desc
#             return {"message":"Data has been updated successfully"}
#     raise HTTPException(status_code=404, detail="Product Not Found")

# # Delete Method in FastAPI
# @app.delete("/delete_product/{price_val}", status_code=201)
# def delete_product(price_val:int):
#     for i in item:
#         if i["price"]==price_val:
#             item.remove(i)
#             return {"message":"Data has been deleted successfully"}
#     raise HTTPException(status_code=404, detail="Product Not Found")







from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector


app = FastAPI()

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="youtube"
    )

cursor=db.cursor()

class  user(BaseModel):
    name:str
    email:str
    age:int
    
# GET
@app.get('/viewuser')
def get_user():
    cursor.execute("SELECT * FROM USER")
    result=cursor.fetchall()
    return {"users":result}

# for single user
@app.get('/viewuser/{user_id}')
def get_user(user_id:int):
    cursor.execute(f"SELECT * FROM USER WHERE id={user_id}")
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=404,detail="User not found")    
    return {"user":result}

# POST
@app.post ("/create_user")
def create_user(user:user):
    # cursor.execute(f"INSERT INTO USER (name,email,age) VALUES ('{user.name}','{user.email}',{user.age})")
    cursor.execute("INSERT INTO USER (name,email,age) VALUES (%s,%s,%s)",(user.name,user.email,user.age))
    db.commit()
    return {"message":"user created"}


# PUT
@app.put("/update_user/{user_id}", status_code=201)
def update_user(user_id:int,user:user):
    cursor.execute(f"UPDATE USER SET name ='{user.name}',email='{user.email}',age={user.age} WHERE id={user_id}")
    db.commit()
    return {"message":"user updated"}

# DELETE
@app.delete("/delete_user/{user_id}", status_code=201)
def delete_user(user_id:int):
    cursor.execute(f"SELECT * FROM USER WHERE id={user_id}")
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=404,detail="User not found")
    cursor.execute(f"DELETE FROM USER WHERE id={user_id}")
    db.commit()
    return {"message":"user Deleted"}