"""
Hair Salon simulation.
"""

from dataclasses import dataclass
import time


@dataclass
class Customer:
    """
    A salon's customer looking for a haircut.
    """

    name: str
    satisfied: bool = False
    cid: int = 0

    @classmethod
    def create(cls):
        """
        Factory method to create customers with an auto-generated name
        """
        cls.cid += 1
        return Customer(f"Customer-{cls.cid}")

    @property
    def mood(self):
        """
        Sepecifies a customer' sentiment towards the salon.
        """
        return "Satisfied" if self.satisfied else "Furious"

    def __str__(self):
        return self.name


class Stylist:
    """
    A Stylist working at the Hair Salon.

    Each stylist keeps track of the customer they are currently serving.
    """

    def __init__(self, name):
        self.name = name
        self.customer = None
        self.minutes = 0

    def assign(self, customer: Customer):
        """
        Assigns a customer to this stylist.

        A stylist is assumed to start cutting the customer's hair as soon as a customer is assigned.
        """
        self.minutes = 30
        self.customer = customer

    @property
    def available(self):
        """
        Indicates whether or not this stylist can take a customer.
        """
        return not self.customer

    def cut_hair(self):
        """
        Tells the stylist to continue with the hair cut, until the haircut is done.
        """
        self.minutes -= 1
        if self.is_done():
            self.customer.satisfied = True

    def is_done(self) -> bool:
        """
        Indicates whether the stylist is done the current customer's haircut.
        """
        return self.minutes == 0

    def __str__(self):
        return self.name


class Salon:
    """
    Haircut Salon representation, keeping track of all stylists currently on-shift.
    """

    def __init__(self, stylists: list[Stylist]):
        self.stylists = stylists
        self.waiting_customers = []
        self.clock = Clock()
        self.is_open = False
        self.closing_time = (17, 0)

    def open(self):
        """
        Opens the salon for business.

        This starts the clock tracking time for a workday.
        """
        self.log_event("Hair salon opened")
        self.is_open = True
        self.clock.start(
            [
                self.check_closing_time,
                self.check_for_customers,
                self.check_stylist_progress,
            ]
        )

    def check_closing_time(self):
        """
        Checks if it's time to close doors.
        """
        if self.clock.time >= self.closing_time:
            self.is_open = False
            self.clock.active = False

    def check_for_customers(self):
        """
        Checks if a customer has arrived
        """
        if self.is_open and self.customer_arrived():
            self.customer_entered(Customer.create())

    def customer_arrived(self) -> bool:
        """
        Returns whether or not a customer has arrived.

        A customer arrives every 7 minutes.
        """
        customer_arrival_time = 7
        return self.clock.mins % customer_arrival_time == 0

    def log_event(self, msg: str):
        """
        Prints interesting events happening at the salon,
        prefixed with the current times in HH:MM format.
        """
        curtime = self.clock.current_time()
        print(f"{curtime} {msg}")

    def customer_entered(self, customer: Customer):
        """
        Recevies an incoming customer.

        The customer is added to a waiting queue, until a stylist
        becomes available.
        """
        self.log_event(f"{customer} entered")
        self.waiting_customers.append(customer)
        stylist = self.next_available()
        if stylist:
            self.assign_next_customer_to(stylist)

    def assign_next_customer_to(self, stylist: Stylist):
        """
        Assigns the customer to a stylist, effectively starting the customer's haircut.
        """
        if self.waiting_customers:
            customer = self.waiting_customers.pop(0)
            stylist.assign(customer)
            self.log_event(f"{stylist} started cutting {customer}'s hair")

    def next_available(self) -> Stylist:
        """
        Returns the next available stylist, or None if everyone's busy.
        """
        free = [s for s in self.stylists if s.available]
        return free[0] if free else None

    def check_stylist_progress(self):
        """
        Checks the status of all stylists currently performing haircuts.
        """
        busy = [s for s in self.stylists if not s.available]
        for stylist in busy:
            if stylist.is_done():
                self.log_event(f"{stylist} ended cutting {stylist.customer}'s hair")
                self.log_event(f"{stylist.customer} left {stylist.customer.mood}")
                self.assign_next_customer_to(stylist)
            else:
                stylist.cut_hair()

    def haircut_in_progress(self) -> bool:
        """
        Checks if any stylist is still working.
        """
        busy = [s for s in self.stylists if not s.available]
        return len(busy) > 0

    def kick_out_customers(self):
        """
        Kicks out all waiting customers out of the salon.
        """
        for customer in self.waiting_customers:
            self.log_event(f"{customer} left {customer.mood}")


class Clock:
    """
    An abstraction representing the passage of time while the salon is opened.

    To simulate a 9 to 5 eight hour shift, this clock uses one second to simulate one hour.

    Once the clock is started, it will emit a notification every (simulated) minute to any
    registered listeners; this allows the listeners to act on a time-specific event.
    """

    def __init__(self):
        self.hour, self.mins = (9, 0)
        self.active = False

    def start(self, listeners: list[callable]):
        """
        Starts the salon clock.

        Oncer started, the clock will run until explicitly stopped by a calling client.

        All supplied listeners are notified every minute.
        """
        self.active = True
        while self.active:
            self.wait_one_minute()
            for time_listener in listeners:
                time_listener()

    def wait_one_minute(self):
        """
        Simulates passage of time: every second simulates 60 minutes.

        The clock's hour and minute attributes are updated to reflect the minute
        that just elapsed.
        """
        time.sleep(1 / 60)
        self.mins += 1
        if self.mins >= 60:
            self.hour += 1
            self.mins = 0

    @property
    def time(self) -> tuple[int, int]:
        """
        The current clock time as a tuple
        """
        return (self.hour, self.mins)

    def current_time(self):
        """
        Returns the current clock time, in a string formatted as HH:MM
        """
        return f"{self.hour:02d}:{self.mins:02d}"


def main():
    """
    Entry point.

    A salon is created with its 4 stylists; it is then opened for business and,
    at the end of the day, any waiting customers are kicked-out.
    """
    salon = Salon([Stylist("Ann"), Stylist("Ben"), Stylist("Carol"), Stylist("Derek")])
    salon.open()
    salon.kick_out_customers()


if __name__ == "__main__":
    main()
