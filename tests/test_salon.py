# pylint: disable=all
import time
import pytest
from salon import Clock, Customer, Salon, Stylist

# Stylist


def test_customer_assignment_sets_minutes():
    stylist = Stylist("ann")
    customer = Customer("joe")
    assert 0 == stylist.minutes
    stylist.assign(customer)
    assert 30 == stylist.minutes


def test_customer_assignment_sets_customer():
    stylist = Stylist("ann")
    customer = Customer("joe")
    assert not stylist.customer
    stylist.assign(customer)
    assert customer == stylist.customer


# Customer


def test_cusomer_creation_generates_name():
    c1 = Customer.create()
    assert "Customer-1" == c1.name
    c2 = Customer.create()
    assert "Customer-2" == c2.name


# Clock


def test_clock_notifies_callback_every_virtual_minute():
    clock = Clock()
    assert (9, 0) == (clock.hour, clock.mins)

    minutes_so_far = 0
    minutes_elapsed = 15

    def on_time_notification():
        nonlocal minutes_so_far
        minutes_so_far += 1
        if minutes_so_far == minutes_elapsed:
            clock.active = False

    clock.start([on_time_notification])
    assert (9, 15) == (clock.hour, clock.mins)


# Salon


def test_opening_salon_changes_status():
    salon = Salon([])
    salon.clock.start = lambda _: []  # mock clock start for this test
    assert salon.is_open == False
    salon.open()
    assert salon.is_open == True


def test_opening_salon_starts_clock():
    salon = Salon([])

    clock_started = False

    def on_clock_start(listeners=[]):
        nonlocal clock_started
        clock_started = True

    salon.clock.start = on_clock_start  # mock clock start to assert invocation
    assert clock_started == False
    salon.open()
    assert clock_started == True


def test_check_closing_time_before_closing_time():
    salon = Salon([])
    salon.clock.start = lambda _: []
    salon.clock.active = True
    salon.open()
    salon.clock.hour, salon.clock.mins = 16, 59
    assert salon.is_open == True
    assert salon.clock.active == True
    salon.check_closing_time()
    assert salon.is_open == True
    assert salon.clock.active == True


def test_check_closing_time_after_closing_time():
    salon = Salon([])
    salon.clock.start = lambda _: []
    salon.clock.active = True
    salon.open()
    salon.clock.hour, salon.clock.mins = 17, 0
    assert salon.is_open == True
    assert salon.clock.active == True
    salon.check_closing_time()
    assert salon.is_open == False
    assert salon.clock.active == False


def test_check_closing_time_after_closing_time_haircuts_in_progress():
    stylist = Stylist("Ben")
    stylist.assign(Customer("Joe"))
    salon = Salon([stylist])
    salon.clock.start = lambda _: []
    salon.clock.active = True
    salon.open()
    salon.clock.hour, salon.clock.mins = 17, 0
    assert salon.is_open == True
    assert salon.clock.active == True
    salon.check_closing_time()
    assert salon.is_open == False
    assert salon.clock.active == True


def test_check_for_customers_with_salon_open_no_customers_yet():
    salon = Salon([])
    salon.is_open = True
    salon.clock.mins = 1
    assert not salon.waiting_customers
    salon.check_for_customers()
    assert not salon.waiting_customers


def test_check_for_customers_with_salon_open_customer_arrived():
    salon = Salon([])
    salon.is_open = True
    salon.clock.mins = 7
    assert not salon.waiting_customers
    salon.check_for_customers()
    assert salon.waiting_customers


def test_check_for_customers_with_salon_closed_customer_arrived():
    salon = Salon([])
    salon.is_open = False
    salon.clock.mins = 7
    assert not salon.waiting_customers
    salon.check_for_customers()
    assert not salon.waiting_customers


def test_assign_next_customer_no_customers_waiting():
    ann = Stylist("Ann")
    salon = Salon([ann])
    salon.is_open = True
    assert ann.customer == None
    salon.assign_next_customer_to(ann)
    assert ann.customer == None


def test_assign_next_customer_customer_waiting():
    ann = Stylist("Ann")
    customer = Customer("Joe")
    salon = Salon([ann])
    salon.is_open = True
    salon.waiting_customers.append(customer)
    assert ann.customer == None
    salon.assign_next_customer_to(ann)
    assert ann.customer == customer


def test_assign_next_customer_customer_waiting_salon_closed():
    ann = Stylist("Ann")
    customer = Customer("Joe")
    salon = Salon([ann])
    salon.is_open = False
    salon.waiting_customers.append(customer)
    assert ann.customer == None
    salon.assign_next_customer_to(ann)
    assert ann.customer == None


def test_update_stylist_progress_with_haircut_in_progress():
    ann = Stylist("Ann")
    ann.assign(Customer("Joe"))
    salon = Salon([ann])
    salon.is_open = True
    assert ann.minutes == 30
    salon.update_stylist_progress()
    assert ann.minutes == 29


def test_update_stylist_progress_on_new_assignment():
    ann = Stylist("Ann")
    ann.assign(Customer("Joe"))
    salon = Salon([ann])
    salon.is_open = True
    salon.waiting_customers.append(Customer("Frank"))
    ann.minutes = 0
    salon.update_stylist_progress()
    assert ann.minutes == 29
