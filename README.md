# quora_crawl
Script to dowload questions related to a particular topic on Quora

# Requirements
- Python 2
run `pip install -r requirements.txt`

# Basic Usage
```
python question_scroller.py --help
```

```
usage: question_scroller.py [-h] [--topic TOPIC] [--num_posts NUM_POSTS]
                            [--driver_location DRIVER_LOCATION]

optional arguments:
  -h, --help            show this help message and exit
  --topic TOPIC         topic name
  --num_posts NUM_POSTS
                        No. of questions to be scraped
  --driver_location DRIVER_LOCATION
                        Location of your chromedriver

```
