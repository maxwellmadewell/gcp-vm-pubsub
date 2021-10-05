const Compute = require('@google-cloud/compute');
const compute = new Compute();

/**
 * Starts Compute Engine instances.
 *
 * Expects a PubSub message with JSON-formatted event data containing the
 * following attributes:
 *  zone - the GCP zone the instances are located in.
 *  label - the label of instances to start.
 *
 * @param {!object} event Cloud Function PubSub message event.
 * @param {!object} callback Cloud Function PubSub callback indicating
 *  completion.
 */
exports.startInstancePubSub = async (event, context, callback) => {
    try {
        const payload = _validatePayload(
            JSON.parse(Buffer.from(event.data, 'base64').toString())
        );
        // get vm instanaces by labels/metadata rather than name
        // more convinient to change vm metadata rather changing cloud functions code
        const options = { filter: `labels.${payload.label}` };
        const [vms] = await compute.getVMs(options);
        let vmCount = 0;
        await Promise.all(
            vms.map(async (instance) => {
                console.log(`instance=${instance.name}, zone=${instance.zone.id}`)
                if (payload.zone === instance.zone.id) {
                    const [operation] = await compute
                        .zone(payload.zone)
                        .vm(instance.name)
                        .start();
                    vmCount += 1
                    // Operation pending
                    return operation.promise();
                }
            })
        );

        // Operation complete. Instance successfully started.
        const message = `Successfully started ${vmCount} instance(s)`;
        console.log(message);
        callback(null, message);
    } catch (err) {
        console.log(err);
        callback(err);
    }
};

/**
 * Validates that a request payload contains the expected fields.
 *
 * @param {!object} payload the request payload to validate.
 * @return {!object} the payload object.
 */
const _validatePayload = (payload) => {
    if (!payload.zone) {
        throw new Error(`Attribute 'zone' missing from payload`);
    } else if (!payload.label) {
        throw new Error(`Attribute 'label' missing from payload`);
    }
    return payload;
};