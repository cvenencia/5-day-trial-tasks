import pandas as pd


class CSV_Queue:
    def __init__(self):
        self.csv_queue = pd.DataFrame(
            columns=['Course Name', 'Course URL', 'Coupon Code', 'Expiration Date'])

    def add(self, title, url, coupon_code, expire_date):
        if self.already_in_queue(url):
            return False
        else:
            self.csv_queue = pd.concat([pd.DataFrame.from_dict({
                'Course Name': [title],
                'Course URL': [url],
                'Coupon Code': [coupon_code],
                'Expiration Date': [expire_date],
            }), self.csv_queue])
            return True

    def already_in_queue(self, url):
        return url in self.csv_queue['Course URL'].unique()

    def to_csv_file(self):
        return self.csv_queue.to_csv(index=False)

    def __len__(self):
        return len(self.csv_queue.index)


class Counter:
    def __init__(self):
        self.counter = 0

    def increment_counter(self):
        self.counter += 1
