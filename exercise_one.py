class ExerciseOne:
    __qty_cities = 0
    __var_1_sum = 0
    __sum_var2_prov_2 = 0
    __max_var_1_reg_4 = 0

    def __init__(self, json_data: dict):
        self.all_data = json_data
        self.__iterate_data()

    def __iterate_data(self):
        """
        Iterates all received data and calculates all necessary
        information
        """
        for data in self.all_data:
            region_name = data["name"]
            is_region_4 = False
            if region_name == "Region4":
                is_region_4 = True
            for province_data in data["children"]:
                self.__qty_cities = self.__qty_cities + len(province_data["children"])
                is_province_2 = False
                if province_data["name"] == "Provincia2":
                    is_province_2 = True
                for cities_data in province_data["children"]:
                    values = cities_data["values"]
                    self.__var_1_sum = self.__var_1_sum + values["var1"]
                    if is_province_2:
                        self.__sum_var2_prov_2 = self.__sum_var2_prov_2 + values["var2"]
                    if is_region_4:
                        var_1 = values["var1"]
                        if var_1 > self.__max_var_1_reg_4:
                            self.__max_var_1_reg_4 = var_1

    def get_var_1_avg(self):
        """
        Returns var1 average calculation

        :return: Var 1 Average calculated
        :rtype: float
        """
        var_1_avg = self.__var_1_sum / self.__qty_cities

        return var_1_avg

    def get_prov_2_sum_var_2(self):
        """
        Returns sum of all var2 from province2

        :return: var2 sum for province2
        :rtype: int
        """
        return self.__sum_var2_prov_2

    def get_reg_4_var_1_max(self):
        """
        Return max number from var1 on Region4

        :return: Max number var1 on Region4
        :rtype: int
        """
        return self.__max_var_1_reg_4
