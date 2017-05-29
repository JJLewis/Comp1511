//
// Created by Jordan Lewis on 13/5/17.
//

#include "world.h"
#include <stdbool.h>
#include <stdlib.h>

location_t find_start_location(location_t a_location) {
    location_t current = a_location;
    while (current->type != LOCATION_START) {
        current = current->next;
    }
    return current;
}

location_t highest_buyer_of_commodity(bot_t bot, commodity_t commodity) {
    location_t buyers[MAX_LOCATIONS] = {0};
    int numBuyers = all_buyers_of_commodity(bot, commodity, buyers);

    location_t highest = buyers[0];
    for (int i = 0; i < numBuyers; i++) {
        location_t a_location = buyers[i];
        if (a_location->quantity > 0) {
            if (a_location->price > highest->price) {
                highest = a_location;
            }
        }
    }

    return highest;
}

location_t lowest_seller_of_commodity(bot_t bot, commodity_t commodity) {
    location_t sellers[MAX_LOCATIONS] = {0};
    int numSellers = all_sellers_of_commodity(bot, commodity, sellers);

    location_t lowest = sellers[0];
    for (int i = 0; i < numSellers; i++) {
        location_t a_location = sellers[i];
        if (a_location->quantity > 0) {
            if (a_location->price < lowest->price) {
                lowest = a_location;
            }
        }
    }

    return lowest;
}

bool will_pass_petrol(location_t start, location_t end) {
    int direction = distance_to_direction(distance_between(start, end));

    location_t tracker = start;
    while (tracker != end) {
        if (tracker->type == LOCATION_PETROL_STATION) {
            if (tracker->quantity > 0) {
                return true;
            }
        }
        shift_location(tracker, direction);
    }

    return false;
}

// TODO: Remember that a -1 for min distance will return a 'self sustaining' petrol station, ie, enough fuel to cover the distance travelled for it
// Should it be 2x the distance?
location_t nearest_petrol_station(location_t location, int minimumFuel) {
    location_t stations[MAX_LOCATIONS];
    int numStations = all_petrol_stations(location, stations);

    location_t closest = NULL;//stations[0];
    int closestDistance = -1;//true_distance_between(location, closest);
    for (int i = 0; i < numStations; i++) {
        location_t a_location = stations[i];
        int distance = true_distance_between(location, a_location);

        if (minimumFuel == -1) {
            minimumFuel = distance;
        }

        if (a_location->quantity >= minimumFuel) {
            if (distance < closestDistance) {
                closestDistance = distance;
                closest = a_location;
            } else {
                if (closest == NULL) {
                    closestDistance = distance;
                    closest = a_location;
                }
            }
        }
    }

    return closest;
}

location_t closest_buyer_of_commodity_to(bot_t bot, location_t location, commodity_t commodity) {
    location_t buyers[MAX_LOCATIONS];
    int num_buyers = all_buyers_of_commodity(bot, commodity, buyers);

    location_t closest_buyer = buyers[0];
    int least_distance = true_distance_between(location, closest_buyer);
    for (int i = 1; i < num_buyers; i++) {
        location_t buyer = buyers[i];
        int distance = true_distance_between(location, buyer);
        if (distance < least_distance) {
            closest_buyer = buyer;
            least_distance = distance;
        }
    }

    return closest_buyer;
}

location_t best_buyer_of_commodity_to(bot_t bot, location_t location, commodity_t commodity) {
    location_t buyers[MAX_LOCATIONS];
    int num_buyers = all_buyers_of_commodity(bot, commodity, buyers);

    location_t best_buyer = buyers[0];
    int distance = true_distance_between(location, best_buyer);
    double best_ratio = (double)best_buyer->price;
    
    if (distance > 0) {
	    best_ratio = (double)best_buyer->price / (double)true_distance_between(location, best_buyer);
    }

    for (int i = 1; i < num_buyers; i++) {
        location_t buyer = buyers[i];
        distance = true_distance_between(location, buyer);
        int price = buyer->price;
        double ratio = (double)price / (double)distance;
        if (ratio > best_ratio) {
            best_buyer = buyer;
            best_ratio = ratio;
        }

    }

    return best_buyer;
}

bool will_pass_location(location_t start, location_t end, location_t x) {
    location_t tracker = start;
    int distance = distance_between(start, end);
    int direction = distance_to_direction(distance);
    for (int i = 0; i < distance * direction; i++) {
        shift_location(tracker, direction);
        if (is_location_equal(tracker, x)) {
            return true;
        }
    }
    return false;
}