def write_operation_log(operator, module, action, content, target_type=None, target_id=None, ip_address=None):
    from system.models import OperationLog

    OperationLog.objects.create(
        operator=operator,
        module=module,
        action=action,
        content=content,
        target_type=target_type,
        target_id=target_id,
        ip_address=ip_address,
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
