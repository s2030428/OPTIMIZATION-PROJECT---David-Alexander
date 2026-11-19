    from airports import airport_data

'''
Open the raw .txt of Loganair flight data and make it into a list. This is done so that we can use list indexing to process the data.
'''
lines = []

with open('Loganair Timetable data.txt') as raw: # open .txt with unprocessed Loganair flight schedule data 
    
    for line in raw: # add each line string as a list element, so that it can be indexed
        lines.append(line)


'''
Create a list of flights, each flight itself a list of the form
[Departure airport, Arrival airport, flight no., departure time, arrival time, frequency, stops, service start date, service end date].
Each element of a flight's data is a string object.
'''
list_of_flights = []

for i in range(len(lines)): 
    flight_data = []
    if 'From' in lines[i]:

        # split the sentence of flight path into the departure airport and the arrival airport for the flight. 
        # Special care is needed since some airport names are more than 1 word long.
        
        flight_path_split = lines[i].split(' to ') 
        out_flight = ' '.join(flight_path_split[0].split(' ')[1:])
        in_flight = ' '.join(flight_path_split[1].split(' '))
        
    elif ('LM' in lines[i]) or ('WF' in lines[i]):
        flight_data.append(out_flight)
        flight_data.append(in_flight.split('\n')[0])

        for j in range(7):
            flight_data.append(lines[i+j].split('\n')[0])

        list_of_flights.append(flight_data)


'''
Further process flights to remove those with >0 stops, those which don't fly on a Monday and those whose service period doesn't begin on 19/10/2026. Each flight in
the list usable_flights is a list of the format [Departure airport, Arrival airport, flight no., departure time, arrival time], with each element of each flight being
a string object.
'''
usable_flights = []

day_of_the_week = 'Mon'
service_start_date = '19/10/2026'

for flight in list_of_flights:
    
    if flight[6] == '0':
        if day_of_the_week in flight[5]:
            if flight[7] == service_start_date:
                usable_flights.append(flight[:5])

print(usable_flights)


'''
Count the number of arrivals and departures to each airport from the list usable_flights. The dictionary airports data has the airports 
as its keys, and 2-lists of integers as the associated values. The first value represents the number of departure flights from that 
airport, while the second value represents the number of arrival flights.
'''
airports_arr_and_dept = {}

for flight in usable_flights:
    out_airport, in_airport, flight_no, out_time, in_time = flight

    # add all departure airports to airport flight data dictionary
    if (out_airport not in airports_arr_and_dept):
        airports_arr_and_dept[out_airport] = [0,0]

    # add all arrival airports to airport flight data dictionary
    if (in_airport not in airports_arr_and_dept):
        airports_arr_and_dept[in_airport] = [0,0]

    # count each time there is a departure or arrival
    airports_arr_and_dept[out_airport][0] += 1
    airports_arr_and_dept[in_airport][1] += 1


list_of_airport_codes = []
for airport in airports_arr_and_dept.keys():
    list_of_airport_codes.append(airport.split(' ')[-1][1:-1])

airport_distances_matrix = airport_data.calculate_distance_matrix(list_of_airport_codes)['distances']

