#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause-Patent

import json
from subprocess import run, check_output
import pathlib

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus

# TODO: put this in a proper location
HOOKS_LOCATION = "/home/ubuntu/webhooks.json"

SERVICE = f"""
[Unit]
Description=Webhooks as a service
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/snap run webhook -hooks {HOOKS_LOCATION}
ExecStop=/bin/kill -2 $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

DEFAULT_WEBHOOKS = [
   {"id": "hello", "execute-command": "echo", "pass-arguments-to-command": [{"source": "string", "name": "hello" }]},
]

def write_webhooks():
    with open(HOOKS_LOCATION, 'w') as f:
        json.dump(DEFAULT_WEBHOOKS, f)
    run(["chown", "ubuntu:ubuntu", HOOKS_LOCATION])


def write_systemd_service():
    with open('/etc/systemd/system/webhook.service', 'w') as f:
        f.write(SERVICE)
    run(['systemctl', 'daemon-reload'])


def restart():
    run(["systemctl", "reload-or-restart", "webhook"])


def open_port(port: int, protocol= "tcp"):
    assert protocol in {"tcp", "udp", "icmp"}
    run(["open-port", f"{port}/{protocol}"])


class WebhookCharm(CharmBase):

    state = StoredState()

    def __init__(self, parent, key):
        super().__init__(parent, key)
        self.my = self.framework.model.unit
        self.framework.observe(self.on.install, self.install)
        self.framework.observe(self.on.update_status, self.check_health)

    def install(self, event):
        self.my.status = MaintenanceStatus("installing dependencies")
        run(['snap', 'install', 'webhook'])
        write_webhooks()
        write_systemd_service()
        restart()
        open_port(9000)
        self.state.installed = True
        self.my.status = ActiveStatus()

    def check_health(self, event):
        if not self.state.installed:
            return

        status_raw = check_output(["systemctl", "show", "webhook", "--no-page"])
        for line in status_raw:
            key, val = line.rstrip().split('=')
            if key == "ActiveState":
                if val == "active":
                    self.my.status = ActiveStatus()
                else:
                    self.my.status = BlockedStatus(f"service unhealthy ({val}); intervention required")
                return


if __name__ == '__main__':
    main(WebhookCharm)
