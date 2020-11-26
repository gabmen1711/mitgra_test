from datetime import datetime
import time


class ExerciseTwo:

    __zone_a_total_dif_time = 0
    __zone_b_total_dif_time = 0
    __zone_a_total_i = 0
    __zone_b_total_i = 0
    __zone_w_2_total_entrance = 0
    __extra_data = {}
    __total_assets = []
    __total_cycles = 0

    def __init__(self, json_data: dict):
        self.json_data = json_data
        self.__iterate_data()

    def __iterate_data(self):
        # Init current_iteration params
        last_asset = self.json_data[0]["asset"]
        self.__total_assets.append(last_asset)

        current_asset_cycle = []
        for data in self.json_data:
            cycle = data["cycle"]
            current_asset = data["asset"]
            if self.__total_cycles != cycle:
                self.__total_cycles = self.__total_cycles + 1

            if last_asset == current_asset:
                current_asset_cycle.append(data)
            else:
                if current_asset not in self.__total_assets:
                    # New Asset
                    self.__total_assets.append(current_asset)
                # Get actual assets data calculation
                self.__calculate_data_from_asset_cycle(current_asset_cycle)
                current_asset_cycle.clear()
                current_asset_cycle.append(data)
                last_asset = current_asset

    def __calculate_data_from_asset_cycle(self, current_asset_cycle):
        """

        :param current_asset_cycle:
        :type current_asset_cycle:
        :return:
        :rtype:
        """
        entered_w_2_zone = False
        entered_w_zone_a = False
        entered_w_zone_b = False

        for data in current_asset_cycle:
            zone = data.get("zone")
            if zone in ("AE1", "AE2", "BE1", "BE2"):
                # Convert_both_dates_to_datetime
                date_format = "%Y-%m-%dT%H:%M:%S"
                dt_in = datetime.strptime(data["dt_in"], date_format)
                dt_out = datetime.strptime(data["dt_out"], date_format)
                # Get difference in seconds
                zone_time_spent = (dt_out - dt_in).total_seconds()

                # If Zone AE1 or AE2, add the time dif to __zone_a_total_dif_time
                if zone in ("AE1", "AE2"):
                    self.__zone_a_total_dif_time = (
                        self.__zone_a_total_dif_time + zone_time_spent
                    )
                    self.__zone_a_total_i = self.__zone_a_total_i + 1
                # Else belongs to BE1 or BE2, add the time dif to __zone_b_total_dif_time
                else:
                    self.__zone_b_total_dif_time = (
                        self.__zone_b_total_dif_time + zone_time_spent
                    )
                    self.__zone_b_total_i = self.__zone_b_total_i + 1

            if zone in ("AW2", "BW2") and not entered_w_2_zone:
                entered_w_2_zone = True
                self.__zone_w_2_total_entrance = self.__zone_w_2_total_entrance + 1

            # This is for Extra calculations, allows me to know if Asset entered both Work Zones
            if zone in ("AW1", "AW2"):
                entered_w_zone_a = True
            if zone in ("BW1", "BW2"):
                entered_w_zone_b = True

        asset = current_asset_cycle[0]["asset"]
        if entered_w_zone_a and entered_w_zone_b:
            try:
                asset_in_ed = self.__extra_data[asset]
                asset_in_ed = asset_in_ed + 1
                self.__extra_data.update({asset: asset_in_ed})
            except KeyError:
                # New Asset
                self.__extra_data.update({asset: 1})

    def get_zones_a_b_avg(self):
        """
        Method returns time average of zones A and B.

        :return: average time for zones A and B
        :rtype: dict
        """
        # Zone A
        zone_a_avg_in_mins = self.__zone_a_total_dif_time / self.__zone_a_total_i
        zone_a_avg_in_mins = time.gmtime(zone_a_avg_in_mins)
        zone_a_avg_in_mins = time.strftime("%H:%M:%S", zone_a_avg_in_mins)

        # Zone B
        zone_b_avg_in_mins = self.__zone_b_total_dif_time / self.__zone_b_total_i
        zone_b_avg_in_mins = time.gmtime(zone_b_avg_in_mins)
        zone_b_avg_in_mins = time.strftime("%H:%M:%S", zone_b_avg_in_mins)

        return dict(
            zone_AE=dict(
                avg_time=zone_a_avg_in_mins,
            ),
            zone_BE=dict(
                avg_time=zone_b_avg_in_mins,
            ),
        )

    def get_w_zones_percentage_on_cycles(self):
        """
        Method returns percentage of cycles in faena that entered any Work Area 2

        :return: Percentage calculation made.
        :rtype: dict
        """
        total_assets_on_cycle = self.__total_cycles * len(self.__total_assets)
        calc_resp = (self.__zone_w_2_total_entrance * 100) / total_assets_on_cycle

        return calc_resp

    def get_asset_w_higher_percent_of_entering_both_w_zones(self):
        """
        Method calculates which asset has the highest percent of entering both
        work zones (AW1, AW2, BW1, BW2) of all cycles.

        :return: Asset and Percent calculated
        :rtype: string | int
        """
        asset = ""
        percent = 0
        for k, v in self.__extra_data.items():
            entered_both_w_zones = v
            percent_both_w_zones = (entered_both_w_zones * 100) / self.__total_cycles
            if percent_both_w_zones > percent:
                percent = percent_both_w_zones
                asset = k

        return asset, percent
