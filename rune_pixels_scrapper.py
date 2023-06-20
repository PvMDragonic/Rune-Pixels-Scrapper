from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from calendar import monthrange
from datetime import datetime
from time import sleep

def scrap(clans: list[str]) -> list[datetime, int]:
    """Recieves a list of clan names and returns all their recorded daily total XP."""

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    driver.maximize_window()

    everything = []

    for clan in clans:
        URL = f"https://runepixels.com/clans/{clan}/xp-analytics"
        xp = []

        driver.get(URL)
        sleep(5)

        try:
            # Closes initial pop-up.
            driver.find_element(By.XPATH, "//span[@class='close']").click()
            sleep(1)
        except NoSuchElementException:
            pass

        try:
            # Checks if the clan page exists.
            driver.find_element(By.XPATH, f"//div[@class='errors']")
        except NoSuchElementException:
            pass
        else:
            continue

        # Loops year.
        for i in reversed(range(2)):
            year = driver.find_element(By.XPATH, "(//div[@class='selected']//span)[2]")
            year.click()
            sleep(1)

            driver.find_element(By.XPATH, f"//div[@class='items']/div[{i+1}]").click()
            year = int(year.text)
            sleep(1)

            # Loops months.
            for j in reversed(range(12)):
                driver.find_element(By.XPATH, "(//div[@class='selected']//span)[1]").click()
                sleep(1)
                driver.find_element(By.XPATH, f"//div[@class='items']/div[{j+1}]").click()
                sleep(1)

                try:
                    driver.find_element(By.XPATH, f"//span[@class='red-color']")
                except NoSuchElementException:
                    sleep(5)
                else:
                    continue

                canvas = driver.find_element(By.XPATH, "(//canvas)[2]")
                actions = ActionChains(driver)
                actions.scroll_by_amount(0, 50)

                # 0,0 is the middle of the canvas, and size depends on screen's.
                canvas_limit = canvas.size['width'] / 2
                x_pos = canvas_limit * -1
                stats = []
                
                # If a given month's recorded XP starts from the not-beginning, then
                # the days need to be counted backwards. <canvas> tags be dammed.
                beginning_left = None

                while x_pos <= canvas_limit:
                    x_pos += 10
                    # Moves the cursor to the bottom of the canvas to try and reach even the smallest of columns. 
                    actions.move_to_element_with_offset(canvas, x_pos, 260).perform()
                    sleep(0.1)

                    try:
                        temp = driver.find_element(By.XPATH, "//div[@id='chartTooltip']/div[1]/span[2]").text    
                        
                        if temp == '':
                            continue

                        if len(stats) > 0:
                            if temp == stats[-1]:
                                continue
                          
                        # If the first recorded XP isn't at the start of the canvas,
                        # then the days need to be count backwards, beginning at right.   
                        if beginning_left is None:
                            if x_pos > -500:
                                beginning_left = False
                            else:
                                beginning_left = True

                        stats.append(temp)
                        print(f"{clan}: {year}/{j+1}/{stats.index(stats[-1]) + 1} - {temp}")
                    except NoSuchElementException:
                        pass

                if beginning_left:
                    for index, exp in reversed(list(enumerate(stats))):
                        xp.append([
                            datetime(year = year, month = j+1, day = index + 1, hour = 21), 
                            int(exp.replace(" ", ""))
                        ])
                else:
                    for index, exp in enumerate(reversed(stats)):    
                        which_day = monthrange(year, j+1)[1] - index
                        xp.append([
                            datetime(year = year, month = j+1, day = which_day, hour = 21), 
                            int(exp.replace(" ", ""))
                        ])

        everything.append([clan, xp])
    return everything