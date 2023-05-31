# check_knot_statistics - Icinga / Nagios Plugin to check Knot DNS statistics

![Pylint](https://github.com/mrimann/check_knot_statistics/actions/workflows/pylint.yml/badge.svg)

Goal of this check script is to read Knot DNS statistics and return it so we can collect some relevant performance data over time and e.g. visualize it via Grafana.

## Installation (Icinga2):
to be written
Clone this repository into the directory where you have all your other plugins, for Icinga on Ubuntu, this is probably `/usr/lib/nagios/plugins` but could be somewhere else on your system:

	cd /usr/lib/nagios/plugins
	git clone https://github.com/mrimann/check_knot_statistics.git
    cd check_knot_statistics
    pip install -r requirements.txt

After that, you should be able to test the functionality on CLI before adding it to the Monitoring system:

    python3 /usr/lib/nagios/plugins/check_knot_statistics.py -f /var/run/knot/stats.yaml

As the statistics file by default is not world-readable, it's one option to run this check script via sudo permissions (please configure that to your needs), the following example config is built to run the command via sudo.

To add the command check to your Icinga2 installation, first add the following command definition e.g. to `/etc/icinga2/conf.d/commands.conf`:

	# 'check_knot_statistics' command definition
	object CheckCommand "check_knot_statistics" {
      import "plugin-check-command"
      command = [ "/usr/bin/sudo", PluginDir + "/check_knot_statistics.py" ]

      arguments = {
        "-f" = {
         required = true
         value = "$yaml_path$"
         }
      }
    }

Then add a service definition e.g. to `/etc/icinga2/conf.d/services.conf`:

    apply Service "knot_statistics" {
        import "generic-service"
        display_name = "Knot DNS Statistics"
        vars.yaml_path = "/var/run/knot/stats.yaml"
        check_command = "check_knot_statistics"

        # run on the target server itself
        command_endpoint = host.name

        assign where host.vars.role == "knot-dns-server-role"
    }


**Please adapt the above snippets to your needs!!!** (and refer to the documentation of your monitoring system for further details).

## Command Line Options:

| Option | Triggers what?                                                                          | Mandatory? | Default value |
|--------|-----------------------------------------------------------------------------------------|------------|---------------|
| -h     | Renders the help / usage information                                                    | no         | n/a           |
| -f     | The path to the Knot statistics YAML file | yes        | n/a           |

Hint: The statistics file on Ubuntu is usually at `/var/run/knot/stats.yaml`

## TODO:
Well, it needs some serious testing to be honest - please provide feedback on whether the plugin helped and in which environment you tested it.

And currently it always returns OK and some numbers. As long as the statistics file can be parsed, there's nothing that would result in a WARNING or CRITICAL state, this could e.g. be extended to check for failures or too high number of queries.


## How to contribute?
Feel free to [raise a new issues](https://github.com/mrimann/check_knot_statistics/issues) if you find a problem or to propose a new feature. If you want to contribute your time and submit an improvement, I'm very eager to look at your pull request!

In case you want to discuss a new feature with me, just send me an [e-mail](mailto:mario@rimann.org).


### Contributors / Supporters
Thanks for your support! (in chronological order)
- [internezzo ag](https://www.internezzo.ch/) for sponsoring the initial development

## License
Licensed under the permissive [MIT license](http://opensource.org/licenses/MIT) - have fun with it!

### Can I use it in commercial projects?
Yes, please! And if you save some of your precious time with it, I'd be very happy if you give something back - be it a warm "Thank you" by mail, spending me a drink at a conference, [send me a post card or some other surprise](http://www.rimann.org/support/) :-)
