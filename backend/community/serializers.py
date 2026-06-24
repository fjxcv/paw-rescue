from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import CommentLike, CommunityComment, CommunityPost, PostFavorite, PostLike


def _display_name(user):
    if not user:
        return ''
    profile = getattr(user, 'profile', None)
    if profile and profile.nickname:
        return profile.nickname
    return user.username


def _infer_root_id(comment):
    if comment.root_id:
        return comment.root_id
    node = comment
    while node.parent_id:
        node = node.parent
    return node.id


class CommunityCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    floor = serializers.IntegerField(read_only=True, required=False)
    is_post_author = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = CommunityComment
        fields = [
            'id', 'post', 'author', 'parent', 'content', 'like_count', 'created_at',
            'replies', 'floor', 'is_post_author', 'is_admin', 'is_liked', 'reply_to',
        ]
        read_only_fields = ['author', 'like_count', 'created_at']

    def _post_author_id(self):
        post = self.context.get('post')
        if post:
            return post.author_id
        return self.context.get('post_author_id')

    def get_is_post_author(self, obj):
        author_id = self._post_author_id()
        return author_id and obj.author_id == author_id

    def get_is_admin(self, obj):
        profile = getattr(obj.author, 'profile', None)
        return bool(profile and profile.role == 'admin')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(comment=obj, user=request.user).exists()
        return False

    def get_reply_to(self, obj):
        if not obj.parent_id:
            return None
        parent = obj.parent
        if hasattr(parent, 'author'):
            return _display_name(parent.author)
        return None

    def get_replies(self, obj):
        tree = self.context.get('replies_by_root') or {}
        children = tree.get(obj.id, [])
        return CommunityCommentSerializer(
            children,
            many=True,
            context=self.context,
        ).data


def build_comment_threads(post, request):
    comments = list(
        CommunityComment.objects.filter(post=post, is_deleted=False)
        .select_related('author', 'author__profile', 'parent', 'parent__author', 'parent__author__profile')
        .order_by('created_at')
    )
    tops = [c for c in comments if not c.parent_id]
    tops.sort(key=lambda x: x.created_at)

    replies_by_root = {}
    for c in comments:
        if c.parent_id:
            root_id = _infer_root_id(c)
            replies_by_root.setdefault(root_id, []).append(c)

    for root_id in replies_by_root:
        replies_by_root[root_id].sort(key=lambda x: x.created_at)

    ctx = {
        'request': request,
        'post': post,
        'post_author_id': post.author_id,
        'replies_by_root': replies_by_root,
    }
    result = []
    for floor, top in enumerate(tops, start=1):
        data = CommunityCommentSerializer(top, context=ctx).data
        data['floor'] = floor
        result.append(data)
    return result


class CommunityPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_edited = serializers.SerializerMethodField()

    class Meta:
        model = CommunityPost
        fields = [
            'id', 'author', 'category', 'title', 'content', 'image_urls',
            'like_count', 'comment_count', 'is_deleted', 'created_at', 'updated_at',
            'edited_at', 'is_edited', 'is_liked', 'is_favorited',
        ]
        read_only_fields = ['author', 'like_count', 'comment_count', 'created_at', 'updated_at', 'edited_at']

    def get_is_edited(self, obj):
        return bool(obj.edited_at)

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostFavorite.objects.filter(post=obj, user=request.user).exists()
        return False


class PostFavoriteItemSerializer(serializers.ModelSerializer):
    post = CommunityPostSerializer(read_only=True)

    class Meta:
        model = PostFavorite
        fields = ['id', 'created_at', 'post']
