const data = require('../data.json')
const _ = require('lodash')
const moment = require('moment')

let end = moment()
let start = moment().subtract(6, 'month')
let X_RANGE = end - start

let graphTemplate = `
<svg version="1.2" xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    class="graph"
    aria-labelledby="title"
    height="230px"
    role="img">
<line x1="0%" x2="100%" y1="200" y2="200" stroke-width='2' stroke='gray'></line>
$bars
<text x="5%" y="220" >$jobName</text>
</svg>
`

let barTemplate = `
<g class="bar-section">
<line class='bar success' x1="$X1" x2="$X2" y1="$Y1" y2="200" stroke='$color'></line>
<text class="hint" x="5%" y="30">$hint</text>
</g>
`

let MAX_BAR_HEIGHT = 200.0
let TOTAL_DURATION = end - start

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
}
const sortByKeys = object => {
    const keys = Object.keys(object)
    const sortedKeys = _.sortBy(keys)
  
    return _.fromPairs(
      _.map(sortedKeys, key => [key, object[key]])
    )
  }

let graphs = ''

_.each(sortByKeys(data), (v, jobName) => {
    let lastBuildNo = _.get(v['index'], 'lastBuild.number', -1)
    let $bars = ''
//    if (jobName != 'piranha-cms-deploy-to-test02') return
    _.each(v.builds, build => {
//        console.log(build.id, build.result, build.timestamp, build.duration)
        let ts = moment(build.timestamp)
        let dm = moment.duration(build.duration).minutes()
        let $hint = JSON.stringify({
            name: build.fullDisplayName,
            duration: moment.duration(build.duration).humanize(),
            date: moment(build.timestamp).toISOString()
        })

        $X = ((1.0 - (ts - start) / X_RANGE) * 100.0 ) + '%'
        $Y1 = 190 - 2 * dm


//        console.log(ts, start, $X)
        let $color = 'lightgreen'

        if (build.result === 'SUCCESS') {
            $color = 'lightgreen'
        } else if (build.result === 'FAILURE') {
            $color = 'red'
        } else if (build.result === 'ABORTED') {
            $color = 'lightgray'
        }
        $line = _.clone(barTemplate
                            .replace('$X1', $X)
                            .replace('$X2', $X)
                            .replace('$Y1', $Y1)
                            .replace('$hint', $hint)
                            .replace('$color', $color))
//        console.log($line)

        $bars += $line
    })
    if (lastBuildNo != -1) {
        let timestamp = v.builds['' + lastBuildNo].timestamp
        let offset = moment(timestamp).fromNow();
    }
    graphs += graphTemplate
                .replace('$jobName', jobName)
                .replace('$bars', $bars)
})


let result = `
<style>
* {
    margin: 0;
    border: 0;
    padding: 0;
}
.graph{
    width: 100%;
//    height: 230px;
}
.bar{
    stroke-width: 5;
}
.hint{
    display: none;
}
.bar-section:hover .hint{
    display: block;
    z-index: 2;
}

</style>
`

console.log(start.format('x'), end.format('x'), end-start)
const http = require('http')

http.createServer(function (req, res) {
//    res.writeHead(200, {'Content-Type': 'image/svg+xml'})
    res.write(result + graphs);
    res.end();
}).listen(8082)