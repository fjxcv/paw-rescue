from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from cms.models import ArticleFavorite, CmsArticle, CmsCategory
from community.models import CommunityPost, PostFavorite
from lostfound.models import LostFoundPost
from pets.models import AdoptApplication, PetProfile
from portal.models import PortalCarousel
from rescue.models import RescueCase
from system.models import PlatformConfig


class Command(BaseCommand):
    help = 'Seed demo data for PawRescue platform (Chinese)'

    def handle(self, *args, **options):
        admin, _ = User.objects.update_or_create(
            username='admin',
            defaults={'email': 'admin@petrescue.local', 'is_staff': True, 'is_superuser': True},
        )
        admin.set_password('admin12345')
        admin.save()
        UserProfile.objects.filter(user=admin).update(role='admin')

        user, _ = User.objects.update_or_create(
            username='demo',
            defaults={'email': 'demo@petrescue.local'},
        )
        user.set_password('demo12345')
        user.save()
        UserProfile.objects.filter(user=user).update(has_privacy_consent=True)

        PlatformConfig.objects.get_or_create(
            config_key='max_upload_mb',
            defaults={'config_value': '10', 'description': '\u6700\u5927\u4e0a\u4f20\u6587\u4ef6\u5927\u5c0f\uff08MB\uff09'},
        )
        PlatformConfig.objects.get_or_create(
            config_key='ai_daily_limit',
            defaults={
                'config_value': '200',
                'description': '\u5e73\u53f0\u6bcf\u65e5 AI \u8c03\u7528\u4e0a\u9650\uff0c0 \u8868\u793a\u4e0d\u9650\u5236',
            },
        )
        PlatformConfig.objects.get_or_create(
            config_key='ai_total_limit',
            defaults={
                'config_value': '10000',
                'description': '\u5e73\u53f0 AI \u7d2f\u8ba1\u8c03\u7528\u4e0a\u9650\uff0c0 \u8868\u793a\u4e0d\u9650\u5236',
            },
        )

        PortalCarousel.objects.update_or_create(
            title='\u6b22\u8fce\u9886\u517b',
            defaults={
                'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800',
                'link_url': '/pets',
                'sort_order': 1,
            },
        )

        category, _ = CmsCategory.objects.get_or_create(
            name='\u79d1\u666e',
            defaults={'sort_order': 1},
        )
        CmsArticle.objects.update_or_create(
            article_type='science',
            title='\u6d41\u6d6a\u732b\u72d7\u79d1\u666e\u77e5\u8bc6',
            defaults={
                'category': category,
                'author': admin,
                'summary': '\u517b\u5ba0\u524d\u5fc5\u770b\u7684\u79d1\u666e\u77e5\u8bc6',
                'content': '\u8bf7\u5728\u9886\u517b\u524d\u505a\u597d\u5fc3\u7406\u51c6\u5907\u4e0e\u8d23\u4efb\u8bc4\u4f30\u3002\u9886\u517b\u4e0d\u4ec5\u4ec5\u662f\u5e26\u56de\u5bb6\u91cc\u4e00\u53ea\u5ba0\u7269\uff0c\u66f4\u662f\u4e00\u4efd\u957f\u8fbe\u5341\u4f59\u5e74\u7684\u627f\u8bfa\u3002',
                'status': 1,
                'published_at': timezone.now(),
            },
        )

        announcement_category, _ = CmsCategory.objects.get_or_create(
            name='\u516c\u544a',
            defaults={'sort_order': 2},
        )
        CmsArticle.objects.update_or_create(
            article_type='announcement',
            title='\u6696\u722a\u6551\u52a9\u5e73\u53f0\u6b63\u5f0f\u4e0a\u7ebf',
            defaults={
                'category': announcement_category,
                'author': admin,
                'summary': '\u6b22\u8fce\u52a0\u5165\u6d41\u6d6a\u5ba0\u7269\u7efc\u5408\u6551\u52a9\u7ba1\u7406\u5e73\u53f0',
                'content': '\u5e73\u53f0\u5df2\u5f00\u653e\u9886\u517b\u3001\u62a5\u5931\u5bfb\u4e3b\u3001\u6551\u52a9\u8ffd\u8e2a\u4e0e\u793e\u533a\u4ea4\u6d41\u7b49\u529f\u80fd\uff0c\u6b22\u8fce\u7231\u5fc3\u4eba\u58eb\u53c2\u4e0e\u3002',
                'is_pinned': True,
                'status': 1,
                'published_at': timezone.now(),
            },
        )
        CmsArticle.objects.update_or_create(
            article_type='announcement',
            title='\u6625\u5b63\u9886\u517b\u65e5\u6d3b\u52a8\u9884\u544a',
            defaults={
                'category': announcement_category,
                'author': admin,
                'summary': '\u672c\u5468\u672b\u5c06\u4e3e\u529e\u7ebf\u4e0b\u9886\u517b\u89c1\u9762\u4f1a',
                'content': '\u5c65\u65f6\u5c06\u6709 20+ \u53ea\u5f85\u9886\u517b\u5ba0\u7269\u5230\u573a\uff0c\u6b22\u8fce\u6709\u610f\u5411\u7684\u9886\u517b\u4eba\u63d0\u524d\u9884\u7ea6\u53c2\u89c2\u3002',
                'is_pinned': False,
                'status': 1,
                'published_at': timezone.now(),
            },
        )

        rescue1, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601001',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.572800'),
                'discover_longitude': Decimal('104.066800'),
                'discover_address': '\u6210\u90fd\u5e02\u9526\u6c5f\u533a\u4e1c\u5927\u8857',
                'appearance': '\u6a58\u8272\u77ed\u6bdb\uff0c\u5706\u8138\uff0c\u4f53\u578b\u4e2d\u7b49',
                'health_note': '\u5df2\u505a\u57fa\u7840\u68c0\u67e5\uff0c\u8f7b\u5fae\u8033\u8815',
                'current_status': 'awaiting_adoption',
            },
        )
        rescue2, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601002',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.660000'),
                'discover_longitude': Decimal('104.063000'),
                'discover_address': '\u6210\u90fd\u5e02\u6b66\u4faf\u533a\u79d1\u534e\u5317\u8def',
                'appearance': '\u9ed1\u767d\u76f8\u95f4\u957f\u6bdb\uff0c\u84dd\u773c\u775b\uff0c\u4f53\u578b\u8f83\u5927',
                'health_note': '\u5df2\u9a71\u866b\u75ab\u82d7\uff0c\u8eab\u4f53\u5065\u5eb7',
                'current_status': 'rescued',
            },
        )
        rescue3, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601003',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.550000'),
                'discover_longitude': Decimal('104.050000'),
                'discover_address': '\u6210\u90fd\u5e02\u6210\u534e\u533a\u5efa\u8bbe\u8def',
                'appearance': '\u7eaf\u767d\u8272\u77ed\u6bdb\uff0c\u4f53\u578b\u5a07\u5c0f',
                'health_note': '\u5df2\u7edd\u80b2\uff0c\u63a5\u79cd\u75ab\u82d7',
                'current_status': 'awaiting_adoption',
            },
        )
        rescue4, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601004',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.580000'),
                'discover_longitude': Decimal('104.120000'),
                'discover_address': '\u6210\u90fd\u5e02\u91d1\u725b\u533a\u8336\u5e97\u5b50',
                'appearance': '\u8910\u8272\u77ed\u6bdb\uff0c\u7acb\u8033\uff0c\u4f53\u683c\u5065\u58ee',
                'health_note': '\u5df2\u63a5\u79cd\u72c2\u72ac\u75ab\u82d7\uff0c\u5df2\u9a71\u866b',
                'current_status': 'awaiting_adoption',
            },
        )
        RescueCase.objects.update_or_create(
            rescue_no='RC20260601005',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.620000'),
                'discover_longitude': Decimal('104.080000'),
                'discover_address': '\u6210\u90fd\u5e02\u9526\u6c5f\u533a\u6625\u7199\u8def\u9644\u8fd1',
                'appearance': '\u4e09\u82b1\u957f\u6bdb\u732b\uff0c\u4f53\u578b\u504f\u7626',
                'health_note': '\u5df2\u5eb7\u590d\uff0c\u53ef\u9886\u517b',
                'current_status': 'rescued',
            },
        )
        RescueCase.objects.update_or_create(
            rescue_no='RC20260623001',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.570000'),
                'discover_longitude': Decimal('104.060000'),
                'discover_address': '\u6210\u90fd\u5e02\u6b66\u4faf\u533a\u79d1\u534e\u5317\u8def',
                'appearance': '\u9ed1\u8272\u4e2d\u578b\u72ac\uff0c\u5de6\u8033\u6709\u7f3a\u53e3',
                'health_note': '\u4eca\u65e5\u4e0a\u62a5\uff0c\u5f85\u8fdb\u4e00\u6b65\u68c0\u67e5',
                'current_status': 'rescued',
                'created_at': timezone.now(),
            },
        )

        AdoptApplication.objects.all().delete()
        PetProfile.objects.all().delete()

        PetProfile.objects.create(
            rescue_case=rescue1,
            name='\u5c0f\u6a58',
            species='cat',
            breed='\u4e2d\u534e\u7530\u56ed\u732b',
            age_months=8,
            gender='male',
            size_category='small',
            health_status='\u5df2\u9a71\u866b\u75ab\u82d7\uff0c\u5df2\u7edd\u80b2',
            description='\u6027\u683c\u6e29\u987a\u7c98\u4eba\uff0c\u559c\u6b22\u8e72\u817f\u6c42\u62b1\u62b1\uff0c\u9002\u5408\u6709\u7ecf\u9a8c\u7684\u5bb6\u5ead\u9886\u517b\u3002',
            photo_url='https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=rescue2,
            name='\u96ea\u7403',
            species='cat',
            breed='\u5e03\u5076\u732b',
            age_months=24,
            gender='female',
            size_category='small',
            health_status='\u5df2\u63a5\u79cd\u75ab\u82d7\uff0c\u5b9a\u671f\u4f53\u68c0',
            description='\u989c\u503c\u8d85\u9ad8\uff0c\u6027\u683c\u5b89\u9759\u4f18\u96c5\uff0c\u84dd\u773c\u775b\u7279\u522b\u8ff7\u4eba\u3002',
            photo_url='https://images.unsplash.com/photo-1574158622682-e40e69881006?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=rescue3,
            name='\u5c0f\u767d',
            species='dog',
            breed='\u6bd4\u718a\u72d7',
            age_months=12,
            gender='female',
            size_category='small',
            health_status='\u5df2\u7edd\u80b2\uff0c\u5df2\u63a5\u79cd\u75ab\u82d7',
            description='\u6d3b\u6cfc\u597d\u52a8\uff0c\u7279\u522b\u4eb2\u4eba\uff0c\u559c\u6b22\u51fa\u53bb\u901b\u5f2f\u3002',
            photo_url='https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=rescue4,
            name='\u65fa\u8d22',
            species='dog',
            breed='\u4e2d\u534e\u7530\u56ed\u72ac',
            age_months=36,
            gender='male',
            size_category='medium',
            health_status='\u5df2\u63a5\u79cd\u72c2\u72ac\u75ab\u82d7\uff0c\u5df2\u9a71\u866b',
            description='\u975e\u5e38\u5fe0\u8bda\uff0c\u770b\u5bb6\u62a4\u9662\u7684\u4e00\u628a\u597d\u624b\uff0c\u5bf9\u4e3b\u4eba\u6781\u4e3a\u4f9d\u604b\u3002',
            photo_url='https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=None,
            name='\u8c46\u8c46',
            species='rabbit',
            breed='\u8377\u5170\u5782\u8033\u5154',
            age_months=6,
            gender='female',
            size_category='small',
            health_status='\u5065\u5eb7\u6d3b\u6cfc\uff0c\u5df2\u505a\u4f53\u68c0',
            description='\u8d85\u840c\u5782\u8033\u5154\uff0c\u7231\u5e72\u51c0\uff0c\u4f1a\u7528\u5154\u5395\u6240\u3002',
            photo_url='https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=None,
            name='\u963f\u798f',
            species='dog',
            breed='\u91d1\u6bdb\u5bfb\u56de\u72ac',
            age_months=18,
            gender='male',
            size_category='large',
            health_status='\u5df2\u7edd\u80b2\uff0c\u63a5\u79cd\u5168\u90e8\u75ab\u82d7',
            description='\u6027\u683c\u9633\u5149\u5f00\u6717\uff0c\u975e\u5e38\u806a\u660e\uff0c\u4f1a\u5750\u4e0b\u3001\u63e1\u624b\u7b49\u57fa\u672c\u6307\u4ee4\u3002',
            photo_url='https://images.unsplash.com/photo-1552053831-71594a27632d?w=600',
            adoption_status='available',
        )
        PetProfile.objects.create(
            rescue_case=None,
            name='\u56e2\u56e2',
            species='cat',
            breed='\u6a58\u732b',
            age_months=30,
            gender='female',
            size_category='small',
            health_status='\u5df2\u7edd\u80b2\uff0c\u8eab\u4f53\u5065\u5eb7',
            description='\u5df2\u4e8e\u53bb\u5e74\u88ab\u7231\u5fc3\u5bb6\u5ead\u9886\u517b\uff0c\u76ee\u524d\u751f\u6d3b\u5e78\u798f\u3002',
            photo_url='https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=600',
            adoption_status='adopted',
            is_public=False,
        )
        PetProfile.objects.create(
            rescue_case=None,
            name='\u5927\u9ec4',
            species='dog',
            breed='\u4e2d\u534e\u7530\u56ed\u72ac',
            age_months=48,
            gender='male',
            size_category='medium',
            health_status='\u5df2\u7edd\u80b2\uff0c\u5b9a\u671f\u4f53\u68c0',
            description='\u5fe0\u8bda\u62a4\u4e3b\uff0c\u5df2\u6210\u529f\u9886\u517b\u81f3\u90ca\u533a\u5c0f\u9662\u3002',
            photo_url='https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600',
            adoption_status='adopted',
            is_public=False,
        )
        PetProfile.objects.create(
            rescue_case=None,
            name='\u5495\u5495',
            species='cat',
            breed='\u72f8\u82b1\u732b',
            age_months=20,
            gender='female',
            size_category='small',
            health_status='\u5df2\u63a5\u79cd\u75ab\u82d7',
            description='\u6027\u683c\u72ec\u7acb\uff0c\u5df2\u88ab\u5927\u5b66\u751f\u9886\u517b\u3002',
            photo_url='https://images.unsplash.com/photo-1529773473-3f2e4d392ae8?w=600',
            adoption_status='adopted',
            is_public=False,
        )

        LostFoundPost.objects.update_or_create(
            publisher=user,
            post_type='lost',
            pet_species='\u732b',
            address_text='\u6210\u90fd\u5e02\u9ad8\u65b0\u533a\u5929\u5e9c\u8f6f\u4ef6\u56ed\u9644\u8fd1',
            defaults={
                'features': '\u68a8\u82b1\u8272\u3001\u7eff\u773c\u775b\u3001\u6234\u7ea2\u8272\u9879\u5708',
                'latitude': Decimal('30.600000'),
                'longitude': Decimal('104.100000'),
                'reward_amount': Decimal('500.00'),
                'contact_phone': '13800000000',
                'status': 'searching',
            },
        )
        LostFoundPost.objects.update_or_create(
            publisher=user,
            post_type='found',
            pet_species='\u6cf0\u8fea\u72ac',
            address_text='\u6210\u90fd\u5e02\u6b66\u4faf\u533a\u7389\u6797\u751f\u6d3b\u5e7f\u573a',
            defaults={
                'features': '\u68d5\u8272\u5377\u6bdb\u3001\u4f53\u578b\u8f83\u5c0f\u3001\u6234\u84dd\u8272\u9879\u5708',
                'latitude': Decimal('30.630000'),
                'longitude': Decimal('104.050000'),
                'reward_amount': Decimal('0'),
                'contact_phone': '13800000001',
                'status': 'searching',
            },
        )
        LostFoundPost.objects.update_or_create(
            publisher=user,
            post_type='lost',
            pet_species='\u67ef\u57fa\u72ac',
            address_text='\u6210\u90fd\u5e02\u9752\u7f8a\u533a\u5bbd\u7a84\u5df7\u5b50',
            defaults={
                'features': '\u9ec4\u767d\u53cc\u8272\u3001\u77ed\u817f\u3001\u8d70\u5931\u65f6\u7a7f\u7ea2\u8272\u8863\u670d',
                'latitude': Decimal('30.670000'),
                'longitude': Decimal('104.050000'),
                'reward_amount': Decimal('800.00'),
                'contact_phone': '13800000002',
                'status': 'searching',
            },
        )

        CommunityPost.objects.update_or_create(
            author=user,
            title='\u5206\u4eab\u4e00\u6b21\u6551\u52a9\u7ecf\u5386',
            defaults={
                'category': 'rescue_share',
                'content': '\u611f\u8c22\u6240\u6709\u5fd7\u613f\u8005\u7684\u5e2e\u52a9\uff01\u6628\u5929\u5728\u8def\u8fb9\u53d1\u73b0\u4e00\u53ea\u53d7\u4f24\u7684\u5c0f\u732b\uff0c\u5927\u5bb6\u4e00\u8d77\u628a\u5b83\u9001\u5230\u4e86\u5ba0\u7269\u533b\u9662\uff0c\u73b0\u5728\u5df2\u7ecf\u8131\u79bb\u4e86\u5371\u9669\u3002',
            },
        )
        post = CommunityPost.objects.filter(author=user).first()
        if post:
            PostFavorite.objects.get_or_create(post=post, user=user)

        article = CmsArticle.objects.filter(status=1).first()
        if article:
            ArticleFavorite.objects.get_or_create(article=article, user=user)

        self.stdout.write(self.style.SUCCESS('[OK] \u6f14\u793a\u6570\u636e\u5df2\u5c31\u7eea\uff08\u5168\u90e8\u4e3a\u4e2d\u6587\u5185\u5bb9\uff09'))
        self.stdout.write('  \u7ba1\u7406\u5458\u8d26\u53f7: admin / admin12345')
        self.stdout.write('  \u666e\u901a\u7528\u6237:   demo / demo12345')
        self.stdout.write(f'  \u53ef\u9886\u517b\u5ba0\u7269: {PetProfile.objects.filter(adoption_status="available").count()} \u53ea')
        self.stdout.write(f'  \u5df2\u9886\u517b\u5ba0\u7269: {PetProfile.objects.filter(adoption_status="adopted").count()} \u53ea')
        self.stdout.write('  \u5efa\u8bae\u7ee7\u7eed\u8fd0\u884c: python manage.py seed_test_data')
