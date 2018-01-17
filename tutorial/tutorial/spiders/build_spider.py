import scrapy
import json
import os

prefix = 'https://jenkins.url'     # need change
suffix = '/api/json?pretty=true'
TARGET_HISTORY = 20

def loads (rawbody):
    return json.loads(str(rawbody, 'utf-8'))

class BuildSpider(scrapy.Spider):
    name = "build"
    http_user = ''   # need change
    http_pass = ''

    def start_requests(self):
        urls = [
        ]

        for job in os.listdir('jobs'):
            indexfile = 'jobs/%s/index.json' % job
            with open(indexfile, 'r') as f:
                content = json.loads("".join(f.readlines()).replace('\n', ''))

                if (len(content['builds']) > 0):
                    urls.append(content['builds'][0]['url'] + 'api/json')

                for build in content['builds']:
                    build_no = build['number']
                    if not os.path.isfile('jobs/%s/builds/%s.json' % (job, build_no)):
                        urls.append(build['url'] + 'api/json')
                # urls += [build['url'] + 'api/json' for build in content['builds']]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = loads(response.body)
        [job_name, build_no] = content['fullDisplayName'].split(' #')
        filename = 'jobs/%s/builds/%s.json' % (job_name, build_no)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(json.dumps(content, indent=2).encode('utf-8'))