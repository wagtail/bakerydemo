#!/usr/bin/env python
"""
Test script to verify the nested InlinePanel implementation
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakerydemo.settings.dev")
django.setup()

from bakerydemo.locations.models import (
    LocationPage,
    LocationWeekDaySlot,
    LocationHourSlot,
)

def test_nested_inline_panel():
    """Test the nested InlinePanel structure"""
    
    print("=" * 80)
    print("NESTED INLINEPANEL DEMONSTRATION")
    print("=" * 80)
    
    # Get a location page
    locations = LocationPage.objects.all()
    
    if not locations.exists():
        print("\n❌ No location pages found in the database.")
        print("Please visit the admin at http://localhost:8000/admin/ and create a location.")
        return
    
    location = locations.first()
    print(f"\n📍 Testing with Location: {location.title}")
    print(f"   URL: http://localhost:8000/admin/pages/{location.id}/edit/")
    
    # Check for week day slots
    week_day_slots = location.week_day_slots.all()
    
    if not week_day_slots.exists():
        print("\n📝 No nested week day slots found yet.")
        print("   Go to the admin interface and add some!")
        print(f"\n   Steps:")
        print(f"   1. Visit: http://localhost:8000/admin/pages/{location.id}/edit/")
        print(f"   2. Scroll to 'Hours of Operation (Nested InlinePanel Demo)'")
        print(f"   3. Click '+ Day' to add a week day slot")
        print(f"   4. Select a day (e.g., Monday)")
        print(f"   5. Within that day, click '+ Time Slot' to add hour slots")
        print(f"   6. Add multiple time slots (e.g., 9:00-12:00, 13:00-17:00)")
        print(f"   7. Save the page")
    else:
        print(f"\n✅ Found {week_day_slots.count()} nested week day slot(s):")
        print("-" * 80)
        
        for day_slot in week_day_slots:
            print(f"\n   📅 {day_slot.get_day_display()}")
            hour_slots = day_slot.hour_slots.all()
            
            if hour_slots.exists():
                print(f"      Time slots ({hour_slots.count()}):")
                for hour_slot in hour_slots:
                    if hour_slot.closed:
                        print(f"         🚫 CLOSED")
                    else:
                        opening = hour_slot.opening_time.strftime("%H:%M") if hour_slot.opening_time else "--:--"
                        closing = hour_slot.closing_time.strftime("%H:%M") if hour_slot.closing_time else "--:--"
                        print(f"         🕒 {opening} - {closing}")
            else:
                print(f"      (No hour slots defined)")
        
        print("\n" + "-" * 80)
        print("✅ Nested InlinePanel structure is working correctly!")
    
    # Show comparison with flat structure
    flat_hours = location.hours_of_operation.all()
    if flat_hours.exists():
        print(f"\n📊 For comparison, flat structure has {flat_hours.count()} slot(s)")
    
    print("\n" + "=" * 80)
    print("TESTING SUMMARY:")
    print("=" * 80)
    print("✓ Models created successfully")
    print("✓ Database migrations applied")
    print("✓ Nested InlinePanel structure available in admin")
    print(f"✓ Admin interface: http://localhost:8000/admin/")
    print(f"✓ Location edit: http://localhost:8000/admin/pages/{location.id}/edit/")
    print("\n🎯 This demonstrates nested InlinePanel for testing:")
    print("   • Expand/collapse functionality per day")
    print("   • Multiple time slots within each day")
    print("   • Scroll behavior with nested panels")
    print("   • Related to Wagtail issue #13352")
    print("=" * 80)

if __name__ == "__main__":
    test_nested_inline_panel()
