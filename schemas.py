import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Photo, db

class PhotoType(SQLAlchemyObjectType):
    class Meta:
        model = Photo
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_photos = SQLAlchemyConnectionField(PhotoType)
    photo = graphene.Field(PhotoType, id=graphene.Int())

    def resolve_photo(self, info, id):
        return Photo.query.get(id)

class CreatePhoto(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        filename = graphene.String()

    photo = graphene.Field(lambda: PhotoType)

    def mutate(self, info, title, filename):
        photo = Photo(title=title, filename=filename)
        db.session.add(photo)
        db.session.commit()
        return CreatePhoto(photo=photo)

class DeletePhoto(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        photo = Photo.query.get(id)
        if photo:
            db.session.delete(photo)
            db.session.commit()
            return DeletePhoto(success=True)
        return DeletePhoto(success=False)

class Mutation(graphene.ObjectType):
    create_photo = CreatePhoto.Field()
    delete_photo = DeletePhoto.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)