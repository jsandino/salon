# pylint: disable=all
import pytest
from salon import Customer, Stylist


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


def test_cusomer_creation_generates_name():
    c1 = Customer.create()
    assert "Customer-1" == c1.name
    c2 = Customer.create()
    assert "Customer-2" == c2.name
