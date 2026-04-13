from django.core.management.base import BaseCommand

from collaboration.models import Category


class Command(BaseCommand):
    help = '種入預設產業領域（Category）'

    def handle(self, *args, **options):
        items = [
            {
                'name': '醫療生技',
                'slug': 'medical-biotech',
                'icon_name': 'heart-pulse',
                'description': '醫院、診所、生技研發、醫材與法規等相關場景。',
            },
            {
                'name': '法律服務',
                'slug': 'legal',
                'icon_name': 'scale',
                'description': '訴訟、合約、智財、法遵與顧問服務等需求。',
            },
            {
                'name': '傳統製造',
                'slug': 'manufacturing',
                'icon_name': 'factory',
                'description': '產線、供應鏈、品質、設備與工安等製造現場課題。',
            },
            {
                'name': '零售電商',
                'slug': 'retail-ecommerce',
                'icon_name': 'shopping-bag',
                'description': '門市營運、電商平台、物流、會員與行銷轉換。',
            },
            {
                'name': '創意內容',
                'slug': 'creative-content',
                'icon_name': 'palette',
                'description': '影音、出版、設計、遊戲與品牌內容製作與授權。',
            },
        ]
        for row in items:
            obj, created = Category.objects.update_or_create(
                slug=row['slug'],
                defaults={
                    'name': row['name'],
                    'icon_name': row['icon_name'],
                    'description': row['description'],
                },
            )
            action = '建立' if created else '更新'
            self.stdout.write(self.style.SUCCESS(f'{action}: {obj.name} ({obj.slug})'))
