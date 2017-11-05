from flask import current_app, request, jsonify, url_for
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from . import api
from .. import db
from ..models import Post, User, Meta

rest_api = Api(api)

user_fields = {
    'username': fields.String,
    'nickname': fields.String,
    'email': fields.String,
}

meta_fields = {
    'slug': fields.String,
    'name': fields.String,
    'type': fields.String,
    'description': fields.String,
}

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'headline': fields.String,
    'content': fields.String,
    'created': fields.DateTime,
    'updated': fields.DateTime,
    'url': fields.Url('main.post', absolute=True),
    'author': fields.Nested(user_fields),
    'metas': fields.Nested(meta_fields),
}

class PostListAPI(Resource):

    def req_parses(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', default='post', type=str)
        parser.add_argument('status', default=True, type=bool)
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('page', default=1, type=int)
        parser.add_argument('type', default='post', type=str)
        args = parser.parse_args()
        return args

    @marshal_with(post_fields)
    def get(self, username=None, slug=None):
        args = self.req_parses()
        queryset = Post.query.filter_by(type=args.type, status=args.status).order_by(Post.created.desc())
        endpoint = 'api.posts'
        params = request.args.copy()
        params['limit'] = args.limit
        link = ''

        if username:
            queryset = queryset.join(User).filter(User.username == username)
            endpoint = 'api.posts_by_author'

        if slug:
            queryset = queryset.join(Post.metas).filter(Meta.slug == slug)
            endpoint = 'api.posts_by_meta'

        pagination = queryset.paginate(args.page, per_page=args.limit, error_out=False)
        posts = pagination.items
        
        link_template = '<{url}>;rel="{rel}",'
        if pagination.has_prev:
            params['page'] = pagination.prev_num
            url = url_for(endpoint, username=username, slug=slug, _external=True, **params)
            link += link_template.format(url=url, rel='prev')
        if pagination.has_next:
            params['page'] = pagination.next_num
            url = url_for(endpoint, username=username, slug=slug, _external=True, **params)
            link += link_template.format(url=url, rel='next')

        return posts, {'Link': link}


class PostAPI(Resource):
    @marshal_with(post_fields)
    def get(self, id):
        post = Post.query.filter(Post.id == id).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(id))
        return post

    @marshal_with(post_fields)
    def put(self, id):
        # parsed_args = parser.parse_args()
        post = Post.query.filter(Post.id == id).first()
        db.session.add(post)
        db.session.commit()
        return post, 201

    def delete(self, id):
        post = Post.query.filter(Post.id == id).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(id))
        session.delete(post)
        session.commit()
        return {}, 204


class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter(User.username == username).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(username))
        return user

    def put(self, username):
        pass

    def delete(self, username):
        pass


class MetaListAPI(Resource):
    @marshal_with(meta_fields)
    def get(self):
        metas = Meta.query.all()
        return metas


class MetaAPI(Resource):
    @marshal_with(meta_fields)
    def get(self, slug):
        meta = Meta.query.filter(Meta.slug == slug).first()
        return meta



rest_api.add_resource(PostListAPI, '/posts', endpoint='posts')
rest_api.add_resource(PostListAPI, '/posts/author/<path:username>', endpoint='posts_by_author')
rest_api.add_resource(PostListAPI, '/posts/meta/<path:slug>', endpoint='posts_by_meta')
rest_api.add_resource(PostAPI, '/post/<int:id>', endpoint='post')
rest_api.add_resource(UserAPI, '/user/<path:username>', endpoint='user')
rest_api.add_resource(MetaListAPI, '/metas', endpoint='metas')
rest_api.add_resource(MetaAPI, '/meta/<path:slug>', endpoint='meta')