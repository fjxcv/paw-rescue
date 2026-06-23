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
    help = 'Seed demo data for PetConnect platform (Chinese)'

    def handle(self, *args, **options):
        # ===== 用户 =====
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

        # ===== 平台配置 =====
        PlatformConfig.objects.get_or_create(
            config_key='max_upload_mb',
            defaults={'config_value': '10', 'description': '最大上传文件大小（MB）'},
        )

        # ===== 首页轮播 =====
        PortalCarousel.objects.update_or_create(
            title='欢迎领养',
            defaults={
                'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800',
                'link_url': '/pets',
                'sort_order': 1,
            },
        )

        # ===== CMS 分类与文章 =====
        category, _ = CmsCategory.objects.get_or_create(
            name='科普',
            defaults={'sort_order': 1},
        )
        CmsArticle.objects.update_or_create(
            article_type='science',
            title='流浪猫狗科普知识',
            defaults={
                'category': category,
                'author': admin,
                'summary': '养宠前必看的科普知识',
                'content': '请在领养前做好心理准备与责任评估。领养不仅仅是带回家一只宠物，更是一份长达十余年的承诺。',
                'status': 1,
                'published_at': timezone.now(),
            },
        )

        # ===== 救助案例 =====
        rescue1, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601001',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.572800'),
                'discover_longitude': Decimal('104.066800'),
                'discover_address': '成都市锦江区东大街',
                'appearance': '橘色短毛，圆脸，体型中等',
                'health_note': '已做基础检查，轻微耳螨',
                'current_status': 'awaiting_adoption',
            },
        )

        rescue2, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601002',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.660000'),
                'discover_longitude': Decimal('104.063000'),
                'discover_address': '成都市武侯区科华北路',
                'appearance': '黑白相间长毛，蓝眼睛，体型较大',
                'health_note': '已驱虫疫苗，身体健康',
                'current_status': 'rescued',
            },
        )

        rescue3, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601003',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.550000'),
                'discover_longitude': Decimal('104.050000'),
                'discover_address': '成都市成华区建设路',
                'appearance': '纯白色短毛，体型娇小',
                'health_note': '已绝育，接种疫苗',
                'current_status': 'awaiting_adoption',
            },
        )

        rescue4, _ = RescueCase.objects.update_or_create(
            rescue_no='RC20260601004',
            defaults={
                'reporter': user,
                'discover_latitude': Decimal('30.580000'),
                'discover_longitude': Decimal('104.120000'),
                'discover_address': '成都市金牛区茶店子',
                'appearance': '棕色短毛，立耳，体格健壮',
                'health_note': '已接种狂犬疫苗，已驱虫',
                'current_status': 'awaiting_adoption',
            },
        )

        # ===== 宠物档案（可领养）=====
        # 先清除已有宠物数据，确保以中文为准
        PetProfile.objects.all().delete()

        PetProfile.objects.create(
            rescue_case=rescue1,
            name='小橘',
            species='cat',
            breed='中华田园猫',
            age_months=8,
            gender='male',
            size_category='small',
            health_status='已驱虫疫苗，已绝育',
            description='性格温顺粘人，喜欢蹭腿求抱抱，适合有经验的家庭领养。小橘是在成都东大街路边发现的流浪猫，当时它正躲在车底下瑟瑟发抖，被好心人救助后一直很亲人。',
            photo_url='https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600',
            adoption_status='available',
        )

        PetProfile.objects.create(
            rescue_case=rescue2,
            name='雪球',
            species='cat',
            breed='布偶猫',
            age_months=24,
            gender='female',
            size_category='small',
            health_status='已接种疫苗，定期体检',
            description='颜值超高，性格安静优雅，蓝眼睛特别迷人。雪球是被遗弃在武侯区一个小区门口的，当时还戴着项圈，应该是原主人搬家时被丢弃的。它非常爱干净，适合有耐心的家庭。',
            photo_url='https://images.unsplash.com/photo-1574158622682-e40e69881006?w=600',
            adoption_status='available',
        )

        PetProfile.objects.create(
            rescue_case=rescue3,
            name='小白',
            species='dog',
            breed='比熊犬',
            age_months=12,
            gender='female',
            size_category='small',
            health_status='已绝育，已接种疫苗',
            description='活泼好动，特别亲人，喜欢出去遛弯。小白是在成华区建设路的一家商铺门口被发现的，当时又脏又瘦，经过三个月悉心照料现在已经恢复得很好，毛发白净蓬松。',
            photo_url='https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600',
            adoption_status='available',
        )

        PetProfile.objects.create(
            rescue_case=rescue4,
            name='旺财',
            species='dog',
            breed='中华田园犬',
            age_months=36,
            gender='male',
            size_category='medium',
            health_status='已接种狂犬疫苗，已驱虫',
            description='非常忠诚，看家护院的一把好手，对主人极为依恋。旺财是在金牛区一个废弃工地上发现的，它独自守在那里等主人回来，等了很久。虽然体型中等但性情温和，不乱叫。',
            photo_url='https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600',
            adoption_status='available',
        )

        PetProfile.objects.create(
            rescue_case=None,
            name='豆豆',
            species='rabbit',
            breed='荷兰垂耳兔',
            age_months=6,
            gender='female',
            size_category='small',
            health_status='健康活泼，已做体检',
            description='超萌垂耳兔，爱干净，会用兔厕所。豆豆是在志愿者家中出生的，父母都是被救助的兔子。它性格温顺，喜欢被人抚摸，特别适合有小孩的家庭。',
            photo_url='https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=600',
            adoption_status='available',
        )

        PetProfile.objects.create(
            rescue_case=None,
            name='阿福',
            species='dog',
            breed='金毛寻回犬',
            age_months=18,
            gender='male',
            size_category='large',
            health_status='已绝育，接种全部疫苗',
            description='性格阳光开朗，非常聪明，会坐下、握手等基本指令。阿福是一只被主人因搬家无法继续养的狗，它非常喜欢和人互动，适合活动空间较大的家庭。',
            photo_url='https://images.unsplash.com/photo-1552053831-71594a27632d?w=600',
            adoption_status='available',
        )

        # ===== 走失/寻主帖子 =====
        LostFoundPost.objects.update_or_create(
            publisher=user,
            post_type='lost',
            defaults={
                'pet_species': '猫',
                'features': '梨花色、绿眼睛、戴红色项圈',
                'latitude': Decimal('30.600000'),
                'longitude': Decimal('104.100000'),
                'address_text': '成都市高新区天府软件园附近',
                'reward_amount': Decimal('500.00'),
                'contact_phone': '13800000000',
            },
        )

        # ===== 社区帖子 =====
        CommunityPost.objects.update_or_create(
            author=user,
            title='分享一次救助经历',
            defaults={
                'category': 'rescue_share',
                'content': '感谢所有志愿者的帮助！昨天在路边发现一只受伤的小猫，大家一起把它送到了宠物医院，现在已经脱离了危险。救助小动物需要全社会的关注和参与。',
            },
        )
        post = CommunityPost.objects.filter(author=user).first()
        if post:
            PostFavorite.objects.get_or_create(post=post, user=user)

        article = CmsArticle.objects.filter(status=1).first()
        if article:
            ArticleFavorite.objects.get_or_create(article=article, user=user)

        self.stdout.write(self.style.SUCCESS('✓ 演示数据已就绪（全部为中文内容）'))
        self.stdout.write('  管理员账号: admin / admin12345')
        self.stdout.write('  普通用户:   demo / demo12345')
        self.stdout.write(f'  可领养宠物: {PetProfile.objects.filter(adoption_status="available").count()} 只')
