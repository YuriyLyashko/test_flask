class ForHtml:
    selected_region = 'Please select a region'
    def __init__(self, table_from_db, structure):
        self.table_from_db = table_from_db
        self.structure = structure
        self.regions = self.get_regions()
        self.select_separator = self.get_select_separator()


    def get_regions(self):
        regions = []
        for row in self.table_from_db:
            name = row[self.structure[0]]
            if {'name': name} not in regions:
                regions.append({'name': name})
        return regions

    def get_data_for_region(self, name):
        data_for_region = []
        for row in self.table_from_db:
            if row[self.structure[0]] == name:
                data_for_region.append(
                    [row[self.structure[1]], int(float(row[self.structure[2]]))])
        return data_for_region

    def get_select_separator(self):
        return '--' * max([len(region['name']) for region in self.regions])