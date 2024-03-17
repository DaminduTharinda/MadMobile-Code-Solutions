const AWS = require('aws-sdk');
const cloudwatch = new AWS.CloudWatch({ apiVersion: '2010-08-01' });
const logs = new AWS.CloudWatchLogs({ apiVersion: '2014-03-28' });

exports.handler = async (event, context) => {
    const metrics = ['CPUUtilization', 'MemoryUtilization', 'DiskReadBytes', 'NetworkOut', 'NetworkIn'];
    const logGroupName = 'Servers_log_group';
    const logStreamName = new Date().toISOString().replace(/[-T:]/g, '/').split('.')[0];
    const logEvents = [];

    for (const metric of metrics) {
        const params = {
            MetricName: metric,
            Namespace: 'AWS/EC2',
            StartTime: new Date(Date.now() - 60000),
            EndTime: new Date(),
            Period: 60,
            Statistics: ['Average']
        };

        const data = await cloudwatch.getMetricStatistics(params).promise();
        const value = data.Datapoints[0].Average;

        logEvents.push({ timestamp: Date.now(), message: JSON.stringify({ metric, value }) });
    }

    await logs.createLogStream({ logGroupName, logStreamName }).promise();
    await logs.putLogEvents({ logGroupName, logStreamName, logEvents }).promise();

    return { statusCode: 200, body: 'Metrics recorded successfully.' };
};
