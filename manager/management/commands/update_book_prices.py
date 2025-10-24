from django.core.management.base import BaseCommand
from manager.models import Book
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update all book prices to fixed price of ¥6.99'

    def handle(self, *args, **options):
        fixed_price = Decimal('6.99')
        
        # Get all books
        books = Book.objects.all()
        total_books = books.count()
        
        if total_books == 0:
            self.stdout.write(self.style.WARNING('No books found in the database.'))
            return
        
        # Update all books
        updated_count = 0
        for book in books:
            old_price = book.price
            book.price = fixed_price
            book.save()
            updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Updated "{book.name}" from ¥{old_price} to ¥{fixed_price}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully updated {updated_count}/{total_books} books to ¥{fixed_price}'
            )
        )
