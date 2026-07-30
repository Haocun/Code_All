import csv
import sys

class Count:
    data = []
    detections = 0
    detection_rate = 0

    def get_detections(self):
        for c in self.data:
            if int(c) > 0:
                self.detections += 1

        return self.detections

    def get_detection_rate(self):
        self.detection_rate = self.detections / len(self.data) if len(self.data) > 0 else 0
        return self.detection_rate


count = Count()


def get_count(name: str):
    with open(name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3 and row[2].isdigit():
                count.data.append(row[2])



if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_count(sys.argv[1])
    else:
        get_count(sys.stdin.read().strip())


    print("tags: ", len(count.data))
    print("detections", count.get_detections())
    print("detection rate: ", count.get_detection_rate())