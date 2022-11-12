import unittest
from appcore.map_model import MapModel
from appcore.station_model import StationModel


class TestMapModel(unittest.TestCase):

    mm = MapModel('../ultrabuddy_db_multi.db', 'vitosha100')

    def test_MapModel_points_initialized_correctly__with_vitosha100_data__expect_first_and_last_points_match(self):
        calculated_first_point = self.mm.points[0]
        calculated_last_point = self.mm.points[-1]
        actual_first_point = (42.652176, 23.280304, 673.6, 0.02597906723502291)
        actual_last_point = (42.654959, 23.277752, 660.6, 97.91112007985886)
        self.assertTupleEqual(calculated_first_point, actual_first_point)
        self.assertTupleEqual(calculated_last_point, actual_last_point)

    def test_MapModel_model_stations_initialized_correctly__with_vitosha100_data__expect_correct_number_of_stations(self):
        # check all objects in self.model_stations are instances of StationModel
        self.assertTrue(all(isinstance(st, StationModel) for st in self.mm.model_stations))
        calculated_number_of_stations = len(self.mm.model_stations)
        actual_number_of_stations = 10
        self.assertEqual(calculated_number_of_stations, actual_number_of_stations)

    def test_MapModel_map_center_calculated_correctly__with_vitosha100_data__expect_correct_lat_lon(self):
        calculated_lat = self.mm.map_center[0]
        calculated_lon = self.mm.map_center[1]
        actual_lat = 42.571258
        actual_lon = 23.261771
        self.assertAlmostEqual(calculated_lat, actual_lat, 5)
        self.assertAlmostEqual(calculated_lon, actual_lon, 5)

    def test_MapModel_get_closest_point_on_track__with_point_on_track__expect_point_on_track_returned_runner_path_updated(self):
        result = self.mm.get_closest_point_on_track(42.50049, 23.206102)
        actual_closest_trackpoint = (42.50049, 23.206102, 1004.8, 38.14070120487804)
        self.assertTupleEqual(result, actual_closest_trackpoint)

    def test_MapModel_get_closest_point_on_track__with_point_NOT_on_track__expect_point_on_track_returned_runner_path_updated(self):
        result = self.mm.get_closest_point_on_track(42.51049, 23.206102)
        actual_closest_trackpoint = (42.50049, 23.206102, 1004.8, 38.14070120487804)
        self.assertTupleEqual(result, actual_closest_trackpoint)

    def test_MapModel_get_next_station_info__with_point_next_to_Chuyipetlevo__expect_correct_next_station_dict_returned(self):
        self.mm.update_model_from_gps_pos(42.50049, 23.206102)
        result = self.mm.get_next_station_info()
        calculated_next_station_name = result['next'].name
        calculated_closest_station_name = result['closest'].name
        calculated_elev_gain = result['gain']
        calculated_elev_loss = result['loss']
        calculated_to_finish = result['end']
        self.assertEqual(calculated_next_station_name, 'Chuyipetlevo', 'next_station_incorrect')
        self.assertEqual(calculated_closest_station_name, 'Studena', 'closest_station_incorrect')
        self.assertAlmostEqual(calculated_elev_gain, 242.40, 1, 'elevation gain incorrect')
        self.assertAlmostEqual(calculated_elev_loss, -9.0, 0, 'elevation loss incorrect')
        self.assertAlmostEqual(calculated_to_finish, 59.77, 1, 'distance to finish incorrect')

class TestStationModel(unittest.TestCase):

    st = StationModel('Studena', 42.507056, 23.152753, 883.8, 32.49510596196858, None)

    def test_StationModel_initialized_correctly__with_vitosha100_Studena_station_data(self):
        self.assertEqual(self.st.name, 'Studena')
        self.assertAlmostEqual(self.st.lat, 42.507056)
        self.assertAlmostEqual(self.st.lon, 23.152753)
        self.assertAlmostEqual(self.st.elev, 883.8)
        self.assertAlmostEqual(self.st.dist, 32.4951, 3)
        self.assertFalse(self.st.dist_diff)

    def test_StationModel_update_station_dist_diff_from_runner(self):
        self.st.update_station_dist_diff_from_runner(30)
        self.assertAlmostEqual(self.st.dist_diff, 2.4951, 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMapModel())
    suite.addTest(TestStationModel())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)

