from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not username:#
            raise ValueError('Users must have an name')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)#normalize_emailは正規表現化
        username = self.model.normalize_username(username)


        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):#
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)#

    def create_superuser(self, username, email, password, **extra_fields):#
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username ,email, password, **extra_fields)#


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    username = models.CharField(_('username'), max_length=30, unique=True)#
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']#nameを入れないとcreatesuperuserで作成できない

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


###########################################################################


class Nation(models.Model):
  name = models.CharField(max_length=100, unique=True)
  def __str__(self):
    return self.name

class Club(models.Model):
  name = models.CharField(max_length=100, unique=True)
  nation = models.ForeignKey('Nation', related_name='club', on_delete=models.PROTECT)
  def __str__(self):
    return self.name

positions = (
    ('FW','FW'),
    ('MF','MF'),
    ('DF','DF')
)

leagues = (
  ('Premier', 'Premier'),
  ('Liga', 'Liga'),
  ('Serie A', 'Serie A'),
  ('Bundes', 'Bundes'),
  ('Ligue 1', 'Ligue 1'),
)

class Player(models.Model):
  name = models.CharField(max_length=50)

  nation = models.ForeignKey('Nation',related_name='player',on_delete=models.PROTECT)

  age = models.IntegerField()

  league = models.CharField(max_length=50, choices=leagues,default='Liga')

  club = models.ForeignKey('Club',related_name='player', on_delete=models.PROTECT, default='Barcelona')

  position = models.CharField(max_length=30, choices=positions)

  image = models.ImageField(upload_to='playerImages/', null=True, blank=True)

  # image_thumbnail = ImageSpecField(
  #   source='image',
  #   processors=[ResizeToFill(100,100)],
  #   format='JPEG',
  #   options={'quality': 60}
  # )

  feature = models.TextField(max_length=400, null=True, blank=True)

  def __str__(self):
    return self.name

