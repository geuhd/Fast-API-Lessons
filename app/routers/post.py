from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from .. import models,schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
import typing
from ..database import engine, get_db
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

@router.get("/", response_model = List[schemas.PostOut])
async def get_posts(db:  Session= Depends(get_db),
                    user_id:int=Depends(oauth2.get_current_user),
                    limit:int =10,
                    skip:int =0,
                    search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#left ineer join bu default
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
        models.Vote,models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [{"post": post, "vote": vote} for post, vote in posts]




@router.post("/",status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db:  Session= Depends(get_db), 
                current_user: int= Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
                  # (post.title,post.content,post.published))
    #new_post =cursor.fetchone()
    #conn.commit()
    print(current_user)
    new_post= models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#id is the path parameter
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db:  Session= Depends(get_db),
             current_user: int=Depends(oauth2.get_current_user)):
    #id=str(id)
    #cursor.execute("""SELECT * FROM posts WHERE %s = id""",(id))
    #post= cursor.fetchone()
    post_query =db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
        models.Vote,models.Vote.post_id== models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id ==id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    post,vote = post_query
    return  {"post": post, "vote": vote}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db:  Session= Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #id=str(id)
    #cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING *""",(id,))
   # deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first() 

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform action")
    post_query.delete(synchronize_session=False)
    db.commit()
    print(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate, 
                db:  Session= Depends(get_db),
                current_user:int =Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content =%s, published=%s WHERE id= %s RETURNING *""", 
                   #(post.title,post.content,post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    print(current_user)
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post =post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    print(post.owner_id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    print(current_user)
    return post_query.first()