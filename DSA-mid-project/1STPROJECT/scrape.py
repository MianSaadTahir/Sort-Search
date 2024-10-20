import threading
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PyQt5 import QtWidgets, QtCore
import sys


class FlipkartScraper(QtCore.QObject):
    progress_updated = QtCore.pyqtSignal(int)
    scraping_finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.names = []
        self.ratings = []
        self.num_of_ratings = []
        self.num_of_reviews = []
        self.descrips = []
        self.original_prices = []
        self.disc_prices = []
        self.unique_products = set()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.total_products_scraped = 0
        self.total_entities = 500

    def scrape(self):
        service = Service(
            executable_path=r'C:\chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service=service)

        driver.get(
            'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=2')

        while not self.stop_event.is_set():
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for a in soup.findAll('div', attrs={'class': 'yKfJKb row'}):
                if self.stop_event.is_set():
                    break
                self.pause_event.wait()

                name = a.find('div', attrs={'class': 'KzDlHZ'})
                rating = a.find('div', attrs={'class': 'XQDdHH'})
                rating_review_parent = a.find(
                    'span', attrs={'class': 'Wphh3N'})

                if rating_review_parent:
                    spans = rating_review_parent.find_all('span')
                    if len(spans) >= 3:
                        rating_text = spans[0].text.strip().split()[0]
                        review_text = spans[3].text.strip().split()[0]
                    else:
                        rating_text = 'N/A'
                        review_text = 'N/A'
                else:
                    rating_text = 'N/A'
                    review_text = 'N/A'

                descrip = a.find('div', attrs={'class': '_6NESgJ'})
                disc_price = a.find('div', attrs={'class': 'Nx9bqj _4b5DiR'})

                if disc_price:
                    clean_disc_price = re.sub(r'[^\d,]', '', disc_price.text)
                else:
                    clean_disc_price = 'N/A'

                original_price = a.find(
                    'div', attrs={'class': 'yRaY8j ZYYwLA'})

                if original_price:
                    clean_original_price = re.sub(
                        r'[^\d,]', '', original_price.text)
                else:
                    clean_original_price = 'N/A'

                product_key = (name.text if name else 'N/A',
                               descrip.text if descrip else 'N/A')
                if product_key not in self.unique_products:
                    self.unique_products.add(product_key)
                    self.names.append(name.text if name else 'N/A')
                    self.ratings.append(rating.text if rating else 'N/A')
                    self.num_of_ratings.append(
                        rating_text if rating else 'N/A')
                    self.num_of_reviews.append(
                        review_text if rating else 'N/A')
                    self.descrips.append(descrip.text if descrip else 'N/A')
                    self.disc_prices.append(clean_disc_price)
                    self.original_prices.append(clean_original_price)

                    # Update progress
                    self.total_products_scraped += 1
                    # Print scraped product count
                    print(f"Scraped {self.total_products_scraped} products")
                    self.progress_updated.emit(self.total_products_scraped)

                    # Stop scraping if we reach the limit of entities
                    if self.total_products_scraped >= self.total_entities:
                        self.scraping_finished.emit()
                        self.save_data()
                        driver.quit()
                        return
            try:
                next_buttons = driver.find_elements(By.CLASS_NAME, "_9QVEpD")
                if len(next_buttons) > 1:
                    next_buttons[1].click()
                    time.sleep(5)
                else:
                    print("No more pages to scrape. Exiting...")
                    self.scraping_finished.emit()
                    self.save_data()
                    driver.quit()
                    break
            except Exception as e:
                print(f"Error: {e}")
                self.save_data()
                driver.quit()
                break

    def save_data(self):
        df = pd.DataFrame({
            'Name': self.names,
            'Rating': self.ratings,
            'Number of Ratings': self.num_of_ratings,
            'Number of Reviews': self.num_of_reviews,
            'Description': self.descrips,
            'Original Price': self.original_prices,
            'Discounted Price': self.disc_prices,
        })

        file_exists = False
        try:
            with open('flipkart.csv', 'r'):
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        # Append the data to the CSV file
        df.to_csv('flipkart.csv', mode='a', index=False,
                  encoding='utf-8', header=not file_exists)
        print("Data saved successfully")


class ScraperApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.scraper = FlipkartScraper()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flipkart Scraper')
        self.setGeometry(300, 300, 300, 200)
        self.start_button = QtWidgets.QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_scraping)
        self.pause_button = QtWidgets.QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_scraping)
        self.resume_button = QtWidgets.QPushButton('Resume', self)
        self.resume_button.clicked.connect(self.resume_scraping)
        self.stop_button = QtWidgets.QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_scraping)

        self.progress = QtWidgets.QProgressBar(self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.resume_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        self.scraper.progress_updated.connect(self.update_progress)
        self.scraper.scraping_finished.connect(self.scraping_done)

    def start_scraping(self):
        self.scraper.stop_event.clear()
        self.scraper.pause_event.set()
        self.scraping_thread = threading.Thread(target=self.scraper.scrape)
        self.scraping_thread.start()

    def pause_scraping(self):
        self.scraper.pause_event.clear()

    def resume_scraping(self):
        self.scraper.pause_event.set()

    def stop_scraping(self):
        self.scraper.stop_event.set()

    def update_progress(self, value):
        self.progress.setValue(
            int((value / self.scraper.total_entities) * 100))

    def scraping_done(self):
        QtWidgets.QMessageBox.information(self, "Done", "Scraping finished!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ScraperApp()
    ex.show()
    sys.exit(app.exec_())
