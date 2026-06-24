from django.utils import timezone

from system.models import AiInvocationLog, PlatformConfig


class AiQuotaExceededError(Exception):
    def __init__(self, message, quota_type='daily'):
        super().__init__(message)
        self.quota_type = quota_type


def _get_config_int(key, default=0):
    try:
        row = PlatformConfig.objects.get(config_key=key)
        return max(0, int(str(row.config_value).strip() or '0'))
    except (PlatformConfig.DoesNotExist, ValueError, TypeError):
        return default


def get_ai_usage_stats():
    today = timezone.now().date()
    return {
        'today_count': AiInvocationLog.objects.filter(created_at__date=today).count(),
        'total_count': AiInvocationLog.objects.count(),
        'daily_limit': _get_config_int('ai_daily_limit', 0),
        'total_limit': _get_config_int('ai_total_limit', 0),
    }


def check_ai_quota(user):
    """Raise AiQuotaExceededError if platform AI quota is exceeded."""
    stats = get_ai_usage_stats()
    daily_limit = stats['daily_limit']
    total_limit = stats['total_limit']

    if daily_limit > 0 and stats['today_count'] >= daily_limit:
        raise AiQuotaExceededError(
            f'\u4eca\u65e5 AI \u8c03\u7528\u5df2\u8fbe\u4e0a\u9650\uff08{stats["today_count"]}/{daily_limit}\uff09\uff0c\u8bf7\u660e\u5929\u518d\u8bd5\u6216\u8054\u7cfb\u7ba1\u7406\u5458\u3002',
            quota_type='daily',
        )
    if total_limit > 0 and stats['total_count'] >= total_limit:
        raise AiQuotaExceededError(
            f'AI \u7d2f\u8ba1\u8c03\u7528\u5df2\u8fbe\u4e0a\u9650\uff08{stats["total_count"]}/{total_limit}\uff09\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u3002',
            quota_type='total',
        )


def log_quota_exceeded(user, feature_type, request_meta=''):
    AiInvocationLog.objects.create(
        user=user,
        feature_type=feature_type,
        request_meta=request_meta or '',
        result_meta='quota_exceeded',
        success=False,
    )
