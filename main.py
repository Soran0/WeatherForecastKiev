from selenium import webdriver
from selenium.webdriver.common.by import By
import multiprocessing
import time
import pandas as pd


def web(i, shared_data):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    url = f'http://www.pogodaiklimat.ru/weather.php?id=33345&bday=%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9+%D0%B4%D0%B5%D0%BD%D1%8C&fday=%D0%9F%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B9+%D0%B4%D0%B5%D0%BD%D1%8C&amonth=1&ayear=20{str(i)}&bot=0'
    driver.get(url)
    time.sleep(3)

    try:
        dates_table = driver.find_element(By.CLASS_NAME, 'archive-table-left-column')
        info_table = driver.find_element(By.CLASS_NAME, 'archive-table-wrap')

        for tr, tr_info in zip(dates_table.find_elements(By.TAG_NAME, "tr")[1:],
                               info_table.find_elements(By.TAG_NAME, "tr")[1:]):  # Пропускаем заголовки
            date_cells = tr.find_elements(By.TAG_NAME, "td")
            info_cells = tr_info.find_elements(By.TAG_NAME, "td")

            if date_cells and info_cells:
                date = date_cells[0].text + f':00 {(date_cells[1].text + f".20{i}")}'
                wind_direction = info_cells[0].text
                wind_speed = info_cells[1].text
                visibility = info_cells[2].text.split(' ')[0] + ('000' if 'км' in info_cells[2].text else '')
                temp = info_cells[5].text
                temp_d = info_cells[6].text
                humid = info_cells[7].text
                temp_e = info_cells[8].text
                temp_es = info_cells[9].text
                pressure = info_cells[11].text
                pressure_o = info_cells[12].text

                shared_data.append([date, wind_direction, wind_speed, visibility, temp, temp_d, humid,
                                    temp_e, temp_es, pressure, pressure_o])

    except Exception as e:
        print(f"Ошибка при обработке года 20{i}: {e}")

    driver.quit()


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_data = manager.list()

    years = list(range(11, 26))  # 2010-2024
    processes = []

    for year in years:
        p = multiprocessing.Process(target=web, args=(year, shared_data))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    df = pd.DataFrame(list(shared_data), columns=["date", "wind_direction", "wind_speed", "visibility", "temp",
                                                  "temp_d", "humidity", "temp_e", "temp_es", "pressure", "pressure_o"])
    df.to_csv("weather_data.csv", index=False, encoding="utf-8")

    print("Данные сохранены в weather_data.csv")
