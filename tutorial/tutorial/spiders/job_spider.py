import scrapy
import json
import os

prefix = 'https://jenkins.url' # need change
suffix = '/api/json?pretty=true'

def loads (rawbody):
    return json.loads(str(rawbody, 'utf-8'))

class QuotesSpider(scrapy.Spider):
    name = "job"
    http_user = ''   # need change
    http_pass = ''

    def start_requests(self):
        urls = [
            'https://jenkins.url/api/json?pretty=true'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_dashboard)

    def parse_dashboard(self, response):
        # page = response.url.split("/")[-2]
        filename = 'dashboard.json'
        with open(filename, 'wb') as f:
            f.write(response.body)

        content = json.loads(str(response.body, 'utf-8'))
        job_names = [job['name'] for job in content['jobs']]
        for job_name in job_names:
            if job_name.startswith('job-prefix'): # need change
                print(prefix + '/job/' + job_name + suffix)
                yield scrapy.Request(url=prefix + '/job/' + job_name+ suffix, callback=self.parse_job)

    def parse_job(self, response):
        content = loads( response.body )
        print (content)

        filename = 'jobs/' + content['fullDisplayName'] + '/' + 'index.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(json.dumps(content, indent=2).encode('utf-8'))
