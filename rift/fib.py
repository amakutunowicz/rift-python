import sortedcontainers

import packet_common
import route
import table

# TODO: If on Linux, and if running in stand-alone mode, program FIB routes into the kernel

class ForwardingTable:

    def __init__(self, address_family):
        self.address_family = address_family
        # Sorted dict of Route objects indexed by prefix. We use the Route class for both the RIB
        # and the FIB, although not all Route attributes are relevant for the FIB.
        self.routes = sortedcontainers.SortedDict()

    def get_route(self, prefix):
        packet_common.assert_prefix_address_family(prefix, self.address_family)
        if prefix in self.routes:
            return self.routes[prefix]
        else:
            return None

    def put_route(self, rte):
        packet_common.assert_prefix_address_family(rte.prefix, self.address_family)
        self.routes[rte.prefix] = rte

    def del_route(self, prefix):
        # Returns True if the route was present in the table and False if not.
        packet_common.assert_prefix_address_family(prefix, self.address_family)
        if prefix in self.routes:
            del self.routes[prefix]
            return True
        else:
            return False

    def all_routes(self):
        for _prefix, rte in self.routes.items():
            yield rte

    def cli_table(self):
        tab = table.Table()
        tab.add_row(route.Route.cli_summary_headers())
        for rte in self.all_routes():
            tab.add_row(rte.cli_summary_attributes())
        return tab

    def nr_routes(self):
        return len(self.routes)