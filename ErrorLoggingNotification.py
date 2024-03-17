const AWS = require('aws-sdk');
const logs = new AWS.CloudWatchLogs({ apiVersion: '2014-03-28' });

exports.handler = async (event, context) => {
    try {
        // Main logic here

        return { statusCode: 200, body: 'Success' };
    } catch (error) {
        await handle_error_logs('Servers_log_group', error);
        return { statusCode: 500, body: 'Error occurred. Check logs for details.' };
    }
};

async function handle_error_logs(logGroupName, error) {
    const logStreamName = new Date().toISOString().replace(/[-T:]/g, '/').split('.')[0];
    const logEvents = [{ timestamp: Date.now(), message: JSON.stringify({ error }) }];

    await logs.createLogStream({ logGroupName, logStreamName }).promise();
    await logs.putLogEvents({ logGroupName, logStreamName, logEvents }).promise();
}
