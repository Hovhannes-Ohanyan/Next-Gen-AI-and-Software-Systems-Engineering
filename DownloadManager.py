import os
import requests
import ftplib
import concurrent.futures

class DownloadManager:
    def __init__(self, max_threads=5, max_processes=2):
        self.max_threads = max_threads
        self.max_processes = max_processes
        self.download_tasks = []
        self.completed_tasks = []

    def download_file(self, url, save_path):
        try:
            response = requests.get(url, stream=True)
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def download_ftp_file(self, url, save_path):
        try:
            ftp = ftplib.FTP(url)
            ftp.login()
            with open(save_path, 'wb') as file:
                ftp.retrbinary('RETR ' + os.path.basename(url), file.write)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def download(self, url, filename):
        save_path = os.path.join(os.getcwd(), filename)
        if url.startswith('http://') or url.startswith('https://'):
            self.download_tasks.append((self.download_file, url, save_path))
        elif url.startswith('ftp://'):
            self.download_tasks.append((self.download_ftp_file, url, save_path))

    def execute_task(self, task):
        func, url, save_path = task
        func(url, save_path)
        self.completed_tasks.append(url)

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.execute_task, task) for task in self.download_tasks]
            concurrent.futures.wait(futures)

    def wait(self):
        pass

if __name__ == "__main__":
    download_manager = DownloadManager(max_threads=5, max_processes=2)

    urls = [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "ftp://example.com/file3.txt",
        "ftp://example.com/file4.txt",
    ]

    for idx, url in enumerate(urls):
        download_manager.download(url, f"file{idx+1}.txt")

    download_manager.start()

    print("All downloads completed.")
