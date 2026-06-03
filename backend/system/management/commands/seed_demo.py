from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from cms.models import ArticleFavorite, CmsArticle, CmsCategory
from community.models import CommunityPost, PostFavorite
from lostfound.models import LostFoundPost
from pets.models import PetProfile
from portal.models import PortalCarousel
from rescue.models import RescueCase
from system.models import PlatformConfig


class Command(BaseCommand):
    help = 'Seed demo data for PetRescue platform'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@petrescue.local', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('admin12345')
            admin.save()
        UserProfile.objects.filter(user=admin).update(role='admin')

        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@petrescue.local'},
        )
        if created:
            user.set_password('demo12345')
            user.save()
            UserProfile.objects.filter(user=user).update(has_privacy_consent=True)

        PlatformConfig.objects.get_or_create(
            config_key='max_upload_mb',
            defaults={'config_value': '10', 'description': 'Max upload size in MB'},
        )

        if not PortalCarousel.objects.exists():
            PortalCarousel.objects.create(
                title='\u6b22\u8fce\u9886\u517b',
                image_url='https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800',
                link_url='/pets',
                sort_order=1,
            )

        category, _ = CmsCategory.objects.get_or_create(
            name='\u79d1\u666e',
            defaults={'sort_order': 1},
        )
        if not CmsArticle.objects.exists():
            CmsArticle.objects.create(
                category=category,
                author=admin,
                article_type='science',
                title='\u6d41\u6d6a\u732b\u72d7\u79d1\u666e\u77e5\u8bc6',
                summary='\u517b\u5ba0\u524d\u5fc5\u770b',
                content='\u8bf7\u5728\u9886\u517b\u524d\u505a\u597d\u51c6\u5907\u4e0e\u8d23\u4efb\u5fc3\u8bc4\u4f30\u3002',
                status=1,
                published_at=timezone.now(),
            )

        rescue, _ = RescueCase.objects.get_or_create(
            rescue_no='RC202606020001',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.572800'),
                'discover_longitude': Decimal('104.066800'),
                'discover_address': '\u6210\u90fd\u5e02\u4e2d\u5fc3',
                'appearance': '\u68a8\u82b1\u8272\u6bdb\u53d1',
                'current_status': 'awaiting_adoption',
            },
        )

        if not PetProfile.objects.exists():
            PetProfile.objects.create(
                rescue_case=rescue,
                name='\u5c0f\u6a58',
                species='cat',
                breed='\u7530\u56ed\u732b',
                age_months=8,
                gender='male',
                health_status='\u5df2\u9a71\u866b\u75ab\u82d7',
                description='\u6027\u683c\u6e29\u987a\uff0c\u9002\u5408\u6709\u7ecf\u9a8c\u7684\u5bb6\u5ead\u9886\u517b\u3002',
                photo_url='https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600',
                adoption_status='available',
            )

        if not LostFoundPost.objects.exists():
            LostFoundPost.objects.create(
                publisher=user,
                post_type='lost',
                pet_species='\u732b',
                features='\u68a8\u82b1\u8272\u3001\u7eff\u773c\u775b',
                latitude=Decimal('30.600000'),
                longitude=Decimal('104.100000'),
                address_text='\u9ad8\u65b0\u533a\u67d0\u5c0f\u533a',
                reward_amount=Decimal('500.00'),
                contact_phone='13800000000',
            )

        post, _ = CommunityPost.objects.get_or_create(
            author=user,
            title='\u5206\u4eab\u4e00\u6b21\u6551\u52a9\u7ecf\u9a8c',
            defaults={
                'category': 'rescue_share',
                'content': '\u611f\u8c22\u5fd7\u613f\u8005\u4eec\u7684\u5e2e\u52a9\uff01',
            },
        )
        PostFavorite.objects.get_or_create(post=post, user=user)

        article = CmsArticle.objects.filter(status=1).first()
        if article:
            ArticleFavorite.objects.get_or_create(article=article, user=user)

        self.stdout.write(self.style.SUCCESS('\u6f14\u793a\u6570\u636e\u5df2\u5c31\u7eea'))
        self.stdout.write('\u7ba1\u7406\u5458: admin / admin12345')
        self.stdout.write('\u666e\u901a\u7528\u6237: demo / demo12345')
