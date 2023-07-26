Data sending & receiving program for BANF iSensor, Profiler, GPS measurement.  

![](https://res.cloudinary.com/aivillain/image/upload/v1677481501/Untitled.png_qfker7.png)  

![](https://res.cloudinary.com/aivillain/image/upload/v1677481509/Untitled.png_qjyt2t.png)  

![](https://res.cloudinary.com/aivillain/image/upload/v1677047726/Design_of_Smart_Tire_Profile_System-Data_Acquisition_Software.drawio_qq3gih.png)

# Requirements
- python 3.10.x
- [miniconda](https://docs.conda.io/en/latest/miniconda.html)

# Installation  

```bash
# Assume python 3.10 version is installed
cd xxx/banf_sendreceive # move to project directory
conda env create -f banf_sendreceive_(win64/linux64).yaml # Windows / Ubuntu 20.04 tested
conda activate banf_sendreceive
```

# Usage  

```bash
python sender_main.py (or receiver_main.py)
```

# Structure
  ```
  banf_sendreceive/
  │
  ├── sender_main.py - main Qt GUI Program for send measurement data
  ├── receiver_main.py - receive measurement data & insert to database 
  │
  ├── Pipfile - manage virtual python env & installed packages (created by pipenv)
  ├── Pipfile.lock -  manage virtual python env & installed packages using detailed
  │                   version (created by pipenv)
  │  
  └── utils/ - small utility functions for BANF sensor's raw data.
    ├── etc/ - Features that do not belong to other categories
    │   │  
    │   ├── observe.py - file observing
    │   └── pattern.py - Implement design pattern
    │  
    ├── send_receive/ Implement data sending and receiving
    │   │  
    │   ├── db_inserter.py - Insert incoming data delivered by kafka_consumer.py into DB
    │   ├── kafka_consumer.py - Unpack consume messages from Kafka broker and
    │   │   forward to db_insert.py (Act as individual threads)
    │   ├── mqtt_receiver.py - Implement MQTT subscribe client (not use, just for test)
    │   │   
    │   ├── mqtt_sender.py - Implement MQTT publish client (Act as individual threads)
    │   ├── s3_sender.py - Implement AWS S3 client for save raw txt file
    │   │   (Act as individual threads)
    │   └── 
    │   
    ├── preprocessing.py - Data preprocessing, MQTT packet conversion, GPS sensor time
    │   conversion, etc.
    │   ...
  ```

# Acknowledgments
## BANF R&D Team  

- GW Jeon (BANF Co., Ltd. email : gwjeon@banf.co.kr)
- JY Jeong (BANF Co., Ltd. email : jyjeong@banf.co.kr)
- DH Kim (BANF Co., Ltd. email : kim.donghun@banf.co.kr)
