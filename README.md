# webhook

This charm makes it very easy to run a script in response to a webhook.
It makes use of the [webhook](https://snapcraft.io/webhook) tool written by Adnan Hajdarevic.

> webhook is a lightweight configurable tool written in Go, that allows you to easily create HTTP endpoints (hooks) on your server, which you can use to execute configured commands. You can also pass data from the HTTP request (such as headers, payload or query variables) to your commands. webhook also allows you to specify rules which have to be satisfied in order for the hook to be triggered.
> 
> For example, if you're using Github or Bitbucket, you can use webhook to set up a hook that runs a redeploy script for your project on your staging server, whenever you push changes to the master branch of your project.
>
> If you use Mattermost or Slack, you can set up an "Outgoing webhook integration" or "Slash command" to run various commands on your server, which can then report back directly to you or your channels using the "Incoming webhook integrations", or the appropriate response body.


## Setting up

You will need to copy the `ops` framework into the charm's `lib/` directory.

This is probably most easily achieved manually at this stage:

```
git clone --depth 1 https://github.com/canonical/operator/ /tmp/operator
mv /tmp/operator/ops lib/ops
```

Or, if you have `just` installed:

```
just update
```

For now, adding your own hooks is slightly awkward. Make any changes to the `DEFAULT_WEBHOOKS` variable within `lib/charm.py`.

You can then deploy the charm:

```
juju deploy .
```
