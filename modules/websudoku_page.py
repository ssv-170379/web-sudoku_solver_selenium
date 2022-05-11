from selenium.webdriver.common.by import By


class WebSudokuPage:
    difficulty = 4  # 1-4 - Easy, Medium, Hard, Evil

    url = f'https://websudoku.com/?level={difficulty}'
    submit_button = (By.NAME, 'submit')  # The button with text 'How am I doing?'

    def cell(self, y, x):
        return By.ID, f'f{x}{y}'

    grid_size = 9

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.url)
        self.driver.switch_to.frame(0)  # This frame contains game board. There's single frame on this page, and it has no name, So we use index instead.

    def get_grid(self) -> (int, list):  # Read current grid from the webpage
        grid = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                val = self.driver.find_element(*self.cell(y, x)).get_attribute('value')
                row.append(int(val) if val else 0)  # get value or 0 if cell is empty
            grid.append(row)
        return self.grid_size, grid

    def set_grid(self, grid_data: list):  # Fill empty cells of the grid with solved board's data
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                element = self.driver.find_element(*self.cell(y, x))
                if not element.get_attribute('value'):  # fill only empty cells
                    element.send_keys(grid_data[y][x])

    def submit(self):  # Submit solved board
        self.driver.find_element(*self.submit_button).click()
