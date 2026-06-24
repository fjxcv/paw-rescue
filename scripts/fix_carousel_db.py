# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
django.setup()

from portal.models import PortalCarousel

TITLE = '\u6b22\u8fce\u9886\u517b'
for row in PortalCarousel.objects.all():
    old = (row.title or '').strip()
    if not old or 'welcome' in old.lower() or 'adoption' in old.lower():
        row.title = TITLE
        row.save(update_fields=['title'])
        print('updated id', row.id, '->', TITLE)
    else:
        print('keep id', row.id, old)
