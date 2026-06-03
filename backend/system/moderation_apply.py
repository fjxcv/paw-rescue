from cms.models import CmsArticle
from community.models import CommunityPost
from lostfound.models import LostFoundPost


CONTENT_TYPES = [
    ('community_post', 'Community Post'),
    ('cms_article', 'CMS Article'),
    ('lost_found_post', 'Lost/Found Post'),
]


def apply_moderation(content_type, content_id, action):
    """Apply hide/delete to the underlying content record."""
    if action == 'approve':
        return
    if content_type == 'community_post':
        post = CommunityPost.objects.filter(pk=content_id).first()
        if not post:
            raise ValueError('community_post not found')
        if action in ('hide', 'delete'):
            post.is_deleted = True
            post.save(update_fields=['is_deleted', 'updated_at'])
        return
    if content_type == 'cms_article':
        article = CmsArticle.objects.filter(pk=content_id).first()
        if not article:
            raise ValueError('cms_article not found')
        if action in ('hide', 'delete'):
            article.status = 2
            article.save(update_fields=['status', 'updated_at'])
        return
    if content_type == 'lost_found_post':
        post = LostFoundPost.objects.filter(pk=content_id).first()
        if not post:
            raise ValueError('lost_found_post not found')
        if action in ('hide', 'delete'):
            post.status = 'cancelled'
            post.save(update_fields=['status', 'updated_at'])
        return
    raise ValueError(f'unsupported content_type: {content_type}')
