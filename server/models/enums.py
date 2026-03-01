import enum

class GlobalRoleEnum(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    owner = 'owner'
    root = 'root'

class GroupRoleEnum(str, enum.Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'
    owner = 'owner'
    root = 'root'

class AuthProviderEnum(str, enum.Enum):
    email = 'email'
    google = 'google'

class MailStatusEnum(str, enum.Enum):
    draft = 'draft'
    pending_approval = 'pending_approval'
    approved = 'approved'
    rejected = 'rejected'
    sent = 'sent'

class NotificationTypeEnum(str, enum.Enum):
    approval_requested = 'approval_requested'
    mail_approved = 'mail_approved'
    mail_rejected = 'mail_rejected'
    mail_sent = 'mail_sent'
    added_to_group = 'added_to_group'
    removed_from_group = 'removed_from_group'
    role_changed = 'role_changed'
