import xlrd
import json
from datetime import datetime

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s = ''
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

if __name__ == '__main__':
    loc = ('data/data.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    data = {
        "title": "Data Visualization: Đường đua Corona tại Châu Âu",
        "source": "Nguồn: thewuhanvirus.com",
        "n_show": 10,
        "height": 480,
        "width": 720,
        "object_height": 36,
        "max_width": 570,
        "margin-bottom": 5,
        "duration": 2000,
        "swap_duration": 120,
        "fps": 60,
    }

    countries = sheet.col_values(0, 3)
    icon_urls = ['icons/' + remove_accents(x).replace(' ', '_').lower() + '.png' for x in countries]

    data["objects"] = []
    for country, icon_url in zip(countries, icon_urls):
        data["objects"].append({
            "name": country,
            "icon_url": icon_url
        })
    
    data["time_points"] = []
    dates = [datetime(*xlrd.xldate_as_tuple(d, 0)) for d in sheet.row_values(2, 1)]
    # dates = [d.strftime("%d/%m/%y") for d in dates][:-1]
    dates = [d.strftime("%d/%m") for d in dates][:-1]

    for j, d in enumerate(dates):
        values = {}
        for i, country in enumerate(countries):
            values[country] = int(sheet.cell_value(i+3, j+1))
        # print(values)
        data["time_points"].append({
            "date": d,
            "values": values
        })

    with open("data/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='    ', ensure_ascii=False)
    with open("data/data.js", 'w', encoding='utf-8') as f:
        f.write('var data = ')
        f.write(json.dumps(data, indent='    ', ensure_ascii=False))
    print("Done!")